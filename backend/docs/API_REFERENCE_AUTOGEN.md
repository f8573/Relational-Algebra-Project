# Auto-generated API Reference

This file is generated from the docstrings in `app/api` and `app/services`.

## Module: app\api\__init__.py

API blueprint registration.

### Function: `register_api(app)`

Register api sub-blueprints on the Flask app.

This will attach each module's `bp` Blueprint under an appropriate URL
prefix (e.g. `/api/run`, `/api/auth`, etc.).

## Module: app\api\assessments.py

Assessment-related routes (simplified).

### Function: `list_assessments()` — routes: / [GET]

Return a short list of assessment ids.

This is a lightweight helper used by the frontend to fetch a paged
list of assessments. It returns only ids for simplicity.

### Function: `submit_answer()` — routes: /submit [POST]

## Module: app\api\auth.py

Auth routes (placeholders).

### Function: `login()` — routes: /login [POST]

## Module: app\api\courses.py

Course-related routes (placeholders).

### Function: `list_courses()` — routes: / [GET]

## Module: app\api\run.py

### Function: `run_query()` — routes: / [POST]

## Module: app\services\__init__.py

Services package initialization.

Keep service implementations here (no Flask app code in this package).

## Module: app\services\execution.py

RA execution utilities.

Provides `RAExecutor` — helper to parse and execute RA scripts.
Uses the bundled `radb` engine. Each call creates a fresh execution
context to isolate runs and capture stdout.

### Class: `RAExecutor`

- `__init__(db_path)`
  - Create an executor bound to a particular database.
- `_load_defaults()`
  - Load radb default function signatures from the packaged `sys.ini`.
- `_clean_query(raw_query)`
  - Pre-process frontend RA input to remove common artifacts.
- `_parse_full_script(script_text)`
  - Parse a script containing one or more RA statements and return ASTs.
- `execute(raw_query)`
  - Execute a relational-algebra script and capture its output.

## Module: app\services\grading.py

Grading service: compare submissions against solution and testcases.

This module exposes `grade_submission(submission)` which runs the
student and solution queries for each `QuestionTestCase` and awards
partial credit via `QuestionMilestone` checks.

### Function: `_compare_results(a, b)`

Compare two execution outputs.

Currently a simple stripped-text comparison; replace with a
canonicalization/ordering-insensitive comparator if needed.

### Function: `grade_submission(submission)`

Grades a single Submission record and updates it with score/feedback.

Returns a dict with results.

## Module: app\services\grading_engine.py

Legacy grading engine shim (kept for compatibility).

This module is deprecated. The active grading implementation lives in
`app.services.grading`.
Importing `GradingEngine` from here will emit a DeprecationWarning and
delegate to `app.services.grading.grade_submission`.

### Class: `GradingEngine`

- `__init__()`
- `grade_submission(*args, **kwargs)`

## Module: app\services\permissions.py

Permissions and whitelist checks.

This module contains small helpers used by views to authorize actions.

### Function: `can_manage_course(user, course)`
