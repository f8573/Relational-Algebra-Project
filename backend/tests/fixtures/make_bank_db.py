"""Helper to create test bank.db files for pytest fixtures."""
import sqlite3
import os


def create_bank_db(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
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
