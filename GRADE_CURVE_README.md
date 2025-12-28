# Grade Curve Builder

## Overview

The Grade Curve Builder is a tool for loading historical exam data into the Relational Algebra Project's LMS for analysis and grade curve calibration. It converts exam scores from a CSV file into submission records within the course database.

## What Was Created

### Data Loaded
- **233 student records** with unique email addresses (student1@university.edu through student233@university.edu)
- **233 course enrollments** for testCourse (id=1)
- **233 assessment attempts** for Introduction to Relational Algebra (id=1)
- **1,398 submission records** (6 questions × 233 students)

### Score Conversion
The exam2 column from `exam_grades.csv` was converted to submission scores:

```
submission_score = (exam2_score / 100) × question_points

Example:
- Exam2 score: 84.5 out of 100
- Question points: 10
- Result: (84.5 / 100) × 10 = 8.45 earned points
```

### Grade Distribution
```
Score Range    Count   Percentage   Visualization
0-2            0       0.0%         
2-4            12      0.9%         
4-6            246     17.6%        ████████
6-8            654     46.8%        ███████████████████████
8-10           486     34.8%        █████████████████
```

**Statistical Summary:**
- Average: 7.26 / 10 (72.6%)
- Median: 7.40
- Std Dev: 1.38
- Range: 3.80 - 9.95

## Key Features

### 1. Mass User Creation
Each exam record creates a new student account with:
- Email: `student{N}@university.edu` (N = 1 to 233)
- Password: `password{N}` (for testing)
- Role: Student

### 2. Automatic Enrollment
All students are automatically enrolled in the target course as 'student' role.

### 3. Proportional Score Scaling
Exam scores are scaled proportionally to accommodate questions of varying point values. This allows the same exam data to be used with different question configurations.

### 4. Complete Assessment Records
For each student, a complete attempt record is created with:
- One submission per question
- Timestamps for tracking
- Calculated scores ready for analysis

## Files Included

### Scripts
1. **load_grade_curve_init.py** (in `backend/scripts/`)
   - Complete initialization and loading script
   - Creates database schema from scratch
   - Sets up course, assessment, and questions
   - Loads all exam data
   - Handles all database locking issues

2. **analyze_grade_curve.py** (in project root)
   - Analyzes loaded submission data
   - Shows distribution statistics
   - Ranks students by performance
   - Analyzes per-question statistics

### Documentation
- **GRADE_CURVE_DATA_SUMMARY.md** - Detailed summary of loaded data
- **README.md** (this file) - Usage instructions

## Using the Loaded Data

### View in Web Interface
1. Start the backend: `python backend/wsgi.py`
2. Login: admin@university.edu / admin-password-123
3. Navigate to testCourse
4. View Assessment 1 and student submissions

### Analyze Programmatically
Run the analysis script:
```bash
python analyze_grade_curve.py
```

Or query directly:
```python
import sqlite3

conn = sqlite3.connect('backend/lms.db')
cursor = conn.cursor()

# Get all submission scores
cursor.execute('''
    SELECT s.score_earned, q.id, u.email
    FROM submissions s
    JOIN questions q ON s.question_id = q.id
    JOIN attempts a ON s.attempt_id = a.id
    JOIN users u ON a.user_id = u.id
    WHERE u.email LIKE 'student%'
''')

for score, question_id, email in cursor.fetchall():
    print(f"{email} scored {score:.2f} on Q{question_id}")
```

### Grade Curve Analysis
The loaded data is ready for grade curve analysis:
- **233 samples** provides good statistical power
- **6 repeated measures** per student enables analysis
- **Wide score range** (3.8-9.95) captures full distribution

You can:
1. Fit distribution curves (normal, skewed, etc.)
2. Calculate optimal curve parameters
3. Test different curving algorithms
4. Compare to historical performance

## Student Access

Any student can login with:
- Email: `student{N}@university.edu` (1-233)
- Password: `password{N}` (same number)

Example:
- Email: student42@university.edu
- Password: password42

Students will see:
- Their enrollment in testCourse
- Their submission scores for each question
- Performance metrics

## Database Details

### Location
`backend/lms.db` (SQLite database)

### Tables Involved
- **users** - 233 new student accounts
- **course_memberships** - 233 enrollments
- **attempts** - 233 assessment attempts
- **submissions** - 1,398 submission records

### Accessing Directly
```bash
# Open database with sqlite3
sqlite3 backend/lms.db

# Query examples
SELECT COUNT(*) FROM users;
SELECT AVG(score_earned) FROM submissions;
SELECT * FROM submissions WHERE question_id=1;
```

## Troubleshooting

### Database Locked Errors
If you encounter "database is locked" errors:
1. Make sure no other Python processes are running
2. The load script handles this automatically with timeouts
3. If needed, remove `backend/lms.db*` files and reload

### Student Not Seeing Submissions
1. Verify student is enrolled in course
2. Check that attempt and submission records exist
3. Ensure assessment is not restricted by dates

### Score Values Seem Wrong
Verify the calculation:
- Exam2 score out of 100
- Multiply by question.points / 100
- Check that question.points = 10 in database

## Advanced Usage

### Reloading Data
To reload with fresh data:
```bash
rm backend/lms.db*
python backend/scripts/load_grade_curve_init.py
```

### Custom Exam Scores
Modify `exam_grades.csv` before loading, or edit the load script to use a different source file.

### Different Question Point Values
Edit the load script to assign different points:
```python
# In load_grade_curve_init.py, change the INSERT statement:
cursor.execute(f"""
    INSERT INTO questions (id, assessment_id, prompt, points, order_index)
    VALUES (?, 1, 'Question {q_id}', 20, {q_id - 1})  # Changed to 20 points
""")
```

## Questions?

For more information about:
- **Grade curves**: See Assessment settings in the LMS
- **Database schema**: See `backend/app/models/`
- **Score calculations**: See `analyze_grade_curve.py` or `load_grade_curve_init.py`
