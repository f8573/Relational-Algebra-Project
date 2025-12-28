#!/usr/bin/env python
"""Initialize database and load exam grade data.

Creates the database schema from scratch, then loads exam grades as submissions.
"""

import csv
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'lms.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'exam_grades.csv')


def init_database():
    """Create database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(120) UNIQUE NOT NULL,
                name VARCHAR(120),
                avatar_url VARCHAR(255),
                is_platform_admin BOOLEAN DEFAULT 0,
                password_hash VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                term VARCHAR(50),
                description TEXT,
                is_published BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role VARCHAR(50) DEFAULT 'student',
                FOREIGN KEY (course_id) REFERENCES courses(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                type VARCHAR(20) DEFAULT 'assignment',
                title VARCHAR(200) NOT NULL,
                description TEXT,
                opens_at DATETIME,
                closes_at DATETIME,
                exam_mode BOOLEAN DEFAULT 0,
                time_limit_minutes INTEGER,
                max_attempts INTEGER,
                curve_enabled BOOLEAN DEFAULT 0,
                curve_alpha REAL DEFAULT 5.0,
                curve_beta REAL DEFAULT 2.0,
                curve_target_median REAL DEFAULT 0.75,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                prompt TEXT NOT NULL,
                points INTEGER DEFAULT 10,
                extra_credit_points INTEGER DEFAULT 0,
                order_index INTEGER DEFAULT 0,
                solution_query TEXT,
                db_id INTEGER,
                question_type VARCHAR(10) DEFAULT 'ra',
                options_json JSON,
                answer_key_json JSON,
                submission_limit INTEGER DEFAULT 0,
                FOREIGN KEY (assessment_id) REFERENCES assessments(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                assessment_id INTEGER NOT NULL,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                submitted_at DATETIME,
                expires_at DATETIME,
                total_score REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (assessment_id) REFERENCES assessments(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                student_query TEXT,
                answer_payload JSON DEFAULT '{}',
                score_earned REAL DEFAULT 0.0,
                grading_feedback JSON DEFAULT '{}',
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attempt_id) REFERENCES attempts(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        """)
        
        conn.commit()
        print("✓ Database schema created")
        
    finally:
        conn.close()


def create_demo_course():
    """Create the demo course, assessment, and questions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        now = datetime.utcnow().isoformat()
        
        # Create course
        cursor.execute("""
            INSERT OR IGNORE INTO courses (id, title, term, description, is_published, created_at)
            VALUES (1, 'testCourse', 'Fall 2025', 'Test course for grade curves', 1, ?)
        """, (now,))
        
        # Create assessment
        cursor.execute("""
            INSERT OR IGNORE INTO assessments (id, course_id, type, title, description, curve_enabled)
            VALUES (1, 1, 'assignment', 'Introduction to Relational Algebra', 'Assignment 1', 0)
        """)
        
        # Create 6 questions (10 points each)
        for q_id in range(1, 7):
            cursor.execute(f"""
                INSERT OR IGNORE INTO questions (id, assessment_id, prompt, points, order_index, question_type)
                VALUES (?, 1, 'Question {q_id}', 10, {q_id - 1}, 'ra')
            """, (q_id,))
        
        conn.commit()
        print("✓ Demo course, assessment, and questions created")
        
    finally:
        conn.close()


def load_grade_curve_data():
    """Load exam grades and create student submissions."""
    
    conn = sqlite3.connect(DB_PATH, timeout=30)
    cursor = conn.cursor()
    
    try:
        # Read exam grades CSV
        try:
            with open(CSV_PATH, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            print(f"ERROR: Could not read CSV file: {e}")
            return
        
        print(f"\nLoaded {len(rows)} exam records")
        
        now = datetime.utcnow().isoformat()
        
        # Get questions info
        cursor.execute("SELECT id, points FROM questions WHERE assessment_id=1 ORDER BY id")
        questions = cursor.fetchall()
        
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
                WHERE course_id=1 AND user_id=?
            """, (user_id,))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO course_memberships (course_id, user_id, role)
                    VALUES (1, ?, 'student')
                """, (user_id,))
                enrollments_created += 1
            
            # Create or get attempt
            cursor.execute("""
                SELECT id FROM attempts 
                WHERE user_id=? AND assessment_id=1
            """, (user_id,))
            
            attempt_result = cursor.fetchone()
            if attempt_result:
                attempt_id = attempt_result[0]
            else:
                cursor.execute("""
                    INSERT INTO attempts (user_id, assessment_id, started_at, submitted_at, total_score)
                    VALUES (?, 1, ?, ?, 0.0)
                """, (user_id, now, now))
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
        
        conn.commit()
        print(f"\n✓ Successfully loaded grade curve data:")
        print(f"  - Users created: {users_created}")
        print(f"  - Enrollments created: {enrollments_created}")
        print(f"  - Attempts created: {attempts_created}")
        print(f"  - Submissions created: {submissions_created}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    # Remove old database
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Removed old database file")
        except:
            pass
    
    # Also remove WAL and journal files
    for suffix in ['-wal', '-shm', '-journal']:
        f = DB_PATH + suffix
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass
    
    print("Initializing database...")
    init_database()
    create_demo_course()
    load_grade_curve_data()
