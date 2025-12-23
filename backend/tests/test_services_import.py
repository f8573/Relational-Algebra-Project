from app.services import grading, execution


def test_grading_export():
    assert hasattr(grading, 'grade_submission')


def test_execution_export():
    assert hasattr(execution, 'RAExecutor')
