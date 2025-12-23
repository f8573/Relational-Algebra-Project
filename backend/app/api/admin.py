"""Admin API endpoints for course and assignment management."""
from flask import Blueprint, jsonify, request, current_app
from .auth_decorators import verify_token
from app.models import Course, Assessment, Question, Attempt, Submission, AuditLog, CourseMembership, User, DatabaseFile
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from flask import current_app
import sqlite3
from sqlalchemy import text

bp = Blueprint('admin', __name__)


def require_platform_admin():
    if not getattr(request, 'user', None) or not request.user.is_platform_admin:
        return jsonify({'status': 'error', 'message': 'Admin privileges required'}), 403


@bp.route('/courses', methods=['GET'])
@verify_token
def admin_list_courses():
    resp = require_platform_admin()
    if resp:
        return resp
    courses = Course.query.order_by(Course.id.desc()).all()
    out = []
    for c in courses:
        out.append({'id': c.id, 'title': c.title, 'term': c.term, 'description': c.description, 'created_at': c.created_at.isoformat() if c.created_at else None})
    return jsonify({'status': 'success', 'courses': out}), 200


@bp.route('/courses', methods=['POST'])
@verify_token
def admin_create_course():
    resp = require_platform_admin()
    if resp:
        return resp
    data = request.get_json() or {}
    title = data.get('title')
    term = data.get('term')
    description = data.get('description')
    if not title:
        return jsonify({'status': 'error', 'message': 'title is required'}), 400
    course = Course(title=title, term=term, description=description)
    db.session.add(course)
    db.session.commit()
    return jsonify({'status': 'success', 'course': {'id': course.id, 'title': course.title, 'term': course.term, 'description': course.description}}), 201


@bp.route('/courses/<int:course_id>', methods=['PUT'])
@verify_token
def admin_update_course(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    data = request.get_json() or {}
    course.title = data.get('title', course.title)
    course.term = data.get('term', course.term)
    course.description = data.get('description', course.description)
    db.session.add(course)
    db.session.commit()
    return jsonify({'status': 'success', 'course': {'id': course.id, 'title': course.title, 'term': course.term, 'description': course.description}}), 200


@bp.route('/courses/<int:course_id>', methods=['DELETE'])
@verify_token
def admin_delete_course(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'status': 'success', 'deleted': course_id}), 200


@bp.route('/courses/<int:course_id>/assignments', methods=['GET'])
@verify_token
def admin_course_assignments(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    assessments = Assessment.query.filter_by(course_id=course_id).all()
    out = []
    for a in assessments:
        qs = []
        # Try to SELECT including db_id; if the column doesn't exist (older DB),
        # fall back to selecting only id/prompt/points and set db_id to None.
        try:
            stmt = text("SELECT id, prompt, points, db_id, solution_query FROM questions WHERE assessment_id = :aid ORDER BY order_index")
            res = db.session.execute(stmt, {'aid': a.id})
            rows = res.fetchall()
            for r in rows:
                try:
                    m = r._mapping
                    dbval = m.get('db_id') if 'db_id' in m.keys() else None
                    sol = m.get('solution_query') if 'solution_query' in m.keys() else None
                    qs.append({'id': m.get('id'), 'prompt': m.get('prompt'), 'points': m.get('points'), 'db_id': dbval, 'solution_query': sol})
                except Exception:
                    # Row may be tuple-like
                    vals = list(r)
                    qs.append({'id': vals[0], 'prompt': vals[1], 'points': vals[2], 'db_id': vals[3] if len(vals) > 3 else None, 'solution_query': vals[4] if len(vals) > 4 else None})
        except Exception:
            try:
                stmt = text("SELECT id, prompt, points, solution_query FROM questions WHERE assessment_id = :aid ORDER BY order_index")
                res = db.session.execute(stmt, {'aid': a.id})
                rows = res.fetchall()
                for r in rows:
                    try:
                        m = r._mapping
                        qs.append({'id': m.get('id'), 'prompt': m.get('prompt'), 'points': m.get('points'), 'db_id': None, 'solution_query': m.get('solution_query')})
                    except Exception:
                        vals = list(r)
                        qs.append({'id': vals[0], 'prompt': vals[1], 'points': vals[2], 'db_id': None, 'solution_query': vals[3] if len(vals) > 3 else None})
            except Exception:
                current_app.logger.exception('Failed to load questions for assessment %s', a.id)
        out.append({'id': a.id, 'title': a.title, 'questions': qs})
    return jsonify({'status': 'success', 'assignments': out}), 200


@bp.route('/databases', methods=['GET'])
@verify_token
def admin_list_databases():
    resp = require_platform_admin()
    if resp:
        return resp
    dbs = DatabaseFile.query.order_by(DatabaseFile.uploaded_at.desc()).all()
    # Determine configured BANK_DB basename so frontend can prefer it as default
    try:
        bank_db_path = current_app.config.get('BANK_DB')
        bank_basename = os.path.basename(bank_db_path) if bank_db_path else None
    except Exception:
        bank_basename = None

    out = []
    for d in dbs:
        rec = d.to_dict()
        rec['is_bank'] = (bank_basename is not None and rec.get('filename') == bank_basename)
        out.append(rec)

    return jsonify({'status':'success','databases': out}), 200


@bp.route('/databases/<int:db_id>', methods=['DELETE'])
@verify_token
def admin_delete_database(db_id):
    resp = require_platform_admin()
    if resp:
        return resp
    dbf = DatabaseFile.query.get(db_id)
    if not dbf:
        return jsonify({'status':'error', 'message': 'Database not found'}), 404
    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
    path = os.path.join(upload_dir, dbf.filename)
    try:
        # remove file if exists
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        current_app.logger.exception('Failed to remove database file: %s', path)
    try:
        db.session.delete(dbf)
        db.session.commit()
        return jsonify({'status': 'success', 'deleted': db_id}), 200
    except Exception:
        current_app.logger.exception('Failed to delete database record')
        return jsonify({'status': 'error', 'message': 'Delete failed'}), 500


@bp.route('/databases', methods=['POST'])
@verify_token
def admin_upload_database():
    resp = require_platform_admin()
    if resp:
        return resp
    if 'file' not in request.files:
        return jsonify({'status':'error','message':'file is required'}), 400
    f = request.files['file']
    name = request.form.get('name') or f.filename
    filename = secure_filename(f.filename)
    # Limit allowed file extensions for uploaded databases
    allowed_ext = {'.db', '.sqlite', '.sqlite3'}
    _, ext = os.path.splitext(filename)
    if (ext or '').lower() not in allowed_ext:
        return jsonify({'status':'error', 'message': 'Unsupported file type'}), 400

    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
    os.makedirs(upload_dir, exist_ok=True)
    dest = os.path.join(upload_dir, filename)
    f.save(dest)
    # Validate sqlite by opening and listing tables
    try:
        conn = sqlite3.connect(dest)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        _ = cur.fetchall()
        conn.close()
    except Exception:
        try:
            os.remove(dest)
        except Exception:
            pass
        return jsonify({'status':'error','message':'Uploaded file is not a valid sqlite database'}), 400

    dbf = DatabaseFile(name=name, filename=filename)
    db.session.add(dbf)
    db.session.commit()
    return jsonify({'status':'success','database':dbf.to_dict()}), 201


@bp.route('/assignments/<int:assessment_id>/submissions', methods=['GET'])
@verify_token
def admin_assignment_submissions(assessment_id):
    resp = require_platform_admin()
    if resp:
        return resp
    # find attempts for this assessment
    attempts = Attempt.query.filter_by(assessment_id=assessment_id).all()
    rows = []
    for a in attempts:
        for s in a.submissions:
            rows.append({
                'submission_id': s.id,
                'attempt_id': a.id,
                'student_id': a.user_id,
                'question_id': s.question_id,
                'score': s.score_earned,
                'last_updated': s.last_updated.isoformat() if s.last_updated else None
            })
    return jsonify({'status': 'success', 'submissions': rows}), 200


@bp.route('/submissions/<int:submission_id>/grade', methods=['POST'])
@verify_token
def admin_grade_submission(submission_id):
    resp = require_platform_admin()
    if resp:
        return resp
    data = request.get_json() or {}
    score = data.get('score')
    feedback = data.get('feedback')
    if score is None:
        return jsonify({'status': 'error', 'message': 'score is required'}), 400

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'status': 'error', 'message': 'Submission not found'}), 404

    old = submission.score_earned
    submission.score_earned = float(score)
    if feedback is not None:
        submission.grading_feedback = feedback
    db.session.add(submission)
    db.session.commit()

    # Record audit
    try:
        AuditLog.record(actor_id=request.user.id, target_id=submission.attempt.user_id,
                        event_type='grade_changed', resource_type='submission',
                        resource_id=submission.id, ip=request.remote_addr,
                        ua=request.headers.get('User-Agent'), meta={'old_score': old, 'new_score': submission.score_earned})
    except Exception:
        current_app.logger.exception('Failed to write audit log')

    return jsonify({'status': 'success', 'submission_id': submission.id, 'score': submission.score_earned}), 200


@bp.route('/courses/<int:course_id>/assignments', methods=['POST'])
@verify_token
def admin_create_assignment(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'status': 'error', 'message': 'title is required'}), 400
    assignment = Assessment(title=title, course_id=course_id)
    db.session.add(assignment)
    db.session.flush()
    # Optionally create questions if provided
    questions = data.get('questions') or []
    for q in questions:
        QuestionObj = Question(prompt=q.get('prompt', ''), points=q.get('points', 0), assessment_id=assignment.id, db_id=q.get('db_id'), solution_query=q.get('solution_query'))
        db.session.add(QuestionObj)
    db.session.commit()
    return jsonify({'status': 'success', 'assignment': {'id': assignment.id, 'title': assignment.title}}), 201


@bp.route('/courses/<int:course_id>/members', methods=['GET'])
@verify_token
def admin_list_course_members(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    members = CourseMembership.query.filter_by(course_id=course_id).all()
    out = []
    for m in members:
        out.append({'id': m.user.id, 'email': m.user.email, 'name': m.user.name, 'role': m.role})
    return jsonify({'status': 'success', 'members': out}), 200


@bp.route('/databases/<int:db_id>/preview', methods=['GET'])
@verify_token
def admin_database_preview(db_id):
    resp = require_platform_admin()
    if resp:
        return resp
    dbf = DatabaseFile.query.get(db_id)
    if not dbf:
        return jsonify({'status':'error','message':'Database not found'}), 404
    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
    path = os.path.join(upload_dir, dbf.filename)
    if not os.path.exists(path):
        return jsonify({'status':'error','message':'File missing on server'}), 404
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        out = []
        for t in tables:
            cur.execute(f"PRAGMA table_info('{t}')")
            cols = [r[1] for r in cur.fetchall()]
            cur.execute(f"SELECT * FROM '{t}' LIMIT 5")
            rows = [dict(r) for r in cur.fetchall()]
            out.append({'name': t, 'columns': cols, 'sample': rows})
        conn.close()
        return jsonify({'status':'success','tables': out}), 200
    except Exception:
        current_app.logger.exception('Failed to preview database')
        return jsonify({'status':'error','message':'Preview failed'}), 500


@bp.route('/courses/<int:course_id>/members', methods=['POST'])
@verify_token
def admin_enroll_member(course_id):
    resp = require_platform_admin()
    if resp:
        return resp
    data = request.get_json() or {}
    email = data.get('email')
    role = data.get('role', 'student')
    name = data.get('name')
    if not email:
        return jsonify({'status': 'error', 'message': 'email is required'}), 400
    # find or create user
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.flush()
    # check existing membership
    existing = CourseMembership.query.filter_by(course_id=course_id, user_id=user.id).first()
    if existing:
        return jsonify({'status': 'error', 'message': 'user already enrolled'}), 400
    membership = CourseMembership(course_id=course_id, user_id=user.id, role=role)
    db.session.add(membership)
    db.session.commit()
    return jsonify({'status': 'success', 'member': {'id': user.id, 'email': user.email, 'name': user.name, 'role': role}}), 201


@bp.route('/courses/<int:course_id>/members/<int:user_id>', methods=['DELETE'])
@verify_token
def admin_remove_member(course_id, user_id):
    resp = require_platform_admin()
    if resp:
        return resp
    membership = CourseMembership.query.filter_by(course_id=course_id, user_id=user_id).first()
    if not membership:
        return jsonify({'status': 'error', 'message': 'membership not found'}), 404
    db.session.delete(membership)
    db.session.commit()
    return jsonify({'status': 'success', 'deleted': {'course_id': course_id, 'user_id': user_id}}), 200


@bp.route('/courses/<int:course_id>/members/<int:user_id>', methods=['PUT'])
@verify_token
def admin_update_member(course_id, user_id):
    resp = require_platform_admin()
    if resp:
        return resp
    membership = CourseMembership.query.filter_by(course_id=course_id, user_id=user_id).first()
    if not membership:
        return jsonify({'status': 'error', 'message': 'membership not found'}), 404
    data = request.get_json() or {}
    membership.role = data.get('role', membership.role)
    db.session.add(membership)
    db.session.commit()
    return jsonify({'status': 'success', 'member': {'id': membership.user_id, 'role': membership.role}}), 200


@bp.route('/users', methods=['GET'])
@verify_token
def admin_search_users():
    """Search users by name or email (admin only)."""
    resp = require_platform_admin()
    if resp:
        return resp
    q = (request.args.get('q') or '').strip()
    limit = int(request.args.get('limit') or 20)
    if not q:
        return jsonify({'status': 'success', 'users': []}), 200
    pattern = f"%{q}%"
    users = User.query.filter((User.email.ilike(pattern)) | (User.name.ilike(pattern))).limit(limit).all()
    out = [{'id': u.id, 'email': u.email, 'name': u.name} for u in users]
    return jsonify({'status': 'success', 'users': out}), 200


@bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@verify_token
def admin_update_assignment(assignment_id):
    resp = require_platform_admin()
    if resp:
        return resp
    assignment = Assessment.query.get(assignment_id)
    if not assignment:
        return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404
    data = request.get_json() or {}
    assignment.title = data.get('title', assignment.title)
    # If questions provided, replace existing questions safely
    if 'questions' in data:
        questions = data.get('questions') or []
        # clear existing relationship (cascade will delete orphans)
        assignment.questions[:] = []
        db.session.flush()
        # create and append new Question objects with proper ordering
        for idx, q in enumerate(questions):
            QuestionObj = Question(prompt=q.get('prompt', ''), points=q.get('points', 0), order_index=idx, db_id=q.get('db_id'), solution_query=q.get('solution_query'))
            assignment.questions.append(QuestionObj)
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'status': 'success', 'assignment': {'id': assignment.id, 'title': assignment.title}}), 200


@bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@verify_token
def admin_delete_assignment(assignment_id):
    resp = require_platform_admin()
    if resp:
        return resp
    assignment = Assessment.query.get(assignment_id)
    if not assignment:
        return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'status': 'success', 'deleted': assignment_id}), 200


@bp.route('/questions/<int:question_id>', methods=['GET'])
@verify_token
def admin_get_question(question_id):
    resp = require_platform_admin()
    if resp:
        return resp
    q = Question.query.get(question_id)
    if not q:
        return jsonify({'status': 'error', 'message': 'Question not found'}), 404
    return jsonify({'status': 'success', 'question': {'id': q.id, 'prompt': q.prompt, 'points': q.points, 'db_id': q.db_id, 'solution_query': q.solution_query}}), 200


@bp.route('/questions/<int:question_id>', methods=['PUT'])
@verify_token
def admin_update_question(question_id):
    resp = require_platform_admin()
    if resp:
        return resp
    q = Question.query.get(question_id)
    if not q:
        return jsonify({'status': 'error', 'message': 'Question not found'}), 404
    data = request.get_json() or {}
    # require solution_query to be present (non-empty)
    sol = data.get('solution_query')
    if sol is None:
        return jsonify({'status': 'error', 'message': 'solution_query is required'}), 400
    q.prompt = data.get('prompt', q.prompt)
    q.points = data.get('points', q.points)
    q.db_id = data.get('db_id', q.db_id)
    q.solution_query = sol
    db.session.add(q)
    db.session.commit()
    return jsonify({'status': 'success', 'question': {'id': q.id, 'solution_query': q.solution_query}}), 200
