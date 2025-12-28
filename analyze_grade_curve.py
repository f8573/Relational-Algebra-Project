#!/usr/bin/env python
"""Grade curve analysis script - Analyze the loaded exam data.

This script provides utilities for analyzing the grade curve data that was
loaded from exam_grades.csv.
"""

import sqlite3
import statistics
from pathlib import Path

DB_PATH = Path(__file__).parent / 'backend' / 'lms.db'


def analyze_grades():
    """Analyze the loaded submission scores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all submission scores
    cursor.execute("""
        SELECT s.score_earned, q.id, q.points, u.email
        FROM submissions s
        JOIN questions q ON s.question_id = q.id
        JOIN attempts a ON s.attempt_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE u.email LIKE 'student%'
        ORDER BY a.user_id
    """)
    submissions = cursor.fetchall()
    
    # Calculate overall statistics
    scores = [row[0] for row in submissions]
    
    print("=" * 60)
    print("GRADE CURVE DATA ANALYSIS")
    print("=" * 60)
    print(f"\nTotal Submissions: {len(scores)}")
    print(f"Min Score: {min(scores):.2f}")
    print(f"Max Score: {max(scores):.2f}")
    print(f"Mean Score: {statistics.mean(scores):.2f}")
    print(f"Median Score: {statistics.median(scores):.2f}")
    print(f"Std Dev: {statistics.stdev(scores):.2f}")
    
    # Score distribution
    print("\n" + "=" * 60)
    print("SCORE DISTRIBUTION")
    print("=" * 60)
    
    bins = [0, 2, 4, 6, 8, 10]
    bin_labels = ["0-2", "2-4", "4-6", "6-8", "8-10"]
    bin_counts = [0] * len(bin_labels)
    
    for score in scores:
        for i, (lower, upper) in enumerate(zip(bins[:-1], bins[1:])):
            if lower <= score < upper:
                bin_counts[i] += 1
            elif score == 10:  # Handle the upper bound
                bin_counts[-1] += 1
    
    for label, count in zip(bin_labels, bin_counts):
        pct = (count / len(scores)) * 100
        bar = '█' * int(pct / 2)
        print(f"  {label:>5}: {count:>4} ({pct:>5.1f}%) {bar}")
    
    # Per-question analysis
    print("\n" + "=" * 60)
    print("PER-QUESTION ANALYSIS")
    print("=" * 60)
    
    cursor.execute("""
        SELECT q.id, q.points, AVG(s.score_earned) as avg_score,
               MIN(s.score_earned) as min_score, MAX(s.score_earned) as max_score,
               COUNT(s.id) as count
        FROM submissions s
        JOIN questions q ON s.question_id = q.id
        GROUP BY q.id
        ORDER BY q.id
    """)
    
    for q_id, points, avg_score, min_score, max_score, count in cursor.fetchall():
        pct = (avg_score / points) * 100
        print(f"\nQuestion {q_id} ({points} points)")
        print(f"  Count: {count}")
        print(f"  Average: {avg_score:.2f} / {points} ({pct:.1f}%)")
        print(f"  Range: {min_score:.2f} - {max_score:.2f}")
    
    # Student performance
    print("\n" + "=" * 60)
    print("TOP 10 STUDENTS (by average score)")
    print("=" * 60)
    
    cursor.execute("""
        SELECT u.email, AVG(s.score_earned) as avg_score, 
               MIN(s.score_earned) as min_score, MAX(s.score_earned) as max_score,
               COUNT(s.id) as submissions
        FROM submissions s
        JOIN attempts a ON s.attempt_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE u.email LIKE 'student%'
        GROUP BY u.id
        ORDER BY avg_score DESC
        LIMIT 10
    """)
    
    print(f"\n{'Email':<25} {'Avg Score':<12} {'Min-Max':<15} {'Count':<8}")
    print("-" * 60)
    for email, avg_score, min_score, max_score, count in cursor.fetchall():
        print(f"{email:<25} {avg_score:>8.2f}/10  {min_score:>5.2f}-{max_score:>5.2f}     {count:>3}")
    
    # Bottom 10 students
    print("\n" + "=" * 60)
    print("BOTTOM 10 STUDENTS (by average score)")
    print("=" * 60)
    
    cursor.execute("""
        SELECT u.email, AVG(s.score_earned) as avg_score,
               MIN(s.score_earned) as min_score, MAX(s.score_earned) as max_score,
               COUNT(s.id) as submissions
        FROM submissions s
        JOIN attempts a ON s.attempt_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE u.email LIKE 'student%'
        GROUP BY u.id
        ORDER BY avg_score ASC
        LIMIT 10
    """)
    
    print(f"\n{'Email':<25} {'Avg Score':<12} {'Min-Max':<15} {'Count':<8}")
    print("-" * 60)
    for email, avg_score, min_score, max_score, count in cursor.fetchall():
        print(f"{email:<25} {avg_score:>8.2f}/10  {min_score:>5.2f}-{max_score:>5.2f}     {count:>3}")
    
    print("\n" + "=" * 60 + "\n")
    conn.close()


if __name__ == '__main__':
    analyze_grades()
