## 가상 환경 세팅
``` zsh
python3 -m venv venv
source ./venv/bin/activate
```

## 라이브러리 설치
``` zsh
pip install -r requirements.txt
```

## 프로젝트 세팅
``` zsh
django-admin startproject jwtpractice .

python3 manage.py startapp accounts
```

## settings.py
```py
.
.

from datetime import timedelta

.
.

INSTALLED_APPS = [

    .
    .
    .
    # app
    'accounts',
    ## 라이브러리
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
]

.
.
.

# dj-rest-auth
REST_USE_JWT = True  # JWT 사용 여부
JWT_AUTH_COOKIE = 'my-app-auth'  # 호출할 Cookie Key 값
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'  # Refresh Token Cookie Key 값

# django-allauth
SITE_ID = 1  # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True  # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # 사용자 이름 필드 지정
ACCOUNT_USERNAME_REQUIRED = False  # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True  # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = 'none'  # email 인증 필수 여부

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # AccessToken 유효 기간 설정
    # RefreshToken 유효 기간 설정
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
ACCOUNT_EMAIL_VERIFICATION = 'none'
AUTH_USER_MODEL = 'accounts.User'

```

## URL 세팅

```py
# jwtpractice > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]

```

```py
# accounts > urls.py

from django.urls import path, include
from . import views
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('join/', include('dj_rest_auth.registration.urls')),
    path('mypage/', views.mypage)
]

```

## models.py
```py
# accounts > models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    objects = UserManager()

    USERNAME_FIELD = 'email'

```

## manager.py
```py
# accounts > managers.py
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

```

## 마이그레이션
```
python3 manage.py makemigrations
python3 mangae.py migrate
```

## 회원가입 테스트 (POST)
```json
# 접속 주소 http://localhost:8000/accounts/join/
{
    "email": "0@0.com",
    "password1": "********",
    "password2": "********"
}
```
## 회원가입 테스트 결과
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAwNTI3LCJpYXQiOjE3MDAxOTY5MjcsImp0aSI6IjBlODkxNGJjYWQ2YjRmYjZiN2Y5Mzc5ZjBiYmVlNTBjIiwidXNlcl9pZCI6NH0.W1lbH96gGvY19AqzzQ9B5Q06vgc_K1A9qSQhH3Zp5oc",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MzMyNywiaWF0IjoxNzAwMTk2OTI3LCJqdGkiOiIwZmI2ZTgxZGY1MDk0NGY0OGY3OTBmZmIxNDAzNzg5ZSIsInVzZXJfaWQiOjR9.jineUG61BQUs5uoflZkMMutjwFWa2WlYjUG-Udfq88s",
    "user": {
        "pk": 4,
        "email": "0@0.com",
        "first_name": "",
        "last_name": ""
    }
}
```
## 로그인 테스트 (POST)
```json
# 접속 주소 http://localhost:8000/accounts/login/
{
    "email": "0@0.com",
    "password": "********",
}
```
## 로그인 테스트 결과
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAwNjk0LCJpYXQiOjE3MDAxOTcwOTQsImp0aSI6IjRiYmQwMTIwMDRmYTQ0NDVhOTkwNDFhMzBlNTJjNzQ5IiwidXNlcl9pZCI6NH0.ekycUDNJowsHMHLBf8AFzQFXywrA4AVdQNktYlM6edE",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MzQ5NCwiaWF0IjoxNzAwMTk3MDk0LCJqdGkiOiJhYjYwZWUxYzg2YmQ0OWFiOWNhN2I0NjZhZmI3NzYyZCIsInVzZXJfaWQiOjR9.R18Hz3bOvuhZ6A8TwJAAKtXXpRWv7vfZuD2napHBDc4",
    "user": {
        "pk": 4,
        "email": "0@0.com",
        "first_name": "",
        "last_name": ""
    }
}
```
## 마이페이지 테스트 (GET)
```py
# 접속 주소 http://localhost:8000/accounts/mypage/

Bearer Toekn : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk5NTExLCJpYXQiOjE3MDAxOTU5MTEsImp0aSI6Ijg3ODBhZjg4ZTEyYjQ5NTY4MTQ4MTU0MmE3ODNjYzM0IiwidXNlcl9pZCI6M30.
Av1lCLAeRQv1XFSXkmcgIJbXlzEuDKJB2cP0ApqPfqA
```
## 마이페이지 테스트 결과
```json
{
    "message": "반갑습니다! 4@4.com님!"
}
```

## 로그아웃 테스트 (POST)
```json
# 접속 주소 http://localhost:8000/accounts/logout/
```
## 로그아웃 테스트 결과
```json
{
    "detail": "Successfully logged out."
}
```
