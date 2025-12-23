"""Create a sample `bank.db` SQLite file with a small table and rows.

Usage:
    python backend/scripts/create_bank_db.py /path/to/bank.db
If no path is given, writes to backend/bank.db next to this script.
"""
import os
import sqlite3
import sys


def create_bank_db(path: str):
    dirp = os.path.dirname(path)
    if dirp and not os.path.exists(dirp):
        os.makedirs(dirp, exist_ok=True)

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # Simple table R with some rows
    cur.execute(
        'CREATE TABLE IF NOT EXISTS R (a INTEGER, b INTEGER, name TEXT)'
    )
    cur.execute('DELETE FROM R')
    cur.executemany(
        'INSERT INTO R (a,b,name) VALUES (?,?,?)',
        [
            (1, 2, 'alice'),
            (2, 3, 'bob'),
            (3, 4, 'carol'),
        ],
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        out = sys.argv[1]
    else:
        out = os.path.join(os.path.dirname(__file__), '..', 'bank.db')
    out = os.path.abspath(out)
    create_bank_db(out)
    print('Created bank DB at:', out)
