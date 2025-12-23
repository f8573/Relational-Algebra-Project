"""Course model.

Defines the `Course` model and relationships to memberships and assessments.
"""

from app.extensions import db
from datetime import datetime


class Course(db.Model):
    __tablename__ = 'courses'
    """A course containing assessments and enrolled members.

    Fields include `title`, `term`, and publication status.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    term = db.Column(db.String(50))
    description = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship(
        'CourseMembership',
        back_populates='course',
        cascade='all, delete-orphan')
    assessments = db.relationship(
        'Assessment', back_populates='course', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Course {self.title}>'
