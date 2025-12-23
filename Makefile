PY=python

.PHONY: init-bank create-example test lint

init-bank:
	$(PY) backend/scripts/create_bank_db.py backend/bank.db

create-example:
	$(PY) backend/scripts/create_example_course.py

test:
	PYTHONPATH=backend $(PY) -m pytest backend/tests

lint:
	flake8 backend
