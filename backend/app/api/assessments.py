"""Assessment-related routes (simplified)."""
from flask import Blueprint, jsonify, request, current_app
from app.extensions import db
from app.models.submission import Attempt, Submission
from app.models.assessment import Assessment
from app.services.grading import grade_submission
from .auth_decorators import verify_token
from flask import request
from app.models import CourseMembership, Question
from app.extensions import db as _db

bp = Blueprint("assessments", __name__)


@bp.route('/', methods=['GET'])
def list_assessments():
    """Return a short list of assessment ids.

    This is a lightweight helper used by the frontend to fetch a paged
    list of assessments. It returns only ids for simplicity.
    """
    items = [a.id for a in Assessment.query.limit(50).all()]
    return jsonify(items)


@bp.route('/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """Return assessment details and record an 'assignment_opened' audit."""
    a = Assessment.query.get(assessment_id)
    if not a:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    # Record audit that current requester opened the assignment (if provided)
    try:
        from app.models import AuditLog
        # actor unknown for anonymous calls; try to read from request json headers
        actor = None
        if 'Authorization' in request.headers:
            # do not decode token here; just record request origin as actor None
            actor = None
        AuditLog.record(actor_id=actor, event_type='assignment_opened', resource_type='assessment', resource_id=a.id, ip=request.remote_addr, ua=request.headers.get('User-Agent'))
    except Exception:
        pass

    return jsonify({
        'id': a.id,
        'title': a.title,
        'course_id': a.course_id
    })


@bp.route('/submit', methods=['POST'])
def submit_answer():
    payload = request.get_json() or {}
    user_id = payload.get('user_id')
    assessment_id = payload.get('assessment_id')
    question_id = payload.get('question_id')
    query = payload.get('query', '')

    # Find or create Attempt
    attempt = (
        Attempt.query.filter_by(user_id=user_id, assessment_id=assessment_id)
        .first()
    )
    if not attempt:
        attempt = Attempt(user_id=user_id, assessment_id=assessment_id)
        db.session.add(attempt)
        db.session.commit()

    submission = Submission(
        attempt_id=attempt.id,
        question_id=question_id,
        student_query=query,
    )
    db.session.add(submission)
    db.session.commit()

    # Audit: record submission created
    try:
        from app.models import AuditLog
        AuditLog.record(actor_id=user_id, event_type='submission_created', resource_type='submission', resource_id=submission.id, ip=request.remote_addr, ua=request.headers.get('User-Agent'), meta={'assessment_id': assessment_id, 'question_id': question_id})
    except Exception:
        pass

    # Grading is synchronous for now; consider async worker later
    result = grade_submission(submission)

    # Recompute attempt total score
    try:
        subs = Submission.query.filter_by(attempt_id=attempt.id).all()
        total = sum((s.score_earned or 0.0) for s in subs)
        attempt.total_score = float(total)
        db.session.add(attempt)
        db.session.commit()
    except Exception:
        pass

    return jsonify({
        "status": "graded",
        "result": result,
    })


@bp.route('/<int:assessment_id>/submissions', methods=['GET'])
@verify_token
def user_assessment_submissions(assessment_id):
    """Return submissions for the current user for a given assessment."""
    user = request.user
    attempts = Attempt.query.filter_by(assessment_id=assessment_id, user_id=user.id).all()
    out = []
    for a in attempts:
        subs = []
        for s in a.submissions:
            subs.append({
                'submission_id': s.id,
                'question_id': s.question_id,
                'score': s.score_earned,
                'last_updated': s.last_updated.isoformat() if s.last_updated else None,
                'student_query': s.student_query
            })
        out.append({'attempt_id': a.id, 'submitted_at': a.submitted_at.isoformat() if a.submitted_at else None, 'total_score': a.total_score, 'submissions': subs})
    return jsonify({'status':'success','attempts': out}), 200


@bp.route('/<int:assessment_id>/questions', methods=['GET'])
@verify_token
def list_assessment_questions(assessment_id):
    """Return questions for an assessment if the caller is enrolled."""
    user = request.user
    a = Assessment.query.get(assessment_id)
    if not a:
        return jsonify({'status': 'error', 'message': 'Assessment not found'}), 404
    # verify enrollment
    membership = CourseMembership.query.filter_by(course_id=a.course_id, user_id=user.id).first()
    if not membership:
        return jsonify({'status': 'error', 'message': 'Not enrolled'}), 403
    qs = []
    total_points = 0.0
    user_total = 0.0
    try:
        try:
            rows = Question.query.filter_by(assessment_id=assessment_id).order_by(Question.order_index).all()
        except Exception:
            # Fallback for older DB schemas: select columns directly
            rows = []
            try:
                stmt = current_app.extensions['db'].session.execute if hasattr(current_app, 'extensions') and False else None
            except Exception:
                stmt = None
            try:
                from sqlalchemy import text
                res = db.session.execute(text("SELECT id, prompt, points, db_id, solution_query FROM questions WHERE assessment_id = :aid ORDER BY id"), {'aid': assessment_id})
                fetched = res.fetchall()
                for r in fetched:
                    try:
                        m = r._mapping
                        q = Question()
                        q.id = m.get('id')
                        q.prompt = m.get('prompt')
                        q.points = m.get('points')
                        q.db_id = m.get('db_id')
                        q.solution_query = m.get('solution_query')
                        rows.append(q)
                    except Exception:
                        vals = list(r)
                        q = Question()
                        q.id = vals[0]
                        q.prompt = vals[1]
                        q.points = vals[2]
                        q.db_id = vals[3] if len(vals) > 3 else None
                        q.solution_query = vals[4] if len(vals) > 4 else None
                        rows.append(q)
            except Exception:
                current_app.logger.exception('Failed raw-selecting questions for assessment %s', assessment_id)
                raise
        # find latest attempt for this user/assessment (if any)
        latest_attempt = None
        try:
            latest_attempt = Attempt.query.filter_by(assessment_id=assessment_id, user_id=user.id).order_by(Attempt.submitted_at.desc()).first()
        except Exception:
            latest_attempt = None

        def _get(q, name):
            if isinstance(q, dict):
                return q.get(name)
            return getattr(q, name, None)

        for q in rows:
            qobj = {
                'id': _get(q, 'id'),
                'prompt': _get(q, 'prompt'),
                'points': _get(q, 'points'),
                'db_id': _get(q, 'db_id'),
                'solution_query': _get(q, 'solution_query')
            }
            total_points += float(qobj['points'] or 0)
            sub = None
            try:
                qid = qobj['id']
                if latest_attempt and qid is not None:
                    sub = Submission.query.filter_by(attempt_id=latest_attempt.id, question_id=qid).order_by(Submission.last_updated.desc()).first()
            except Exception:
                current_app.logger.exception('Failed to load submission for question %s', qobj.get('id'))
                sub = None

            if sub:
                qobj['score'] = float(sub.score_earned or 0)
                qobj['student_query'] = sub.student_query
                user_total += float(sub.score_earned or 0)
            else:
                qobj['score'] = None
                qobj['student_query'] = None
            qs.append(qobj)

        percent = (user_total / total_points * 100.0) if total_points > 0 else None
        # compute letter grade
        letter = None
        if percent is not None:
            p = percent
            if p >= 93: letter = 'A'
            elif p >= 90: letter = 'A-'
            elif p >= 87: letter = 'B+'
            elif p >= 83: letter = 'B'
            elif p >= 80: letter = 'B-'
            elif p >= 77: letter = 'C+'
            elif p >= 73: letter = 'C'
            elif p >= 70: letter = 'C-'
            elif p >= 67: letter = 'D+'
            elif p >= 63: letter = 'D'
            elif p >= 60: letter = 'D-'
            else: letter = 'F'
    except Exception:
        current_app.logger.exception('Failed to load questions for assessment %s', assessment_id)
        return jsonify({'status': 'error', 'message': 'Failed to load questions'}), 500

    return jsonify({'status': 'success', 'questions': qs, 'total_points': total_points, 'user_points': user_total, 'percent': percent, 'letter_grade': letter}), 200
