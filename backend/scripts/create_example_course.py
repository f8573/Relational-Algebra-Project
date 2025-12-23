"""Create a small example course, assessment, and question for local testing.

Usage:
    python backend/scripts/create_example_course.py

This will create database tables (if missing) and insert a Course, an
Assessment, a Question, a TestCase pointing to `BANK_DB`, and a Milestone.
"""
import os
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.course import Course
from app.models.assessment import Assessment, Question
from app.models.grading import QuestionTestCase, QuestionMilestone


def main():
    app = create_app()
    with app.app_context():
        db.create_all()

        # sample admin
        if not User.query.filter_by(email='admin@university.edu').first():
            admin = User(
                email='admin@university.edu',
                name='System Admin',
                is_platform_admin=True,
            )
            db.session.add(admin)

        course = Course(title='Intro to Relational Algebra')
        db.session.add(course)

        assessment = Assessment(course=course, title='Quiz 1')
        db.session.add(assessment)

        question = Question(
            assessment=assessment,
            prompt='Return all names',
            points=10,
            solution_query='SOLUTION_Q',
        )
        db.session.add(question)

        bank_db = app.config.get('BANK_DB')
        if not bank_db:
            base = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    '..'))
            bank_db = os.path.join(base, 'bank.db')

        # ensure bank db exists as a placeholder
        open(bank_db, 'a').close()

        tc = QuestionTestCase(question=question, db_path=bank_db, weight=1.0)
        db.session.add(tc)

        m = QuestionMilestone(
            question=question,
            check_query='MILESTONE_CHECK',
            points=2)
        db.session.add(m)

        db.session.commit()

        print('Created example course, assessment, question, and testcase.')


if __name__ == '__main__':
    main()
