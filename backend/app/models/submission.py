"""Attempt and submission models.

`Attempt` groups a student's run at an assessment, and `Submission`
stores a student's query for a specific question plus grading results.
"""

from app.extensions import db
from datetime import datetime


class Attempt(db.Model):
    __tablename__ = 'attempts'
    """An attempt by a `User` at completing an `Assessment`.

    Tracks timing and total score for the attempt.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey('assessments.id'),
        nullable=False)

    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    total_score = db.Column(db.Float, default=0.0)

    assessment = db.relationship('Assessment', back_populates='attempts')
    user = db.relationship('User')
    submissions = db.relationship(
        'Submission', back_populates='attempt', cascade='all, delete-orphan'
    )


class Submission(db.Model):
    __tablename__ = 'submissions'
    """A student's submission for a single `Question`.

    Stores the submitted RA query and grading results/feedback.
    """

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(
        db.Integer, db.ForeignKey('attempts.id'), nullable=False
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey('questions.id'), nullable=False
    )

    student_query = db.Column(db.Text)
    # For non-RA question types, store structured answer payload
    # e.g., { choice: 'A' } for mcq, { choices: ['A','C'] } for msq,
    # { text: '...' } for free, { normal_form: 'BCNF' } for norm
    answer_payload = db.Column(db.JSON, default={})
    score_earned = db.Column(db.Float, default=0.0)
    grading_feedback = db.Column(db.JSON, default={})
    last_updated = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    attempt = db.relationship('Attempt', back_populates='submissions')
    question = db.relationship('Question')
