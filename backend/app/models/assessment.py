"""Assessment and question models.

Contains `Assessment` and `Question` which represent an assignment/quiz
and its constituent questions, including solution query storage.
"""

from app.extensions import db


class Assessment(db.Model):
    __tablename__ = 'assessments'
    """Represents an assessment (assignment, quiz, or exam).

    Stores scheduling and configuration metadata and related questions.
    """

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer, db.ForeignKey('courses.id'), nullable=False
    )
    type = db.Column(
        db.String(20), nullable=False, default='assignment'
    )
    # possible values: 'assignment', 'quiz', 'exam'
    title = db.Column(
        db.String(200), nullable=False
    )
    description = db.Column(db.Text)

    opens_at = db.Column(db.DateTime)
    closes_at = db.Column(db.DateTime)
    exam_mode = db.Column(db.Boolean, default=False)
    time_limit_minutes = db.Column(db.Integer, nullable=True)
    max_attempts = db.Column(db.Integer, nullable=True)

    course = db.relationship('Course', back_populates='assessments')
    questions = db.relationship(
        'Question',
        back_populates='assessment',
        order_by='Question.order_index',
        cascade='all, delete-orphan',
    )
    attempts = db.relationship(
        'Attempt',
        back_populates='assessment',
        cascade='all, delete-orphan',
    )


class Question(db.Model):
    __tablename__ = 'questions'
    """A single question within an `Assessment`.

    Contains `prompt`, `solution_query`, and point values.
    """

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey('assessments.id'),
        nullable=False)

    prompt = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=10)
    extra_credit_points = db.Column(db.Integer, default=0)
    order_index = db.Column(db.Integer, default=0)
    solution_query = db.Column(db.Text, nullable=True)
    db_id = db.Column(db.Integer, db.ForeignKey('databases.id'), nullable=True)

    # New: support multiple question types beyond RA query
    # 'ra' (default), 'mcq' (multiple choice), 'msq' (multi-select),
    # 'free' (free response), 'norm' (normalization theory)
    question_type = db.Column(db.String(10), nullable=False, default='ra')
    # Store choices/options and grading keys as JSON for non-RA types
    options_json = db.Column(db.JSON, default={})
    answer_key_json = db.Column(db.JSON, default={})
    # Submission limit: 0 = unlimited, >0 = max submissions allowed
    submission_limit = db.Column(db.Integer, default=0)

    database = db.relationship('DatabaseFile')

    assessment = db.relationship('Assessment', back_populates='questions')
    test_cases = db.relationship(
        'QuestionTestCase',
        back_populates='question',
        cascade='all, delete-orphan',
    )

    milestones = db.relationship(
        'QuestionMilestone',
        back_populates='question',
        cascade='all, delete-orphan',
    )
