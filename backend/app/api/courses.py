"""Course-related routes."""
from flask import Blueprint, jsonify, request, current_app
from app.models import Course, CourseMembership, User
from app.extensions import db
from .auth_decorators import verify_token
from app.models.course import Course as CourseModel
from app.models.user import CourseMembership as CourseMembershipModel
from app.models.assessment import Assessment, Question
from app.models.submission import Attempt, Submission
from sqlalchemy import func

bp = Blueprint("courses", __name__)


@bp.route('/', methods=['GET'])
@verify_token
def list_courses():
    """Get all courses the user is enrolled in."""
    user = request.user
    
    # Get user's course memberships
    memberships = CourseMembership.query.filter_by(user_id=user.id).all()
    courses = []
    
    for membership in memberships:
        course_data = {
            'id': membership.course.id,
            'title': membership.course.title,
            'role': membership.role,
            'created_at': membership.course.created_at.isoformat() if membership.course.created_at else None
        }
        courses.append(course_data)
    
    return jsonify({
        'status': 'success',
        'courses': courses
    }), 200


@bp.route('/', methods=['POST'])
@verify_token
def create_course():
    """Create a new course and enroll the creator as instructor."""
    user = request.user
    data = request.get_json() or {}
    title = data.get('title')
    term = data.get('term')
    description = data.get('description')

    if not title:
        return jsonify({'status': 'error', 'message': 'Title is required'}), 400

    # Create course
    course = Course(title=title, term=term, description=description)
    db.session.add(course)
    db.session.flush()

    # Enroll creator as instructor
    membership = CourseMembership(course_id=course.id, user_id=user.id, role='instructor')
    db.session.add(membership)
    db.session.commit()

    current = {
        'id': course.id,
        'title': course.title,
        'term': course.term,
        'description': course.description,
        'created_at': course.created_at.isoformat() if course.created_at else None
    }

    return jsonify({'status': 'success', 'course': current}), 201


@bp.route('/<int:course_id>', methods=['GET'])
@verify_token
def get_course(course_id):
    """Get course details if user is enrolled."""
    user = request.user
    
    # Check if user is enrolled in this course
    membership = CourseMembership.query.filter_by(
        course_id=course_id,
        user_id=user.id
    ).first()
    
    if not membership:
        return jsonify({
            'status': 'error',
            'message': 'Not enrolled in this course'
        }), 403
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({
            'status': 'error',
            'message': 'Course not found'
        }), 404

    return jsonify({
        'status': 'success',
        'course': {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'role': membership.role,
            'created_at': course.created_at.isoformat() if course.created_at else None
        }
    }), 200


@bp.route('/<int:course_id>/assignments', methods=['GET'])
@verify_token
def public_course_assignments(course_id):
    """List assignments for a course with question counts and the current user's grade."""
    user = request.user

    # verify enrollment
    membership = CourseMembership.query.filter_by(course_id=course_id, user_id=user.id).first()
    if not membership:
        return jsonify({'status': 'error', 'message': 'Not enrolled in this course'}), 403

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    assessments = Assessment.query.filter_by(course_id=course_id).all()
    out = []
    for a in assessments:
        # Use a count query to avoid loading Question objects (which may reference
        # schema columns that don't exist on older DBs). This avoids OperationalError
        # when the `questions` table lacks newer columns like `db_id`.
        try:
            qcount = db.session.query(func.count(Question.id)).filter(Question.assessment_id == a.id).scalar() or 0
        except Exception:
            # Fallback: avoid crashing, treat as zero questions
            qcount = 0
        # compute total points for assignment
        try:
            total_points = float(db.session.query(func.coalesce(func.sum(Question.points), 0)).filter(Question.assessment_id == a.id).scalar() or 0.0)
        except Exception:
            total_points = 0.0
        # compute grade as the average of per-question grades that have at least
        # one submission (unweighted per-question average). For each question
        # with at least one submission from this user, compute (score/points)*100
        # and average those percentages.
        percent = None
        letter = None
        try:
            # Simpler: for each question, fetch the latest submission for
            # this user (if any) and compute the per-question percent.
            # Then average only across questions that have at least one
            # submission (graded questions).
            try:
                q_rows = Question.query.filter(Question.assessment_id == a.id).all()
            except Exception:
                # Older DB schemas may lack newer Question columns; select
                # only the minimal columns we need (id, points) via raw SQL
                from sqlalchemy import text
                q_rows = []
                try:
                    res = db.session.execute(text("SELECT id, points FROM questions WHERE assessment_id = :aid ORDER BY id"), {'aid': a.id})
                    for r in res.fetchall():
                        # build a lightweight object with id and points attrs
                        class _Q:
                            pass
                        q = _Q()
                        try:
                            m = r._mapping
                            q.id = m.get('id')
                            q.points = m.get('points')
                        except Exception:
                            vals = list(r)
                            q.id = vals[0]
                            q.points = vals[1] if len(vals) > 1 else None
                        q_rows.append(q)
                except Exception:
                    current_app.logger.exception('Failed raw-selecting questions for assignment %s during percent calc', a.id)
                    q_rows = []
            if q_rows:
                pct_sum = 0.0
                pct_count = 0
                for q in q_rows:
                    try:
                        qid = int(getattr(q, 'id', 0) or 0)
                        qpoints = getattr(q, 'points', None)
                        if qid is None or not qpoints or float(qpoints) <= 0:
                            continue
                        # latest submission for this user & question
                        sub = None
                        try:
                            sub = Submission.query.join(Attempt).filter(
                                Attempt.user_id == user.id,
                                Submission.question_id == qid
                            ).order_by(Submission.last_updated.desc()).first()
                        except Exception:
                            sub = None
                        if sub and sub.score_earned is not None:
                            score = float(sub.score_earned or 0.0)
                            pct = (score / float(qpoints)) * 100.0
                            pct_sum += pct
                            pct_count += 1
                    except Exception:
                        # skip problematic question rows but keep processing
                        current_app.logger.exception('Error processing question %s for percent calc', getattr(q, 'id', None))
                if pct_count > 0:
                    percent = pct_sum / float(pct_count)
                else:
                    percent = None
            else:
                percent = None
        except Exception:
            current_app.logger.exception('Failed computing per-question latest scores for assignment %s user %s', a.id, user.id)
            percent = None
        label = None
        # If we couldn't compute per-question percent (no per-question
        # submissions found), fall back to latest attempt.total_score
        # divided by total_points so instructors still see a grade in
        # environments where questions/submissions mapping may differ.
        if percent is None and total_points and total_points > 0:
            try:
                latest_attempt = Attempt.query.filter_by(assessment_id=a.id, user_id=user.id).order_by(Attempt.submitted_at.desc()).first()
                if latest_attempt and latest_attempt.total_score is not None:
                    percent = (float(latest_attempt.total_score) / float(total_points)) * 100.0
            except Exception:
                percent = None
        # Compute letter grade from percent if available
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
            label = f"{letter} ({round(percent)}%)"
        out.append({
            'id': a.id,
            'title': a.title,
            'question_count': qcount,
            'total_points': total_points,
            'user_grade': label,
            'percent': percent,
            'letter': letter,
        })

    return jsonify({'status': 'success', 'assignments': out}), 200
