from app.services.execution import RAExecutor


def test_clean_query_basic():
    ex = RAExecutor()
    raw = r"\text{_}"
    cleaned = ex._clean_query(raw)
    assert '_' in cleaned

    # ensure semicolon appended when single-line
    cleaned2 = ex._clean_query('select *')
    assert cleaned2.strip().endswith(';')
