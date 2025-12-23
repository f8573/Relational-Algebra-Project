"""Run migrations (create missing tables) for development/testing.

This script runs `db.create_all()` to ensure new models (like `AuditLog`)
are created in the configured database. It's intended for local/dev use.
"""
from app import create_app
from app.extensions import db
import os


def main():
    app = create_app()
    # allow optional env-configured DB during script runs
    with app.app_context():
        db.create_all()
        print('Database tables created/updated (if missing).')


if __name__ == '__main__':
    main()
