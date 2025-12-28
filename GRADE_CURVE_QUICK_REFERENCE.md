# Grade Curve Builder - Quick Reference

## 📊 What's Loaded

| Metric | Count |
|--------|-------|
| Students | 233 |
| Course Enrollments | 233 |
| Assessment Attempts | 233 |
| Submissions | 1,398 |
| Average Score | 7.26/10 |
| Score Range | 3.80-9.95 |

## 🚀 Get Started (30 seconds)

```bash
# Start the Flask server
python backend/wsgi.py

# In another terminal, analyze the data
python analyze_grade_curve.py
```

## 👤 Login Credentials

**Admin Account:**
- Email: `admin@university.edu`
- Password: `admin-password-123`

**Any Student Account:**
- Email: `student{N}@university.edu` (N = 1-233)
- Password: `password{N}`

Example:
- Email: `student42@university.edu`
- Password: `password42`

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/scripts/load_grade_curve_init.py` | Load the data (already done) |
| `analyze_grade_curve.py` | Analyze scores and statistics |
| `backend/lms.db` | Database with all data |
| `GRADE_CURVE_README.md` | Detailed usage guide |
| `GRADE_CURVE_FINAL_REPORT.md` | Complete technical report |

## 📈 Quick Analysis

```bash
python analyze_grade_curve.py
```

Output includes:
- Overall statistics (min, max, mean, std dev)
- Score distribution (histogram)
- Per-question analysis
- Top 10 students
- Bottom 10 students

## 🔍 Quick Database Queries

```bash
# SQLite command line
sqlite3 backend/lms.db

# Count records
SELECT COUNT(*) FROM users WHERE email LIKE 'student%';
SELECT COUNT(*) FROM submissions;
SELECT AVG(score_earned) FROM submissions;

# Get student data
SELECT email, COUNT(*) as submissions, AVG(score_earned) as avg_score
FROM submissions s
JOIN attempts a ON s.attempt_id = a.id
JOIN users u ON a.user_id = u.id
WHERE u.email = 'student1@university.edu'
GROUP BY u.id;
```

## 🧮 Score Scaling Formula

```
submission_score = (exam2_score / 100) × question_points

Example:
- Exam2 score: 84.5
- Question points: 10
- Result: (84.5 / 100) × 10 = 8.45
```

## 📊 Score Distribution

```
Excellent (8-10):  486 students (34.8%)  [█████████]
Good (6-8):        654 students (46.8%)  [██████████████]
Fair (4-6):        246 students (17.6%)  [█████]
Poor (2-4):         12 students (0.9%)   
```

## ✅ Verification

```bash
# Check data was loaded
python -c "
import sqlite3
conn = sqlite3.connect('backend/lms.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM submissions')
print(f'Submissions loaded: {c.fetchone()[0]}')
"
# Output: Submissions loaded: 1398
```

## 🎯 Common Tasks

### View All Student Submissions
```bash
sqlite3 backend/lms.db << EOF
SELECT u.email, COUNT(*) as count, AVG(s.score_earned) as avg
FROM submissions s
JOIN attempts a ON s.attempt_id = a.id
JOIN users u ON a.user_id = u.id
WHERE u.email LIKE 'student%'
GROUP BY u.id
ORDER BY avg DESC
LIMIT 20;
EOF
```

### Export Scores to CSV
```bash
sqlite3 backend/lms.db << EOF
.headers on
.mode csv
SELECT u.email, q.id as question_id, s.score_earned
FROM submissions s
JOIN questions q ON s.question_id = q.id
JOIN attempts a ON s.attempt_id = a.id
JOIN users u ON a.user_id = u.id
WHERE u.email LIKE 'student%'
ORDER BY u.email, q.id;
EOF > scores.csv
```

### Calculate Statistics
```bash
sqlite3 backend/lms.db << EOF
SELECT
  COUNT(*) as total_submissions,
  AVG(score_earned) as mean_score,
  MIN(score_earned) as min_score,
  MAX(score_earned) as max_score,
  ROUND(AVG(score_earned), 2) as avg_rounded
FROM submissions;
EOF
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database locked | Kill Python, remove `lms.db-*`, reload |
| Can't see students | Check course_memberships table |
| Scores wrong | Verify exam2 values and 10-point questions |
| App won't start | Check port 5000 is available |

## 📚 Documentation

- **Quick Start**: This file (you are here)
- **Full Guide**: `GRADE_CURVE_README.md`
- **Data Summary**: `GRADE_CURVE_DATA_SUMMARY.md`
- **Technical Details**: `GRADE_CURVE_FINAL_REPORT.md`
- **Implementation**: `GRADE_CURVE_IMPLEMENTATION.md`

## 💡 Pro Tips

1. **Batch Operations** - The load script uses batches of 50 for efficiency
2. **WAL Mode** - Database uses WAL for better concurrency
3. **Timestamps** - All records have creation timestamps
4. **Referential Integrity** - All foreign keys are enforced
5. **Password Hashing** - Werkzeug hashes all student passwords securely

## 📞 Support

For questions about:
- **Data format**: See `GRADE_CURVE_README.md`
- **Statistics**: See `analyze_grade_curve.py` or output
- **Database schema**: See `backend/app/models/`
- **Technical details**: See `GRADE_CURVE_FINAL_REPORT.md`

---

**Status**: ✅ Ready to use  
**Data Loaded**: 233 students, 1,398 submissions  
**Last Updated**: December 27, 2025
