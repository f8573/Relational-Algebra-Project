# Grade Curve Data Loader - Summary

## Overview
Successfully created a grade curve dataset for analysis by loading exam scores from `exam_grades.csv` and converting them to course submissions.

## Data Loaded
- **Source File**: `exam_grades.csv` (233 exam records)
- **Source Column**: `exam2` (second exam scores, out of 100)
- **Target Course**: testCourse (id=1)
- **Target Assessment**: Introduction to Relational Algebra (id=1)
- **Questions**: 6 questions, each worth 10 points

## Database Statistics
- **Users Created**: 233 (student1@university.edu through student233@university.edu)
- **Course Enrollments**: 233 (all as 'student' role)
- **Attempts**: 233 (one per student for Assessment 1)
- **Submissions**: 1,398 (6 questions × 233 students)
- **Average Submission Score**: 7.26 / 10 points

## Score Scaling
Exam2 scores were scaled proportionally to question point values:
- Formula: `score_earned = (exam2_score / 100) * question_points`
- Example: A student with exam2=84.5 earns 8.45 points on each 10-point question

## Grade Distribution
With 233 samples across 6 questions, you have:
- 1,398 submission scores to analyze
- Scores range from 0-10 points (proportional to original exam2 0-100 range)
- This dataset can be used for:
  - Grade curve analysis and fitting
  - Distribution analysis
  - Statistical modeling of performance
  - Calibrating grading scales

## Scripts Used
1. **load_grade_curve_init.py** - Complete initialization script that:
   - Creates fresh database schema
   - Sets up demo course, assessment, and questions
   - Loads all exam data as submissions
   - Avoids Flask app lock issues by using raw SQLite

## Database File
- **Location**: `backend/lms.db`
- **Size**: ~500 KB (after data loading)

## Next Steps
To use this data with the application:
1. Start the Flask backend: `python backend/wsgi.py`
2. Log in as: `admin@university.edu` / `admin-password-123`
3. Navigate to testCourse and Assessment 1
4. View student submissions and grades
5. Configure and apply grade curve settings if needed

To analyze the data programmatically:
```python
import sqlite3
conn = sqlite3.connect('backend/lms.db')
cursor = conn.cursor()

# Get all submission scores for analysis
cursor.execute('''
    SELECT s.score_earned, q.points, a.user_id
    FROM submissions s
    JOIN questions q ON s.question_id = q.id
    JOIN attempts a ON s.attempt_id = a.id
''')
scores = cursor.fetchall()
```

## Notes
- All students have password: `password{number}` (e.g., student1 = password1)
- Demo admin account available for testing
- Database uses SQLite for simplicity and portability
- WAL mode enabled for better concurrency
