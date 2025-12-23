import os
import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def temp_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp('data')
    yield str(d)


@pytest.fixture(scope='function')
def app(temp_dir):
    # Create a Flask app configured for testing with a temporary sqlite file
    db_file = os.path.join(temp_dir, 'test_lms.db')
    cfg = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_file,
        'BANK_DB': os.path.join(temp_dir, 'bank.db')
    }

    app = create_app()
    app.config.update(cfg)

    # ensure bank.db populated with sample rows for testing
    from tests.fixtures.make_bank_db import create_bank_db as _create_db
    small_db = os.path.join(temp_dir, 'bank_small.db')
    edge_db = os.path.join(temp_dir, 'bank_edge.db')
    _create_db(small_db)
    _create_db(edge_db)

    # expose both DB paths to tests; primary BANK_DB kept for backward
    # compatibility
    app.config['BANK_DB'] = small_db
    app.config['BANK_DB_EDGE'] = edge_db

    # Create DB tables
    with app.app_context():
        _db.create_all()

    yield app

    # Teardown
    try:
        with app.app_context():
            _db.session.remove()
            _db.drop_all()
    except Exception:
        pass
    if os.path.exists(db_file):
        os.remove(db_file)
