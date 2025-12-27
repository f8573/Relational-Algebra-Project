"""One-off script: add `submission_limit` column to `questions` table and set existing rows to 0.

Run from repository root:
    python backend/scripts/add_submission_limit_column.py
"""
import os
import sys
import sqlite3
# Ensure backend package is importable when running this script from repo root
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
BACKEND_DIR = os.path.abspath(os.path.join(HERE, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
from app.config import Config

# Determine DB path from config
db_uri = Config.SQLALCHEMY_DATABASE_URI
if db_uri.startswith('sqlite:///'):
    db_path = db_uri.replace('sqlite:///', '')
else:
    raise SystemExit('Only sqlite DBs supported by this script. DB URI: %s' % db_uri)

print('Using DB:', db_path)
if not os.path.exists(db_path):
    raise SystemExit('Database file not found: %s' % db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check if column exists
cur.execute("PRAGMA table_info('questions')")
cols = [r[1] for r in cur.fetchall()]
if 'submission_limit' in cols:
    print('Column submission_limit already exists. Ensuring values are non-null...')
    cur.execute("UPDATE questions SET submission_limit = 0 WHERE submission_limit IS NULL")
    conn.commit()
    print('Update complete.')
else:
    print('Adding column submission_limit...')
    try:
        cur.execute("ALTER TABLE questions ADD COLUMN submission_limit INTEGER DEFAULT 0")
        conn.commit()
        print('Column added.')
    except Exception as e:
        print('ALTER TABLE failed:', e)
        # As a fallback, create a new table and copy data (complex), but for now exit
        conn.close()
        raise
    # Ensure existing rows have 0
    cur.execute("UPDATE questions SET submission_limit = 0 WHERE submission_limit IS NULL")
    conn.commit()
    print('Set existing rows to 0.')

conn.close()
print('Done.')
