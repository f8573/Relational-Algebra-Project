"""User models.

Defines `User` and `CourseMembership` SQLAlchemy models used to manage
users and their roles within courses.
"""

from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    """A platform user.

    Attributes:
        id: Primary key.
        email: Unique user email used for login/identification.
        name: Human-readable name.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    avatar_url = db.Column(db.String(255))
    is_platform_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    memberships = db.relationship(
        'CourseMembership',
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


class CourseMembership(db.Model):
    __tablename__ = 'course_memberships'
    """Association object linking `User` to `Course` with a role."""

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id'),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    # 'instructor', 'ta', 'student'
    role = db.Column(db.String(20), nullable=False)
    permissions_override = db.Column(db.JSON, default={})
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='memberships')
    course = db.relationship('Course', back_populates='members')
