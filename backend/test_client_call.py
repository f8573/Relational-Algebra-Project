import jwt
from app import create_app
app = create_app()
secret = app.config.get('SECRET_KEY')
payload = {'user_id':1}
try:
    token = jwt.encode(payload, secret, algorithm=app.config.get('JWT_ALGORITHM','HS256'))
    if isinstance(token, bytes): token = token.decode('utf-8')
except Exception as e:
    print('token error', e); raise
with app.test_client() as c:
    headers = {'Authorization': 'Bearer ' + token}
    resp = c.get('/api/courses/1/assignments', headers=headers)
    print('STATUS', resp.status_code)
    print(resp.get_data(as_text=True))
