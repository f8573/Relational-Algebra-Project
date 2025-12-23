# Contributing

Thank you for contributing to the Relational Algebra LMS project! A few tips to get started:

- Code style: run `flake8` against the `backend/` directory.
- Tests: use `pytest` and the `backend/tests` directory. Tests run with PYTHONPATH=backend.
- To add a sample course locally, run:

```bash
python backend/scripts/create_example_course.py
```

- CI: a GitHub Actions workflow runs linting and tests on push/PRs (see `.github/workflows/ci.yml`).

If you're unsure, open an issue describing your planned changes and request guidance.
