import json
import jwt
from datetime import datetime, timedelta
from app.extensions import db
from app.models import User, Course, CourseMembership, Assessment, Question, Attempt, Submission, AuditLog


def make_admin(app):
    with app.app_context():
        admin = User(email='admin2@example.com', name='Admin Two', is_platform_admin=True)
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()
        return admin.id


def make_student_submission(app, student_id, assessment_id):
    with app.app_context():
        attempt = Attempt(user_id=student_id, assessment_id=assessment_id)
        db.session.add(attempt)
        db.session.flush()
        sub = Submission(attempt_id=attempt.id, question_id=1, student_query='S', score_earned=0.0)
        db.session.add(sub)
        db.session.commit()
        return sub.id, attempt.id


def get_token_for_user(app, user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
    return token


def test_admin_grade_records_audit(app):
    client = app.test_client()
    with app.app_context():
        # create student and assessment
        student = User(email='s1@example.com', name='Student One')
        student.set_password('pw')
        db.session.add(student)
        course = Course(title='Admin Course')
        db.session.add(course)
        db.session.flush()
        # enroll student
        cm = CourseMembership(course_id=course.id, user_id=student.id, role='student')
        db.session.add(cm)
        # create assessment + question
        a = Assessment(course_id=course.id, title='A1')
        db.session.add(a)
        db.session.flush()
        q = Question(assessment_id=a.id, prompt='Q1', points=5, solution_query='S')
        db.session.add(q)
        db.session.commit()

        # create submission
        sub_id, attempt_id = make_student_submission(app, student.id, a.id)

        # create admin and token
        admin_id = make_admin(app)
        token = get_token_for_user(app, admin_id, 'admin2@example.com')

    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    res = client.post(f'/api/admin/submissions/{sub_id}/grade', data=json.dumps({'score': 4.0, 'feedback': {'note': 'good'}}), headers=headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'success'

    with app.app_context():
        s = Submission.query.get(sub_id)
        assert s.score_earned == 4.0
        logs = AuditLog.query.filter_by(event_type='grade_changed', resource_type='submission', resource_id=sub_id).all()
        assert len(logs) >= 1
