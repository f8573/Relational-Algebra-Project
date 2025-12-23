"""Grading service: compare submissions against solution and testcases.

This module exposes `grade_submission(submission)` which runs the
student and solution queries for each `QuestionTestCase` and awards
partial credit via `QuestionMilestone` checks.
"""
from typing import Dict
from .execution import RAExecutor
from flask import current_app
from app.models.submission import Submission
from app.models.grading import QuestionTestCase, QuestionMilestone
from app.models.assessment import Question
from app.extensions import db
from app.models import DatabaseFile
import os


def _compare_results(a: str, b: str) -> bool:
    """Compare two execution outputs.

    Currently a simple stripped-text comparison; replace with a
    canonicalization/ordering-insensitive comparator if needed.
    """
    return a.strip() == b.strip()


def grade_submission(submission: Submission) -> Dict:
    """Grades a single Submission record and updates it with score/feedback.

    Returns a dict with results.
    """
    # Use Session.get for SQLAlchemy 1.x+ compatibility (no legacy
    # Query.get)
    question = db.session.get(Question, submission.question_id)
    if question is None:
        return {"error": "question not found"}

    testcases = QuestionTestCase.query.filter_by(question_id=question.id).all()
    executor = RAExecutor()

    # If the question has an explicit solution_query, prefer direct comparison
    if question.solution_query and str(question.solution_query).strip():
        # determine DB path: question.db_id -> uploaded DB file, else BANK_DB
        db_path = None
        if question.db_id:
            try:
                dbf = db.session.get(DatabaseFile, question.db_id)
                if dbf:
                    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
                    candidate = os.path.join(upload_dir, dbf.filename)
                    if os.path.exists(candidate):
                        db_path = candidate
            except Exception:
                current_app.logger.exception('Failed to resolve question database file')

        if not db_path:
            db_path = current_app.config.get('BANK_DB')

        executor.db_path = db_path

        # run solution and student queries
        sol_out, sol_err = executor.execute(question.solution_query or "")
        stu_out, stu_err = executor.execute(submission.student_query or "")

        feedback = []
        if sol_err:
            feedback.append({'error': f'solution error: {sol_err}'})
            submission.score_earned = 0.0
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': False}}

        if stu_err:
            feedback.append({'student_error': stu_err})
            submission.score_earned = 0.0
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': False}}

        if _compare_results(sol_out, stu_out):
            # full credit
            submission.score_earned = float(question.points or 0)
            feedback.append({'result': 'match', 'explanation': 'Student query matches solution_query'})
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': True}}
        # else fall through to testcase/milestone grading

    total_weight = sum((tc.weight or 1.0) for tc in testcases) or 1.0
    earned = 0.0
    feedback = []

    for tc in testcases:
        # Use testcase db_path if provided, otherwise fall back to
        # configured BANK_DB
        executor.db_path = tc.db_path or current_app.config.get('BANK_DB')

        # Run solution and student queries
        sol_out, sol_err = executor.execute(question.solution_query or "")
        stu_out, stu_err = executor.execute(submission.student_query or "")

        if sol_err:
            feedback.append({
                "tc": tc.id,
                "error": f"solution error: {sol_err}",
            })
            continue

        if stu_err:
            feedback.append({"tc": tc.id, "student_error": stu_err})
            # no credit for this testcase
            continue

        if _compare_results(sol_out, stu_out):
            earned += (tc.weight or 1.0)
            feedback.append({"tc": tc.id, "result": "pass"})
        else:
            # Check milestones for partial credit
            ms_score = 0.0
            for m in QuestionMilestone.query.filter_by(
                question_id=question.id
            ).all():
                # Run the milestone check query against the same DB
                chk_out, chk_err = executor.execute(m.check_query or "")
                if not chk_err and chk_out.strip():
                    ms_score += getattr(m, "points", 0)
            if ms_score:
                earned += ms_score
                feedback.append(
                    {
                        "tc": tc.id,
                        "result": "partial",
                        "milestone_points": ms_score,
                    }
                )
            else:
                feedback.append({"tc": tc.id, "result": "fail"})

    # Normalize score to question points
    score_fraction = earned / total_weight
    final_score = (question.points or 0) * score_fraction

    # Persist
    submission.score_earned = float(final_score)
    submission.grading_feedback = {"feedback": feedback}
    submission.last_updated = db.func.now()
    db.session.add(submission)
    db.session.commit()

    return {"score": submission.score_earned, "feedback": feedback}
