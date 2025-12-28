#!/usr/bin/env python
"""Load exam grade data to create submissions for grade curve analysis.

Uses raw SQL to avoid Flask app initialization issues and database locks.
"""

import csv
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash


def load_grade_curve_data():
    """Load exam grades and create student submissions using raw SQL."""
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'lms.db')
    conn = sqlite3.connect(db_path, timeout=30)
    conn.isolation_level = None  # Autocommit mode
    cursor = conn.cursor()
    
    try:
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        
        # Get target course
        cursor.execute("SELECT id, title FROM courses WHERE id=1")
        course = cursor.fetchone()
        if not course:
            print("ERROR: Course with id=1 not found.")
            return
        
        course_id, course_title = course
        print(f"Target course: {course_title} (id={course_id})")
        
        # Get assessment
        cursor.execute("SELECT id, title FROM assessments WHERE id=1")
        assessment = cursor.fetchone()
        if not assessment:
            print("ERROR: Assessment with id=1 not found.")
            return
        
        assessment_id, assessment_title = assessment
        print(f"Assessment: {assessment_title} (id={assessment_id})")
        
        # Get questions
        cursor.execute("""
            SELECT id, points FROM questions 
            WHERE assessment_id=1 
            ORDER BY id
        """)
        questions = cursor.fetchall()
        if not questions:
            print("ERROR: No questions found for assessment 1.")
            return
        
        print(f"Questions ({len(questions)}): {[f'Q{q[0]}({q[1]}pts)' for q in questions]}")
        
        # Read exam grades CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'exam_grades.csv')
        
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            print(f"ERROR: Could not read CSV file: {e}")
            return
        
        print(f"\nLoaded {len(rows)} exam records")
        
        # Track stats
        users_created = 0
        enrollments_created = 0
        attempts_created = 0
        submissions_created = 0
        batch_size = 50
        now = datetime.utcnow().isoformat()
        
        # Process each exam record
        for i, row in enumerate(rows, 1):
            try:
                exam2_score = float(row['exam2'])
            except (ValueError, KeyError):
                continue
            
            # Create user if not exists
            email = f"student{i}@university.edu"
            cursor.execute("SELECT id FROM users WHERE email=?", (email,))
            user_result = cursor.fetchone()
            
            if not user_result:
                password_hash = generate_password_hash(f"password{i}")
                cursor.execute("""
                    INSERT INTO users (email, name, is_platform_admin, password_hash, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (email, f"Student {i}", False, password_hash, now))
                user_id = cursor.lastrowid
                users_created += 1
            else:
                user_id = user_result[0]
            
            # Enroll in course if not exists
            cursor.execute("""
                SELECT id FROM course_memberships 
                WHERE course_id=? AND user_id=?
            """, (course_id, user_id))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO course_memberships (course_id, user_id, role)
                    VALUES (?, ?, ?)
                """, (course_id, user_id, 'student'))
                enrollments_created += 1
            
            # Create or get attempt
            cursor.execute("""
                SELECT id FROM attempts 
                WHERE user_id=? AND assessment_id=?
            """, (user_id, assessment_id))
            
            attempt_result = cursor.fetchone()
            if attempt_result:
                attempt_id = attempt_result[0]
            else:
                cursor.execute("""
                    INSERT INTO attempts (user_id, assessment_id, started_at, submitted_at, total_score)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, assessment_id, now, now, 0.0))
                attempt_id = cursor.lastrowid
                attempts_created += 1
            
            # Create submissions for each question
            for question_id, points in questions:
                # Check if submission exists
                cursor.execute("""
                    SELECT id FROM submissions 
                    WHERE attempt_id=? AND question_id=?
                """, (attempt_id, question_id))
                
                if not cursor.fetchone():
                    # Scale exam2 score to question points
                    score_earned = (exam2_score / 100.0) * points
                    
                    cursor.execute("""
                        INSERT INTO submissions (attempt_id, question_id, score_earned, last_updated)
                        VALUES (?, ?, ?, ?)
                    """, (attempt_id, question_id, score_earned, now))
                    submissions_created += 1
            
            # Log progress
            if i % batch_size == 0:
                print(f"  ✓ Processed {i}/{len(rows)} records...")
        
        # Final commit (explicit since we're in autocommit mode, but good for clarity)
        conn.commit()
        print(f"\n✓ Successfully loaded grade curve data:")
        print(f"  - Users created: {users_created}")
        print(f"  - Enrollments created: {enrollments_created}")
        print(f"  - Attempts created: {attempts_created}")
        print(f"  - Submissions created: {submissions_created}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    load_grade_curve_data()
