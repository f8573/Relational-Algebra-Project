import pytest

from app.extensions import db
from app.models.user import User
from app.models.course import Course
from app.models.assessment import Assessment, Question
from app.models.submission import Attempt, Submission

from app.services import grading


def _fake_execute_factory(solution_out_map):
    def fake_execute(self, raw_query):
        return solution_out_map.get(raw_query, ('', None))

    return fake_execute


def test_ra_partial_credit(app, monkeypatch):
    with app.app_context():
        user = User(email='student2@example.com', name='Student2')
        db.session.add(user)

        course = Course(title='RA Partial')
        db.session.add(course)

        assessment = Assessment(course=course, title='RA quiz')
        db.session.add(assessment)

        question = Question(
            assessment=assessment,
            prompt='Return pairs',
            points=10,
            solution_query='SOLUTION_Q',
        )
        db.session.add(question)
        db.session.commit()

        attempt = Attempt(user_id=user.id, assessment_id=assessment.id)
        db.session.add(attempt)
        db.session.commit()

        # Setup mapping for fake RAExecutor outputs
        # Solution prints header 'a | b' then rows; student flips column order
        mapping = {
            'SOLUTION_Q': ('a | b\n1 | 2\n3 | 4\n', None),
            'STUDENT_PARTIAL': ('b | a\n2 | 1\n4 | 3\n', None),
            'STUDENT_DIFF': ('a | b\n1 | 99\n3 | 4\n', None),
        }

        from app.services import execution as ex_mod
        monkeypatch.setattr(ex_mod.RAExecutor, 'execute', _fake_execute_factory(mapping))

        # Partial-match submission
        sub_partial = Submission(
            attempt_id=attempt.id,
            question_id=question.id,
            student_query='STUDENT_PARTIAL',
        )
        db.session.add(sub_partial)
        db.session.commit()

        res = grading.grade_submission(sub_partial)
        # partial credit fraction is 0.5 by policy
        assert res['score'] == pytest.approx(5.0)

        # Different submission should not get full/partial credit
        sub_diff = Submission(
            attempt_id=attempt.id,
            question_id=question.id,
            student_query='STUDENT_DIFF',
        )
        db.session.add(sub_diff)
        db.session.commit()

        res2 = grading.grade_submission(sub_diff)
        assert res2['score'] == pytest.approx(0.0)
