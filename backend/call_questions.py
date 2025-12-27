import jwt, requests, json
secret='dev-key-change-this-in-prod'
payload={'user_id':1}
try:
    token = jwt.encode(payload, secret, algorithm='HS256')
    if isinstance(token, bytes): token = token.decode('utf-8')
except Exception as e:
    print('token error', e); raise
h={'Authorization':'Bearer '+token}
url='http://127.0.0.1:5001/api/assessments/1/questions'
r=requests.get(url, headers=h, timeout=10)
print('STATUS', r.status_code)
print(json.dumps(r.json(), indent=2))
