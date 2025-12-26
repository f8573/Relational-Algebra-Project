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
            # Use a window function to select the latest submission per question
            # for this user & assessment. This avoids relying on ORM ordering
            # and is efficient in SQL.
            from sqlalchemy import text
            sql = text('''
                SELECT question_id, score_earned FROM (
                  SELECT s.question_id, s.score_earned,
                         row_number() OVER (PARTITION BY s.question_id ORDER BY s.last_updated DESC) as rn
                  FROM submissions s
                  JOIN attempts at ON s.attempt_id = at.id
                  WHERE at.user_id = :uid AND at.assessment_id = :aid
                ) t WHERE rn = 1
            ''')
            rows = db.session.execute(sql, {'uid': user.id, 'aid': a.id}).fetchall()
            # map question_id -> score
            latest_by_q = { int(r[0]): float(r[1] or 0.0) for r in rows }
            
            # Load ALL questions for this assessment to properly weight the grade
            q_rows = Question.query.filter(Question.assessment_id == a.id).all()
            if q_rows:
                pct_sum = 0.0
                pct_count = 0
                for q in q_rows:
                    qid = int(getattr(q, 'id', 0) or 0)
                    qpoints = getattr(q, 'points', None)
                    if qpoints and float(qpoints) > 0:
                        # Only include this question if the user has at least
                        # one submission for it — do not count unanswered
                        # questions as zero in the average.
                        if qid in latest_by_q:
                            score = float(latest_by_q.get(qid, 0.0))
                            pct = (score / float(qpoints)) * 100.0
                            pct_sum += pct
                            pct_count += 1
                if pct_count > 0:
                    percent = pct_sum / float(pct_count)
            else:
                percent = None
        except Exception:
            current_app.logger.exception('Failed computing per-question latest scores for assignment %s user %s', a.id, user.id)
            percent = None
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

        if letter is not None and percent is not None:
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
