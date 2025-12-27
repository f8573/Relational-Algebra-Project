from app import create_app
app=create_app()
with app.app_context():
    from app.models import Question
    qs = Question.query.filter_by(assessment_id=1).all()
    for q in qs:
        print('ID', q.id, 'type', getattr(q,'question_type',None), 'options', getattr(q,'options_json',None), 'answer_key', getattr(q,'answer_key_json',None), 'points', getattr(q,'points',None))
