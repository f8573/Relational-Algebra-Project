# API Reference — Backend (services, API endpoints & models)

This document provides a concise reference for the backend HTTP endpoints
and the core services/models they interact with. It is intended for
frontend developers and integrators who need to call the API.

**Base URL**: the app registers blueprints under their module names; in
a deployed environment these are mounted at `/api/<blueprint>` by
convention (e.g., `/api/run`, `/api/assessments`).

**Contents**
- **Services**: short summaries of key service classes used by endpoints
- **Endpoints**: per-route signatures, payloads, responses and examples
- **Models**: concise field/purpose list for core persistence objects

## Services

- `app.services.execution.RAExecutor`
  - Purpose: parse and execute relational-algebra scripts using the
    bundled `radb` engine.
  - Key methods:
    - `RAExecutor(db_path='bank.db')`: constructor; `db_path` may be a
      filesystem `.db` path or a SQLAlchemy URL.
    - `execute(raw_query) -> (output: str, error: Optional[str])`: run an
      RA script and return captured stdout and an optional error string.
  - Notes: performs small frontend cleanup and creates a fresh `radb`
    context per execution to avoid shared state.

- `app.services.grading.grade_submission(submission)`
  - Purpose: grade a `Submission` record by executing the question's
    `solution_query` and the student's `student_query` against configured
    `QuestionTestCase` DB fixtures, awarding milestone partial credit.
  - Behavior: updates `submission.score_earned`, `submission.grading_feedback`,
    and `submission.last_updated` and commits to the DB.

## HTTP Endpoints (expanded)

Note: All endpoints return JSON. Error conditions typically return a
non-2xx status code or a JSON object with an `error` field.

**Run Query**
- Path: `/` (blueprint `run`) — mounted commonly at `/api/run/`
- Method: `POST`
- Description: execute a relational-algebra script and return captured
  stdout or an error message.
- Request JSON:

```json
{"query": "<relational algebra script>"}
```
- Success response (200):

```json
{"status": "success", "output": "...captured stdout..."}
```
- Error response (200 with error body or non-200):

```json
{"status": "error", "error": "error message", "partial_output": "..."}
```
- Notes: the executor uses the configured `BANK_DB` or a testcase's
  `db_path` when grading. Empty `query` returns 400 with `{"error": "Empty query"}`.

**List Assessments**
- Path: `/` (blueprint `assessments`) — commonly `/api/assessments/`
- Method: `GET`
- Description: returns a lightweight list of assessment ids (paged,
  limited to 50 currently).
- Success response (200):

```json
[1, 2, 3]
```

**Submit Answer**
- Path: `/submit` (blueprint `assessments`)
- Method: `POST`
- Description: create or find an `Attempt`, persist a `Submission`, and
  synchronously grade it (returns grading result).
- Request JSON (example):

```json
{
  "user_id": 42,
  "assessment_id": 7,
  "question_id": 13,
  "query": "R \u22c3 S;"
}
```
- Success response (200):

```json
{
  "status": "graded",
  "result": {"score": 8.5, "feedback": [...]}
}
```
- Edge cases:
  - If the `question` cannot be found the grading service returns
    `{"error": "question not found"}` inside the `result` object.
  - Student or solution execution errors are captured in `feedback` and
    the submission receives no credit for those testcases.

**Auth (placeholder)**
- Path: `/login` (blueprint `auth`)
- Method: `POST`
- Description: currently a placeholder; returns `{"status": "not-implemented"}`.

**Courses (placeholder)**
- Path: `/` (blueprint `courses`)
- Method: `GET`
- Description: placeholder returning an empty list `[]`.

## Models (summary)

All models use `app.extensions.db` (SQLAlchemy). Below are the core
entities referenced by the API.

- `User`: `id`, `email`, `name`, `avatar_url`, `is_platform_admin`, `created_at`.
- `Course`: `id`, `title`, `term`, `description`, `is_published`, `created_at`.
- `CourseMembership`: association linking `User` and `Course` with a `role`.
- `Assessment`: `id`, `course_id`, `type`, `title`, `opens_at`, `closes_at`, `exam_mode`, etc.; relations: `questions`, `attempts`.
- `Question`: `id`, `assessment_id`, `prompt`, `points`, `solution_query`, `order_index`; relations: `test_cases`, `milestones`.
- `QuestionTestCase`: `id`, `question_id`, `db_path`, `weight` — points to a DB fixture to run solution and student queries against.
- `QuestionMilestone`: partial-credit checks that run a `check_query` and award `points` when satisfied.
- `Attempt`: groups multiple `Submission` objects for a student's attempt at an assessment.
- `Submission`: `id`, `attempt_id`, `question_id`, `student_query`, `score_earned`, `grading_feedback`, `last_updated`.

## Examples / Integration Notes

- Client should POST JSON and handle both `status: success` and `status: error` responses from the run endpoint.
- Submissions are graded synchronously — for heavy workloads consider
  converting `grade_submission` to an async task and returning a job id.

## Type-checking & Linting Notes

- `mypy` currently reports `db.Model` as undefined due to SQLAlchemy's
  dynamic base. Two non-suppressive approaches improve results:
  1. Add a small typing alias in `app/extensions.py` (e.g., `from typing import Any; db: Any = SQLAlchemy()`), which helps mypy reason about `db` without hiding other errors.
  2. Add a focused `mypy.ini` to configure per-module options for SQLAlchemy models.

---

If you want, I can now:
- add per-endpoint curl examples and sample payloads, or
- convert this into an auto-generated reference by extracting docstrings
  programmatically from `app/api` and `app/services`.
