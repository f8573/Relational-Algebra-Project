#!/usr/bin/env python
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'lms.db'

def ensure_column():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(course_memberships)")
    cols = [r[1] for r in cur.fetchall()]
    print('Existing columns:', cols)
    if 'permissions_override' not in cols:
        print('Adding column permissions_override (TEXT)')
        cur.execute("ALTER TABLE course_memberships ADD COLUMN permissions_override TEXT")
        con.commit()
        print('Added column')
    else:
        print('Column already present')
    con.close()

if __name__ == '__main__':
    ensure_column()
