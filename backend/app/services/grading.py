"""Grading service: compare submissions against solution and testcases.

This module exposes `grade_submission(submission)` which runs the
student and solution queries for each `QuestionTestCase` and awards
partial credit via `QuestionMilestone` checks.
"""
from typing import Dict, List, Set, Tuple
import json
from .execution import RAExecutor
from flask import current_app
from app.models.submission import Submission
from app.models.grading import QuestionTestCase, QuestionMilestone
from app.models.assessment import Question
from app.extensions import db
from app.models import DatabaseFile
import os


def _compare_results(a: str, b: str) -> bool:
    """Compare two execution outputs.

    Currently a simple stripped-text comparison; replace with a
    canonicalization/ordering-insensitive comparator if needed.
    """
    return a.strip() == b.strip()


def _ensure_json(val):
    try:
        if isinstance(val, (dict, list)):
            return val
        if isinstance(val, str) and val.strip():
            return json.loads(val)
    except Exception:
        pass
    return {}


def _canonicalize_decomposition(decomp: List[List[str]]) -> List[List[str]]:
    try:
        rels = []
        for r in decomp:
            # normalize to list of unique strings
            rr = sorted(list(dict.fromkeys([str(x).strip() for x in r if str(x).strip()])))
            if rr:
                rels.append(rr)
        # sort relations lexicographically by joined name
        rels.sort(key=lambda a: ",".join(a))
        return rels
    except Exception:
        return []


def _signature_of_decomposition(decomp: List[List[str]]) -> str:
    rels = _canonicalize_decomposition(decomp)
    return " | ".join(["{" + ",".join(r) + "}" for r in rels])


def _closure(attrs: Set[str], fds: List[Tuple[Set[str], Set[str]]]) -> Set[str]:
    res = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(res) and not rhs.issubset(res):
                res |= rhs
                changed = True
    return res


def _candidate_keys(attrs: List[str], fds: List[Tuple[Set[str], Set[str]]]) -> List[Set[str]]:
    # Brute force minimal keys (ok for small relations)
    n = len(attrs)
    attr_list = list(attrs)
    keys: List[Set[str]] = []
    for r in range(1, n + 1):
        idx = list(range(r))
        while True:
            subset = {attr_list[i] for i in idx}
            clos = _closure(subset, fds)
            if clos.issuperset(attr_list):
                # minimality
                if not any(k.issubset(subset) for k in keys):
                    keys.append(subset)
            # next comb
            i = r - 1
            while i >= 0 and idx[i] == i + n - r:
                i -= 1
            if i < 0:
                break
            idx[i] += 1
            for j in range(i + 1, r):
                idx[j] = idx[j - 1] + 1
        if keys:
            break
    return keys or [set(attr_list)]


def _project_fds(relation: Set[str], fds: List[Tuple[Set[str], Set[str]]]) -> List[Tuple[Set[str], Set[str]]]:
    return [(lhs, rhs) for lhs, rhs in fds if lhs.issubset(relation) and rhs.issubset(relation)]


def _parse_relations_from_text(text: str) -> List[Set[str]]:
    """Parse relations from text format like:
    R_1(A,B)
    R_2(B,C,D)
    Returns list of sets of attributes.
    """
    rels = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Match R_x(A,B,C) or relation(A,B,C) pattern
        import re
        match = re.search(r'\(([^)]+)\)', line)
        if match:
            attrs_str = match.group(1)
            attrs = set(str(a).strip() for a in attrs_str.split(',') if str(a).strip())
            if attrs:
                rels.append(attrs)
    return rels


def _nf_level(relation: Set[str], fds: List[Tuple[Set[str], Set[str]]]) -> str:
    """Returns the highest normal form level for a relation: BCNF, 4NF, 5NF (or lower)
    
    Note: 4NF and 5NF require multivalued dependencies (MVDs) and join dependencies (JDs)
    which are typically not provided in basic FD-based problems. Without explicit MVDs/JDs,
    we conservatively return BCNF as the maximum level since we cannot determine 4NF/5NF.
    
    For full 4NF/5NF support, students would need to specify MVDs and JDs in the schema.
    """
    projected = _project_fds(relation, fds)
    keys = _candidate_keys(list(relation), projected)
    prime_attrs = set().union(*keys) if keys else set()

    # BCNF check: for every non-trivial FD X -> Y, X must be a superkey
    for lhs, rhs in projected:
        if not rhs or rhs == relation:  # skip trivial FDs
            continue
        clos = _closure(lhs, projected)
        if not clos.issuperset(relation):
            # lhs is not a superkey; relation is not BCNF
            # Check if it's 3NF (allow if RHS is all prime attributes)
            if not rhs.issubset(prime_attrs):
                # 2NF check: partial dependency on composite key
                for key in keys:
                    if len(key) > 1 and lhs.issubset(key) and not key.issubset(lhs) and not rhs.issubset(prime_attrs):
                        return '1NF' if len(lhs) == 0 else '2NF'
                return '2NF' if len(lhs) < len(relation) else '3NF'
            else:
                return '3NF'
    
    # If we reach here, relation is BCNF
    # 4NF and 5NF would require explicit MVDs and JDs in the schema, which are not currently supported
    # Return BCNF as the highest determinable level
    return 'BCNF'


def _normalize_sql_result(result_str: str) -> List[Tuple]:
    """Parse SQL result string into list of tuples (rows), with column order normalized.
    
    Expects format like:
      column1,column2,column3
      value1,value2,value3
      value4,value5,value6
    
    Returns sorted list of tuples for comparison.
    """
    if not result_str or not isinstance(result_str, str):
        return []
    
    lines = result_str.strip().split('\n')
    if len(lines) < 2:
        return []
    
    try:
        headers = [h.strip() for h in lines[0].split(',')]
        rows = []
        for line in lines[1:]:
            if not line.strip():
                continue
            values = [v.strip() for v in line.split(',')]
            # Create tuple of (header, value) pairs, then sort by header
            row_dict = dict(zip(headers, values))
            # Sort by header to normalize column order
            sorted_row = tuple(row_dict[h] for h in sorted(headers))
            rows.append(sorted_row)
        # Sort rows to normalize row order
        rows.sort()
        return rows
    except Exception:
        return []


def _compare_sql_results(student_result: str, expected_result: str) -> Tuple[str, float]:
    """Compare SQL results with grading logic:
    - Full credit (1.0): exact same tuples in exact same order
    - Partial credit (0.5): same rows (in same order), columns can be reordered
    - No credit (0.0): different rows or out of order
    
    Returns (grade_type, fraction) where grade_type is 'full', 'partial', or 'none'
    """
    if not student_result or not expected_result:
        return ('none', 0.0)
    
    student_lines = student_result.strip().split('\n')
    expected_lines = expected_result.strip().split('\n')
    
    if len(student_lines) < 2 or len(expected_lines) < 2:
        return ('none', 0.0)
    
    try:
        # Parse headers and rows
        student_headers = [h.strip() for h in student_lines[0].split(',')]
        expected_headers = [h.strip() for h in expected_lines[0].split(',')]
        
        student_rows = []
        for line in student_lines[1:]:
            if not line.strip():
                continue
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(student_headers):
                student_rows.append(values)
        
        expected_rows = []
        for line in expected_lines[1:]:
            if not line.strip():
                continue
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(expected_headers):
                expected_rows.append(values)
        
        # Check if same number of rows
        if len(student_rows) != len(expected_rows):
            return ('none', 0.0)
        
        # Check exact match (full credit)
        if student_headers == expected_headers:
            if student_rows == expected_rows:
                return ('full', 1.0)
        
        # Check partial match: same rows, possibly different column order
        # Create normalized row format for comparison
        student_normalized = []
        for row in student_rows:
            row_dict = dict(zip(student_headers, row))
            # Create tuple of values sorted by header name
            normalized = tuple(row_dict.get(h, '') for h in sorted(student_headers))
            student_normalized.append(normalized)
        
        expected_normalized = []
        for row in expected_rows:
            row_dict = dict(zip(expected_headers, row))
            # Create tuple of values sorted by header name
            normalized = tuple(row_dict.get(h, '') for h in sorted(expected_headers))
            expected_normalized.append(normalized)
        
        # Check if rows are the same (regardless of column order)
        # Both should have same set of normalized rows in same order
        if student_normalized == expected_normalized:
            return ('partial', 0.5)
        
        return ('none', 0.0)
    except Exception:
        return ('none', 0.0)

def grade_submission(submission: Submission) -> Dict:
    """Grades a single Submission record and updates it with score/feedback.

    Returns a dict with results.
    """
    # Use Session.get for SQLAlchemy 1.x+ compatibility (no legacy
    # Query.get)
    question = db.session.get(Question, submission.question_id)
    if question is None:
        return {"error": "question not found"}

    # Branch by question type
    qtype = (question.question_type or 'ra').lower()
    if qtype != 'ra':
        key = _ensure_json(question.answer_key_json)
        ans = _ensure_json(submission.answer_payload)
        feedback = []

        def _ok():
            submission.score_earned = float(question.points or 0)
            submission.grading_feedback = {"feedback": feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {"score": submission.score_earned, "feedback": feedback}

        def _fail(msg=None):
            submission.score_earned = 0.0
            if msg:
                feedback.append({"note": msg})
            submission.grading_feedback = {"feedback": feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {"score": submission.score_earned, "feedback": feedback}

        try:
            if qtype == 'mcq':
                # Expect shapes:
                # key: {"correct": "A"} or {"correct": "A) Option"}
                # ans: {"selected": "A"} or {"selected": "A) Option"} or {"choice": "A"}
                k = key.get('correct', key.get('correct_index'))
                a = ans.get('selected', ans.get('choice', ans.get('index')))
                
                if k is None or a is None:
                    return _fail('missing answer or key')
                
                # Normalize both by extracting identifiers (e.g., "A" from "A) Option")
                def normalize_choice(s):
                    s = str(s).strip()
                    # Extract first token before ')' or space
                    import re
                    match = re.match(r'^([A-Za-z0-9]+)', s)
                    if match:
                        return match.group(1).upper()
                    return s.upper()
                
                k_norm = normalize_choice(k)
                a_norm = normalize_choice(a)
                
                if k_norm == a_norm:
                    feedback.append({"result": "match"})
                    return _ok()
                return _fail('incorrect')

            if qtype == 'msq':
                # key: {"correct": ["A","C"]} or {"correct": ["A) Option 1", "C) Option 3"]}
                # ans: {"selected": ["A","C"]} or {"selected": ["A) Option 1", "C) Option 3"]}
                kc = key.get('correct') or []
                ac = ans.get('selected') or []
                
                # Normalize both by extracting identifiers (e.g., "A" from "A) Option")
                def normalize_choice(s):
                    s = str(s).strip()
                    # Extract first token before ')' or space
                    import re
                    match = re.match(r'^([A-Za-z0-9]+)', s)
                    if match:
                        return match.group(1).upper()
                    return s.upper()
                
                ks = set(normalize_choice(x) for x in kc)
                as_ = set(normalize_choice(x) for x in ac)
                
                if not ks:
                    return _fail('missing key')
                if ks == as_:
                    feedback.append({"result": "match"})
                    return _ok()
                # simple partial credit: intersection fraction
                inter = len(ks & as_)
                if inter:
                    frac = inter / float(len(ks))
                    pts = (question.points or 0) * frac
                    submission.score_earned = float(pts)
                    feedback.append({"result": "partial", "fraction": frac})
                    submission.grading_feedback = {"feedback": feedback}
                    submission.last_updated = db.func.now()
                    db.session.add(submission)
                    db.session.commit()
                    return {"score": submission.score_earned, "feedback": feedback}
                return _fail('incorrect')

            if qtype == 'sql':
                # SQL query grading
                # key: {"expected_result_sql": "SELECT ... FROM ..."}
                # ans: {"sql": "SELECT ... FROM ..."}
                sql_query = (ans.get('sql') or '').strip()
                expected_result_sql = (key.get('expected_result_sql') or '').strip()
                
                if not sql_query:
                    return _fail('empty query')
                if not expected_result_sql:
                    return _fail('no expected result SQL in key')
                
                # Get the database for this question
                options = _ensure_json(getattr(question, 'options_json', None))
                db_file_id = options.get('database_file_id')
                
                if not db_file_id:
                    return _fail('no database configured for this question')
                
                db_file = db.session.get(DatabaseFile, db_file_id)
                if not db_file:
                    return _fail('database not found')
                
                # Resolve actual file path from DatabaseFile.filename
                filename = getattr(db_file, 'filename', None)
                if not filename:
                    return _fail('database has no filename')

                # If filename is absolute and exists, use it
                if os.path.isabs(filename) and os.path.isfile(filename):
                    db_path = filename
                else:
                    # Otherwise, look in the uploads/databases directory (historical storage)
                    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
                    candidate = os.path.join(upload_dir, filename)
                    if os.path.isfile(candidate):
                        db_path = candidate
                    else:
                        # Fallback: try relative to project root
                        candidate2 = os.path.join(current_app.root_path, '..', filename)
                        if os.path.isfile(candidate2):
                            db_path = candidate2
                        else:
                            return _fail('database file not accessible')
                
                try:
                    # Execute both student and expected queries, capture per-query cursor descriptions
                    import sqlite3
                    conn = sqlite3.connect(db_path)
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()

                    # Execute student query
                    cursor.execute(sql_query)
                    student_rows = cursor.fetchall()
                    student_desc = cursor.description

                    # Execute expected query
                    cursor.execute(expected_result_sql)
                    expected_rows = cursor.fetchall()
                    expected_desc = cursor.description

                    # Format both results as CSV-like strings using the correct descriptions
                    def format_result(rows, cursor_desc):
                        if not cursor_desc:
                            return ''
                        headers = [desc[0] for desc in cursor_desc]
                        result = ','.join(headers) + '\n'
                        for row in (rows or []):
                            vals = []
                            for h in headers:
                                try:
                                    v = row[h]
                                except Exception:
                                    v = None
                                vals.append('' if v is None else str(v))
                            result += ','.join(vals) + '\n'
                        return result

                    student_result = format_result(student_rows, student_desc)
                    expected_result = format_result(expected_rows, expected_desc)

                    # Close connection after formatting to avoid losing cursor metadata
                    try:
                        conn.close()
                    except Exception:
                        pass

                    # Compare results
                    grade_type, fraction = _compare_sql_results(student_result, expected_result)

                    if grade_type == 'full':
                        feedback.append({"result": "match", "mode": "sql", "grade": "full"})
                        return _ok()
                    elif grade_type == 'partial':
                        pts = (question.points or 0) * fraction
                        submission.score_earned = float(pts)
                        feedback.append({"result": "partial", "mode": "sql", "grade": "partial", "fraction": fraction})
                        submission.grading_feedback = {"feedback": feedback}
                        submission.last_updated = db.func.now()
                        db.session.add(submission)
                        db.session.commit()
                        return {"score": submission.score_earned, "feedback": feedback}
                    else:
                        return _fail('query result does not match expected output')

                except sqlite3.Error as e:
                    current_app.logger.exception('SQLite error during SQL grading')
                    return _fail(f'SQL error: {str(e)[:200]}')
                except Exception as e:
                    current_app.logger.exception('SQL grading failed')
                    # Return the exception text (trimmed) to aid debugging while still recording server-side logs
                    return _fail(f'execution error: {str(e)[:200]}')

            if qtype == 'norm':
                # Two modes: structured selection of normal forms and/or textual answers
                # Structured: key {"correct_forms":[...]} vs ans {"selected_forms":[...]}
                if 'correct_forms' in key:
                    kc = set(map(str, key.get('correct_forms') or []))
                    ac = set(map(str, (ans.get('selected_forms') or ans.get('selected') or [])))
                    if not kc:
                        return _fail('missing key')
                    if kc == ac:
                        feedback.append({"result": "match", "mode": "forms"})
                        return _ok()
                    inter = len(kc & ac)
                    if inter:
                        frac = inter / float(len(kc))
                        pts = (question.points or 0) * frac
                        submission.score_earned = float(pts)
                        feedback.append({"result": "partial", "mode": "forms", "fraction": frac})
                        submission.grading_feedback = {"feedback": feedback}
                        submission.last_updated = db.func.now()
                        db.session.add(submission)
                        db.session.commit()
                        return {"score": submission.score_earned, "feedback": feedback}
                    # fall through to text-based checks

                # If schema and decomposition provided, check NF level against target
                schema = _ensure_json(getattr(question, 'options_json', None)).get('schema') if hasattr(question, 'options_json') else None
                if schema and ans.get('decomposition'):
                    try:
                        rels = ans.get('decomposition') or []
                        rel_sets = []
                        for r in rels:
                            rel_sets.append(set(str(x).strip() for x in (r or []) if str(x).strip()))
                        fds_raw = (_ensure_json(schema).get('fds') or []) if isinstance(schema, (dict, str)) else []
                        fds: List[Tuple[Set[str], Set[str]]] = []
                        for fd in fds_raw:
                            lhs = set(str(x).strip() for x in fd.get('lhs', []) if str(x).strip())
                            rhs = set(str(x).strip() for x in fd.get('rhs', []) if str(x).strip())
                            if lhs and rhs:
                                fds.append((lhs, rhs))
                        if fds and rel_sets:
                            levels_map = {'1NF': 1, '2NF': 2, '3NF': 3, 'BCNF': 4, '4NF': 5, '5NF': 6}
                            per_rel_levels = []
                            for r in rel_sets:
                                lvl = _nf_level(r, fds)
                                per_rel_levels.append(lvl)
                            min_lvl = min(per_rel_levels, key=lambda x: levels_map.get(x, 1)) if per_rel_levels else '1NF'
                            target = (key.get('target_nf') or '').upper()
                            if target in levels_map:
                                if levels_map[min_lvl] >= levels_map[target]:
                                    feedback.append({"result": "match", "mode": "nf", "level": min_lvl, "target": target})
                                    return _ok()
                                else:
                                    frac = levels_map[min_lvl] / float(levels_map[target])
                                    submission.score_earned = float((question.points or 0) * frac)
                                    feedback.append({"result": "partial", "mode": "nf", "level": min_lvl, "target": target, "fraction": frac})
                                    submission.grading_feedback = {"feedback": feedback}
                                    submission.last_updated = db.func.now()
                                    db.session.add(submission)
                                    db.session.commit()
                                    return {"score": submission.score_earned, "feedback": feedback}
                    except Exception:
                        current_app.logger.exception('Normalization NF evaluation failed')

                # Textual checks (same as free)
                text = (ans.get('text') or '').strip()
                
                # Try to parse as relations and evaluate against target NF if schema+target provided
                schema = _ensure_json(getattr(question, 'options_json', None)).get('schema') if hasattr(question, 'options_json') else None
                target_nf = (key.get('target_nf') or '').upper()
                if text and schema and target_nf:
                    try:
                        # Parse relations from text
                        rels = _parse_relations_from_text(text)
                        if rels:
                            # Get FDs from schema
                            fds_raw = (_ensure_json(schema).get('fds') or []) if isinstance(schema, (dict, str)) else []
                            fds: List[Tuple[Set[str], Set[str]]] = []
                            for fd in fds_raw:
                                lhs = set(str(x).strip() for x in fd.get('lhs', []) if str(x).strip())
                                rhs = set(str(x).strip() for x in fd.get('rhs', []) if str(x).strip())
                                if lhs and rhs:
                                    fds.append((lhs, rhs))
                            
                            if fds:
                                levels_map = {'1NF': 1, '2NF': 2, '3NF': 3, 'BCNF': 4, '4NF': 5, '5NF': 6}
                                per_rel_levels = []
                                for r in rels:
                                    lvl = _nf_level(r, fds)
                                    per_rel_levels.append(lvl)
                                min_lvl = min(per_rel_levels, key=lambda x: levels_map.get(x, 1)) if per_rel_levels else '1NF'
                                
                                if target_nf in levels_map:
                                    if levels_map[min_lvl] >= levels_map[target_nf]:
                                        feedback.append({"result": "match", "mode": "nf_text", "level": min_lvl, "target": target_nf, "relations": len(rels)})
                                        return _ok()
                                    else:
                                        frac = levels_map[min_lvl] / float(levels_map[target_nf])
                                        submission.score_earned = float((question.points or 0) * frac)
                                        feedback.append({"result": "partial", "mode": "nf_text", "level": min_lvl, "target": target_nf, "fraction": frac, "relations": len(rels)})
                                        submission.grading_feedback = {"feedback": feedback}
                                        submission.last_updated = db.func.now()
                                        db.session.add(submission)
                                        db.session.commit()
                                        return {"score": submission.score_earned, "feedback": feedback}
                    except Exception:
                        current_app.logger.exception('Normalization NF text evaluation failed')
                
                # Fall back to acceptable/regex matching
                acc = key.get('acceptable') or []
                regex = key.get('regex')
                if text and any(str(x).strip().lower() == text.lower() for x in acc):
                    feedback.append({"result": "match", "mode": "acceptable"})
                    return _ok()
                if text and regex:
                    import re
                    try:
                        if re.compile(regex, re.I).fullmatch(text):
                            feedback.append({"result": "match", "mode": "regex"})
                            return _ok()
                    except Exception:
                        current_app.logger.exception('Invalid regex in normalization answer_key_json')
                return _fail('incorrect')

            # Optional: accept a student-provided decomposition by signature
            if qtype == 'norm' and 'decomposition' in ans:
                try:
                    sig = _signature_of_decomposition(ans.get('decomposition') or [])
                    allowed = set(map(str, key.get('decomposition_signatures') or []))
                    if allowed:
                        if sig in allowed:
                            feedback.append({"result": "match", "mode": "decomposition", "signature": sig})
                            return _ok()
                        return _fail('decomposition not in accepted set')
                except Exception:
                    current_app.logger.exception('Failed to evaluate normalization decomposition signature')
                    return _fail('decomposition evaluation error')

            if qtype == 'free':
                # key: {"acceptable": ["answer1", "answer2"], "regex": "^foo$"}
                # ans: {"text": "..."}
                text = (ans.get('text') or '').strip()
                if not text:
                    return _fail('empty')
                acc = key.get('acceptable') or []
                regex = key.get('regex')
                # case-insensitive exact match against acceptable list
                low = text.lower()
                if any(str(x).strip().lower() == low for x in acc):
                    feedback.append({"result": "match", "mode": "acceptable"})
                    return _ok()
                if regex:
                    import re
                    try:
                        if re.compile(regex, re.I).fullmatch(text):
                            feedback.append({"result": "match", "mode": "regex"})
                            return _ok()
                    except Exception:
                        current_app.logger.exception('Invalid regex in answer_key_json')
                return _fail('incorrect')

            # Unknown type: no credit
            return _fail('unsupported question type')
        except Exception as e:
            current_app.logger.exception('Non-RA grading failed')
            # Surface trimmed exception text in feedback to aid debugging in dev
            return _fail(f'grading error: {str(e)[:200]}')

    # Default RA-type grading
    testcases = QuestionTestCase.query.filter_by(question_id=question.id).all()
    executor = RAExecutor()

    # If the question has an explicit solution_query, prefer direct comparison
    if question.solution_query and str(question.solution_query).strip():
        # determine DB path: question.db_id -> uploaded DB file, else BANK_DB
        db_path = None
        if question.db_id:
            try:
                dbf = db.session.get(DatabaseFile, question.db_id)
                if dbf:
                    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
                    candidate = os.path.join(upload_dir, dbf.filename)
                    if os.path.exists(candidate):
                        db_path = candidate
            except Exception:
                current_app.logger.exception('Failed to resolve question database file')

        if not db_path:
            db_path = current_app.config.get('BANK_DB')

        executor.db_path = db_path

        # run solution and student queries
        sol_out, sol_err = executor.execute(question.solution_query or "")
        stu_out, stu_err = executor.execute(submission.student_query or "")

        feedback = []
        if sol_err:
            feedback.append({'error': f'solution error: {sol_err}'})
            submission.score_earned = 0.0
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': False}}

        if stu_err:
            feedback.append({'student_error': stu_err})
            submission.score_earned = 0.0
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': False}}

        if _compare_results(sol_out, stu_out):
            # full credit
            submission.score_earned = float(question.points or 0)
            feedback.append({'result': 'match', 'explanation': 'Student query matches solution_query'})
            submission.grading_feedback = {'feedback': feedback}
            submission.last_updated = db.func.now()
            db.session.add(submission)
            db.session.commit()
            return {'score': submission.score_earned, 'feedback': feedback, 'comparison': {'solution_output': sol_out, 'student_output': stu_out, 'match': True}}
        # else fall through to testcase/milestone grading

    total_weight = sum((tc.weight or 1.0) for tc in testcases) or 1.0
    earned = 0.0
    feedback = []

    for tc in testcases:
        # Use testcase db_path if provided, otherwise fall back to
        # configured BANK_DB
        executor.db_path = tc.db_path or current_app.config.get('BANK_DB')

        # Run solution and student queries
        sol_out, sol_err = executor.execute(question.solution_query or "")
        stu_out, stu_err = executor.execute(submission.student_query or "")

        if sol_err:
            feedback.append({
                "tc": tc.id,
                "error": f"solution error: {sol_err}",
            })
            continue

        if stu_err:
            feedback.append({"tc": tc.id, "student_error": stu_err})
            # no credit for this testcase
            continue

        if _compare_results(sol_out, stu_out):
            earned += (tc.weight or 1.0)
            feedback.append({"tc": tc.id, "result": "pass"})
        else:
            # Check milestones for partial credit
            ms_score = 0.0
            for m in QuestionMilestone.query.filter_by(
                question_id=question.id
            ).all():
                # Run the milestone check query against the same DB
                chk_out, chk_err = executor.execute(m.check_query or "")
                if not chk_err and chk_out.strip():
                    ms_score += getattr(m, "points", 0)
            if ms_score:
                earned += ms_score
                feedback.append(
                    {
                        "tc": tc.id,
                        "result": "partial",
                        "milestone_points": ms_score,
                    }
                )
            else:
                feedback.append({"tc": tc.id, "result": "fail"})

    # Normalize score to question points
    score_fraction = earned / total_weight
    final_score = (question.points or 0) * score_fraction

    # Persist
    submission.score_earned = float(final_score)
    submission.grading_feedback = {"feedback": feedback}
    submission.last_updated = db.func.now()
    db.session.add(submission)
    db.session.commit()

    return {"score": submission.score_earned, "feedback": feedback}
