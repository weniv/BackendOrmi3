import requests

# Django 로그인 테스트용 파일입니다.
HOST = 'http://localhost:8000'
LOGIN_URL = HOST + '/accounts/login/'
LOGIN_INFO = {
    'username': 'admin',
    'password': 'admin',
}

res = requests.post(LOGIN_URL, data=LOGIN_INFO)
print(res.status_code)

token = res.json()['token']
print(token)

# 헤더가 필요한 경우
headers = {
    'Authorization': 'Token ' + token,
}

res = requests.get(HOST + '/blog/1', headers=headers)
print(res.status_code)
print(res.json())
