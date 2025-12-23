# Local Development (DEV)

This file describes common local development tasks for the Relational-Algebra-LMS backend.

Prereqs
- Python 3.10+ recommended
- Create and activate a virtual environment at repository root (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # (on Windows: .venv\\Scripts\\activate)
```

Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

Create the sample bank DB (used for query execution)

```bash
make init-bank
# or direct
python backend/scripts/create_bank_db.py backend/bank.db
```

Create an example course (populates `lms.db` with a sample course/assessment)

```bash
make create-example
```

Run tests

```bash
make test
```

Lint

```bash
make lint
```

Useful notes
- Tests run with `PYTHONPATH=backend` so the `app` package is importable.
- Use `python backend/wsgi.py` to run the development server (it uses the app factory).
