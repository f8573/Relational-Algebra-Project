"""Attach `bank.db` as a test case to an assessment under the example course.

Usage:
    python backend/scripts/attach_bank_to_assignment.py

This script finds the course titled 'Intro to Relational Algebra' (or the first course)
and creates an Assessment, a Question, and a QuestionTestCase using the configured
`BANK_DB` path.
"""
from app import create_app
from app.extensions import db
from app.models.course import Course
from app.models.assessment import Assessment, Question
from app.models.grading import QuestionTestCase
import os


def main():
    app = create_app()
    with app.app_context():
        course = Course.query.filter_by(title='Intro to Relational Algebra').first()
        if not course:
            course = Course.query.first()
            if not course:
                print('No course found; aborting. Please create a course first.')
                return
            print(f"Falling back to first course: {course.title} (id={course.id})")

        assessment = Assessment(course=course, title='Bank DB Assignment')
        db.session.add(assessment)

        question = Question(
            assessment=assessment,
            prompt='Use the bank DB to list all account holders',
            points=10,
            solution_query='SELECT name FROM customers;'
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

        db.session.commit()

        print('Attached bank.db to course:', course.title)
        print('Assessment id:', assessment.id)
        print('Question id:', question.id)
        print('TestCase id:', tc.id)


if __name__ == '__main__':
    main()
