# pip install requests
import requests

HOST = 'http://localhost:8000'
LOGIN_URL = HOST + '/account/login/'


# step1 로그인
# 사용자가 본 html파일에 입력 form에서 입력한 데이터라고 생각해주세요. 
LOGIN_INFO = {
    "email": "hojun@gmail.com",
    "password": "dlghwns1234!"
}

# 로그인을 위해 post요청을 보냅니다.
response = requests.post(LOGIN_URL, data=LOGIN_INFO)
print(response.status_code)
print(response.text)
print(response.json())
print(response.json()['access_token'])

token = response.json()['access_token']


# step2 로그인한 사용자만 들어갈 수 있는 URL에 접속
# headers에 token을 넣어서 보냅니다.
header = {
    'Authorization': 'Bearer ' + token.replace('m', 'n')
}

data = {
    'title': '제목',
    'content': '내용',
    'author': 1
}

res = requests.get(HOST + '/account/test/', headers=header, data=data)
print(res.status_code)
print(res.text)