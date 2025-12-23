import pytest

from app.extensions import db
from app.models.user import User
from app.models.course import Course
from app.models.assessment import Assessment, Question
from app.models.grading import QuestionTestCase, QuestionMilestone
from app.models.submission import Attempt, Submission

from app.services import grading


def _fake_execute_factory(solution_out_map):
    """Return a fake execute(self, raw_query) function.

    `solution_out_map` is a dict mapping raw_query -> (output, err)
    """

    def fake_execute(self, raw_query):
        return solution_out_map.get(raw_query, ('', None))

    return fake_execute


def test_grade_full_and_partial(app, monkeypatch):
    # Setup sample data
    with app.app_context():
        user = User(email='student@example.com', name='Student')
        db.session.add(user)

        course = Course(title='Intro RA')
        db.session.add(course)

        assessment = Assessment(course=course, title='Quiz 1')
        db.session.add(assessment)

        question = Question(
            assessment=assessment,
            prompt='Compute R',
            points=10,
            solution_query='SOLUTION_Q',
        )
        db.session.add(question)

        # Two testcases pointing to different fixture DBs
        tc1 = QuestionTestCase(
            question=question,
            db_path=app.config['BANK_DB'],
            weight=1.0,
        )
        tc2 = QuestionTestCase(
            question=question,
            db_path=app.config['BANK_DB_EDGE'],
            weight=2.0,
        )
        db.session.add_all([tc1, tc2])

        # Milestone gives 2 points for a matching check_query
        m = QuestionMilestone(
            question=question,
            check_query='MILESTONE_CHECK',
            points=2,
        )
        db.session.add(m)

        db.session.commit()

        # Create attempt + submission that matches solution
        attempt = Attempt(
            user_id=user.id,
            assessment_id=assessment.id,
        )
        db.session.add(attempt)
        db.session.commit()

        sub_match = Submission(
            attempt_id=attempt.id,
            question_id=question.id,
            student_query='STUDENT_MATCH',
        )
        db.session.add(sub_match)
        db.session.commit()

        # Patch RAExecutor.execute to return same output for solution and
        # student when matching
        mapping = {
            'SOLUTION_Q': ('ROWS', None),
            'STUDENT_MATCH': ('ROWS', None),
            'STUDENT_FAIL': ('DIFF', None),
            'MILESTONE_CHECK': ('OK', None),
        }

        from app.services import execution as ex_mod
        monkeypatch.setattr(
            ex_mod.RAExecutor, 'execute', _fake_execute_factory(mapping)
        )

        # Grade matching submission -> full credit
        res1 = grading.grade_submission(sub_match)
        assert res1['score'] == pytest.approx(10.0)

        # Now failing student submission but gets milestone partial credit
        sub_fail = Submission(
            attempt_id=attempt.id,
            question_id=question.id,
            student_query='STUDENT_FAIL',
        )
        db.session.add(sub_fail)
        db.session.commit()

        res2 = grading.grade_submission(sub_fail)
        # Milestone points added: mapping gives 'OK' for milestone -> 2 points
        assert res2['score'] > 0
