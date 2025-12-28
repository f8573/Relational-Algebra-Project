#!/usr/bin/env python
"""Load exam grade data to create submissions for grade curve analysis.

This script reads exam_grades.csv and creates:
1. A new user for each score (student1@university.edu, student2@university.edu, etc.)
2. Enrolls each student in the testCourse (course_id=1)
3. Creates an attempt and submissions for each assessment/question
4. Sets scores scaled to the question point value

For example: exam2 score of 84.5 out of 100
- For a 10-point question: (84.5/100) * 10 = 8.45 points earned
- For a 5-point question: (84.5/100) * 5 = 4.225 points earned
"""

import sys
import os
import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import models directly
from app.models import User, Course, CourseMembership, Assessment, Question, Attempt, Submission

# Setup database connection directly
db_path = os.path.join(os.path.dirname(__file__), '..', 'lms.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={'timeout': 30, 'check_same_thread': False})
Session = sessionmaker(bind=engine)


def load_grade_curve_data():
    """Load exam grades and create student submissions."""
    session = Session()
    
    try:
        # Get the target course
        course = session.query(Course).filter_by(id=1).first()
        if not course:
            print("ERROR: Course with id=1 not found. Create it first.")
            return
        
        print(f"Target course: {course.title} (id={course.id})")
        
        # Get the assessment and its questions
        assessment = session.query(Assessment).filter_by(id=1).first()
        if not assessment:
            print("ERROR: Assessment with id=1 not found.")
            return
        
        questions = session.query(Question).filter_by(assessment_id=1).order_by(Question.id).all()
        if not questions:
            print("ERROR: No questions found for assessment 1.")
            return
        
        print(f"Assessment: {assessment.title} (id={assessment.id})")
        print(f"Questions ({len(questions)}): {[f'Q{q.id}({q.points}pts)' for q in questions]}")
        
        # Read exam grades CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'exam_grades.csv')
        
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            print(f"ERROR: Could not read CSV file: {e}")
            return
        
        print(f"\nLoaded {len(rows)} exam records from {csv_path}")
        
        # Track stats
        users_created = 0
        enrollments_created = 0
        attempts_created = 0
        submissions_created = 0
        batch_size = 50
        
        # Process each exam record
        for i, row in enumerate(rows, 1):
            try:
                exam2_score = float(row['exam2'])
            except (ValueError, KeyError):
                print(f"Row {i}: Skipping - invalid exam2 score")
                continue
            
            # Create user
            email = f"student{i}@university.edu"
            user = session.query(User).filter_by(email=email).first()
            
            if not user:
                user = User(
                    email=email,
                    name=f"Student {i}",
                    is_platform_admin=False
                )
                user.set_password(f"password{i}")
                session.add(user)
                session.flush()  # Get the user ID without committing
                users_created += 1
            
            # Enroll in course
            existing_membership = session.query(CourseMembership).filter_by(
                course_id=course.id,
                user_id=user.id
            ).first()
            
            if not existing_membership:
                membership = CourseMembership(
                    course_id=course.id,
                    user_id=user.id,
                    role='student'
                )
                session.add(membership)
                enrollments_created += 1
            
            session.flush()
            
            # Create or get attempt
            attempt = session.query(Attempt).filter_by(
                user_id=user.id,
                assessment_id=assessment.id
            ).first()
            
            if not attempt:
                attempt = Attempt(
                    user_id=user.id,
                    assessment_id=assessment.id,
                    started_at=datetime.utcnow(),
                    submitted_at=datetime.utcnow()
                )
                session.add(attempt)
                session.flush()
                attempts_created += 1
            
            # Create submissions for each question
            for question in questions:
                # Check if submission already exists
                existing_submission = session.query(Submission).filter_by(
                    attempt_id=attempt.id,
                    question_id=question.id
                ).first()
                
                if not existing_submission:
                    # Scale exam2 score to question points
                    # exam2_score is out of 100, scale to question.points
                    score_earned = (exam2_score / 100.0) * question.points
                    
                    submission = Submission(
                        attempt_id=attempt.id,
                        question_id=question.id,
                        score_earned=score_earned,
                        last_updated=datetime.utcnow()
                    )
                    session.add(submission)
                    submissions_created += 1
            
            # Batch commit every N records
            if i % batch_size == 0:
                try:
                    session.commit()
                    print(f"  ✓ Processed {i}/{len(rows)} records... (committed)")
                except Exception as e:
                    print(f"  ERROR at batch {i}: {e}")
                    session.rollback()
                    return
        
        # Final commit
        try:
            session.commit()
            print(f"\n✓ Successfully loaded grade curve data:")
            print(f"  - Users created: {users_created}")
            print(f"  - Enrollments created: {enrollments_created}")
            print(f"  - Attempts created: {attempts_created}")
            print(f"  - Submissions created: {submissions_created}")
        except Exception as e:
            print(f"ERROR: Failed to commit final batch: {e}")
            session.rollback()
            return
    finally:
        session.close()


if __name__ == '__main__':
    load_grade_curve_data()
