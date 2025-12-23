"""Legacy grading engine shim (kept for compatibility).

This module is deprecated. The active grading implementation lives in
`app.services.grading`.
Importing `GradingEngine` from here will emit a DeprecationWarning and
delegate to `app.services.grading.grade_submission`.
"""
import warnings

from app.services.grading import grade_submission


class GradingEngine:
    def __init__(self):
        warnings.warn(
            "GradingEngine is deprecated; use "
            "app.services.grading.grade_submission",
            DeprecationWarning,
        )

    def grade_submission(self, *args, **kwargs):
        return grade_submission(*args, **kwargs)
