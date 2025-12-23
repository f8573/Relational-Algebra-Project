#!/usr/bin/env python
"""Create test users with passwords for the LMS.

This script creates sample users that can be used for testing the login
and course assessment flows.
"""

import sys
import os

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.extensions import db
from app.models import User, Course, CourseMembership
from app import create_app


def create_test_users():
    """Create test users and enroll them in courses."""
    app = create_app()

    with app.app_context():
        # Clear existing test users
        User.query.filter(User.email.in_([
            'admin@university.edu',
            'instructor@university.edu',
            'student@university.edu'
        ])).delete()
        db.session.commit()

        # Create admin user
        admin = User(
            email='admin@university.edu',
            name='Platform Administrator',
            is_platform_admin=True
        )
        admin.set_password('admin-password-123')
        db.session.add(admin)

        # Create instructor user
        instructor = User(
            email='instructor@university.edu',
            name='Dr. Jane Smith'
        )
        instructor.set_password('instructor-password-456')
        db.session.add(instructor)

        # Create student user
        student = User(
            email='student@university.edu',
            name='John Doe'
        )
        student.set_password('student-password-789')
        db.session.add(student)

        db.session.commit()

        # Get or create the sample course
        course = Course.query.filter_by(title='Intro to Relational Algebra').first()
        if not course:
            print("Course not found. Run create_example_course.py first.")
            return

        # Enroll instructor as instructor
        membership_inst = CourseMembership(
            course_id=course.id,
            user_id=instructor.id,
            role='instructor'
        )
        db.session.add(membership_inst)

        # Enroll student as student
        membership_std = CourseMembership(
            course_id=course.id,
            user_id=student.id,
            role='student'
        )
        db.session.add(membership_std)

        db.session.commit()

        print("✓ Created test users:")
        print("  - admin@university.edu (password: admin-password-123)")
        print("  - instructor@university.edu (password: instructor-password-456)")
        print("  - student@university.edu (password: student-password-789)")
        print("\n✓ Enrolled users in 'Intro to Relational Algebra' course")


if __name__ == '__main__':
    create_test_users()
