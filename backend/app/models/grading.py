"""Grading support models.

Defines `QuestionTestCase` and `QuestionMilestone` used by the grading
service to run test-case queries and award partial-credit milestones.
"""

from app.extensions import db


class QuestionTestCase(db.Model):
    __tablename__ = 'question_test_cases'
    """A test-case for a `Question` executed against a specific DB.

    `db_path` points to the fixture database used for this testcase.
    """

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey('questions.id'), nullable=False
    )

    db_path = db.Column(
        db.String(500), nullable=False
    )
    is_visible = db.Column(db.Boolean, default=True)
    weight = db.Column(db.Float, default=1.0)

    question = db.relationship('Question', back_populates='test_cases')


class QuestionMilestone(db.Model):
    __tablename__ = 'question_milestones'
    """A milestone check that can award partial credit for a question.

    `check_query` is executed and non-empty output indicates the milestone
    passed.
    """

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey('questions.id'), nullable=False
    )

    description = db.Column(db.String(200))
    check_query = db.Column(
        db.Text, nullable=False
    )
    points = db.Column(db.Integer, default=0)

    question = db.relationship('Question', back_populates='milestones')
