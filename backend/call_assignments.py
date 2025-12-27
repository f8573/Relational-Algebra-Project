import jwt, requests
secret='dev-key-change-this-in-prod'
payload={'user_id':1}
# Create token
try:
    token = jwt.encode(payload, secret, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
except Exception as e:
    print('Error creating token', e)
    raise
headers={'Authorization': 'Bearer ' + token}
url = 'http://127.0.0.1:5001/api/courses/1/assignments'
try:
    r = requests.get(url, headers=headers, timeout=10)
    print('STATUS', r.status_code)
    print(r.text)
except Exception as e:
    print('REQUEST ERROR', e)
