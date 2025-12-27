import sqlite3, os, json
db_path = os.path.join(os.path.dirname(__file__), '..', 'lms.db')
print('DB', db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# get questions for assessment 1
cur.execute('SELECT id, points FROM questions WHERE assessment_id = ?', (1,))
qs = {row[0]: row[1] for row in cur.fetchall()}
print('Questions:', qs)
# get submissions joined with attempts for user 1 assessment 1
cur.execute('SELECT s.id, s.question_id, s.score_earned, s.last_updated FROM submissions s JOIN attempts a ON s.attempt_id = a.id WHERE a.user_id = ? AND a.assessment_id = ?', (1,1))
rows = cur.fetchall()
print('Raw submissions count', len(rows))
# pick latest per question by last_updated
import datetime
latest = {}
for r in rows:
    sid, qid, score, last = r
    # last may be string
    key = int(qid)
    t = last
nrows = []
# use SQL to get latest per question
for qid in qs.keys():
    cur.execute('''SELECT s.score_earned, s.last_updated FROM submissions s JOIN attempts a ON s.attempt_id=a.id WHERE a.user_id=? AND a.assessment_id=? AND s.question_id=? ORDER BY s.last_updated DESC LIMIT 1''', (1,1,qid))
    row = cur.fetchone()
    if row:
        print('Q', qid, 'points', qs[qid], 'score', row[0], 'last', row[1])
    else:
        print('Q', qid, 'no submission')
conn.close()
