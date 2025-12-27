"""Add grading curve columns to assessments table if missing.

Run from repo root:
    python backend/scripts/add_assessment_curve_columns.py
"""
import os
import sys
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(HERE, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
from app.config import Config

db_uri = Config.SQLALCHEMY_DATABASE_URI
if not db_uri.startswith('sqlite:///'):
    raise SystemExit('Only sqlite supported by this script')

db_path = db_uri.replace('sqlite:///', '')
print('Using DB:', db_path)
if not os.path.exists(db_path):
    raise SystemExit('DB not found')

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("PRAGMA table_info('assessments')")
cols = [r[1] for r in cur.fetchall()]
added = False
if 'curve_enabled' not in cols:
    print('Adding curve_enabled...')
    cur.execute("ALTER TABLE assessments ADD COLUMN curve_enabled BOOLEAN DEFAULT 0")
    added = True
if 'curve_alpha' not in cols:
    print('Adding curve_alpha...')
    cur.execute("ALTER TABLE assessments ADD COLUMN curve_alpha FLOAT DEFAULT 5.0")
    added = True
if 'curve_beta' not in cols:
    print('Adding curve_beta...')
    cur.execute("ALTER TABLE assessments ADD COLUMN curve_beta FLOAT DEFAULT 2.0")
    added = True
if 'curve_target_median' not in cols:
    print('Adding curve_target_median...')
    cur.execute("ALTER TABLE assessments ADD COLUMN curve_target_median FLOAT DEFAULT 0.75")
    added = True
if added:
    conn.commit()
    print('Columns added.')
else:
    print('Columns already present.')
conn.close()
print('Done.')
