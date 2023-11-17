# JWT, DRF 연습

1. 프로젝트 세팅 <br>

    - 가상환경 설정

    ```
    python -m venv .venv
    ```

    - django를 비롯한 모든 모듈 `requirements.txt`에서 설치 <br>

   ```text
   # requirements.txt 파일 내용
   asgiref==3.7.2
   certifi==2023.7.22
   cffi==1.16.0
   charset-normalizer==3.3.2
   cryptography==41.0.5
   defusedxml==0.7.1
   dj-rest-auth==2.2.4
   Django==4.0.3
   django-allauth==0.50.0
   djangorestframework==3.13.1
   djangorestframework-simplejwt==5.1.0
   idna==3.4
   oauthlib==3.2.2
   pycparser==2.21
   PyJWT==2.8.0
   python3-openid==3.2.0
   pytz==2023.3.post1
   requests==2.31.0
   requests-oauthlib==1.3.1
   sqlparse==0.4.4
   typing_extensions==4.8.0
   tzdata==2023.3
   urllib3==2.0.7
   ```


2. 장고 프로젝트 생성하기 <br>

```zsh
# 프로젝트 생성
django-admin startproject jwt
# app 생성
python manage.py startapp accounts
```

3. 커스텀 User Model 생성하기

```python
# accounts -> managers.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


# accounts -> models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager

GENDER_CHOICES = (
    ("male", "남자"),
    ("female", "여자"),
)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

```

4. settings.py 설정

```python
# 모든 호스트 허용
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    ...,
    # DRF ,JWT 및 인증 관련
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    # 커스텀 앱
    'accounts',
    ...
]

# 커스텀 유저 모델
AUTH_USER_MODEL = "accounts.CustomUser"

# 인증 및 JWT 관련
# dj-rest-auth
REST_USE_JWT = True  # JWT 사용 여부
JWT_AUTH_COOKIE = "my-app-auth"  # 호출할 Cookie Key 값
JWT_AUTH_REFRESH_COOKIE = "my-refresh-token"  # Refresh Token Cookie Key 값

# django-allauth
SITE_ID = 1  # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True  # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # 사용자 이름 필드 지정
ACCOUNT_USERNAME_REQUIRED = False  # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True  # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = "email"  # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = "none"  # email 인증 필수 여부

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # AccessToken 유효 기간 설정
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),  # RefreshToken 유효 기간 설정
}

# DRF 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
```

5. accounts.views.py 설정

```python
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_page(request: HttpRequest):
    user = request.user
    return Response(status=200, data={"message": f"반갑니다. {user.email}님"})

```

6. url 설정

### accounts.urls.py

```python
from django.urls import path, include

from accounts.views import my_page

urlpatterns = [
    path("join/", include("dj_rest_auth.registration.urls")),
    path("", include("dj_rest_auth.urls")),
    path("mypage/", my_page, name="mypage"),
]
```

### jwt.urls.py

```python

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls")),
]
```

7. Api 테스트

### 회원가입 API

```python
# Create your tests here.

from unittest import TestCase

import requests


class TestApi(TestCase):
    def setUp(self):
        self.Host = "http://localhost:8000"
        self.token: str | None = None

        data = {"email": "test@Test.com", "password": "someTestPassword!"}
        res = requests.post(f"{self.Host}/account/login/", data)
        self.token = res.json()["access_token"]

    def test_join(self):
        data = {
            "email": "test3@Test.com",
            "password1": "someTestPassword!",
            "password2": "someTestPassword!",
        }

        res = requests.post(f"{self.Host}/account/join/", data)
        self.assertNotIn(res.status_code, [400, 401, 404])
        print(res.text)

    def test_login(self):
        data = {"email": "test@Test.com", "password": "someTestPassword!"}

        res = requests.post(f"{self.Host}/account/login/", data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.json()["access_token"], None)
        print(res.json()["access_token"])
        self.token = res.json()["access_token"]

    def test_mypage(self):
        header = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(f"{self.Host}/account/mypage/", headers=header)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text, None)
        print(res.text)

    def test_logout(self):
        res = requests.post(f"{self.Host}/account/logout/", {"token": self.token})
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text, None)
        print(res.text)
```

### 테스트 결과

```
Launching unittests with arguments python -m unittest tests.TestApi in /Users/daehyeon/Documents/coding_files/Boot_Camp/Ormi/JWT_20231117/accounts

# 회원 가입 테스트
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk5NTc4LCJpYXQiOjE3MDAxOTU5NzgsImp0aSI6ImNkOWY4ZWEzMzI5MDQ5YzM4YjI4MDNiYmNiNDA0MDI0IiwidXNlcl9pZCI6NX0.VsQ4976XHm942y8nBXp2GMqKjsyxrztPpt0JCQMIhts","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MjM3OCwiaWF0IjoxNzAwMTk1OTc4LCJqdGkiOiJiY2M3NjNlZGMwZTQ0NTMyYWZjOWFjMGM2ZDE5ODIyOCIsInVzZXJfaWQiOjV9.6DAd4fYwxghyBhuyds8X3ygZh-1V4K4OrvPhxYDBKDo","user":{"pk":5,"email":"test3@Test.com","first_name":"","last_name":""}}

# 로그인 테스트
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk5NTc4LCJpYXQiOjE3MDAxOTU5NzgsImp0aSI6IjU4OTExNmZmZjFjNzRiNDVhZWJhMjJiOTIzNmEyNDRhIiwidXNlcl9pZCI6M30.cY0HCw9mxycDLzK633npBE5JQe55BJqXnqnEDWBP-90

# 로그아웃 테스트
{"detail":"Successfully logged out."}


Ran 4 tests in 0.574s

OK

# mypage 테스트
{"message":"반갑니다. test@Test.com님"}

Process finished with exit code 0
```