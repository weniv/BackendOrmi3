### 가상 환경 설치
```
python -m venv venv
```

### 가상 환경 진입
```
.\venv\Script\activate
```

### 라이브러리 설치
```
pip install -r requirements.txt
```

### Django 프로젝트 설치
```
django-admin startproject project .
```

### accounts 앱 설치
```
python manage.py startapp accounts
```

### settings.py
```
...

from datetime import timedelta

...

ALLOWED_HOSTS = ['*']

...

INSTALLED_APPS = [
    ...
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
]

...

AUTH_USER_MODEL = 'accounts.CustomUser'

# dj-rest-auth
REST_USE_JWT = True # JWT 사용 여부
JWT_AUTH_COOKIE = 'my-app-auth' # 호출할 Cookie Key 값
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' # Refresh Token Cookie Key 값

# django-allauth
SITE_ID = 1 # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # 사용자 이름 필드 지정
ACCOUNT_USERNAME_REQUIRED = False # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = 'none' # email 인증 필수 여부

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # AccessToken 유효 기간 설정
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # RefreshToken 유효 기간 설정
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

```

### project > urls.py
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls")),
]
```

### accounts > managers.py
```
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
```

### accounts > models.py
```
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

GENDER_CHOICES = (
    ('male', '남자'),
    ('female', '여자'),
)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.email
```

### 마이그레이션
```
python manage.py makemigrations
python manage.py migrate
```

### accounts > urls.py
```
from django.urls import path, include
from . import views

urlpatterns = [
    path('join/', include("dj_rest_auth.registration.urls")),
    path("", include("dj_rest_auth.urls")),
]
```

### join 테스트
```POST
http://127.0.0.1:8000/account/join/
{
    "email": "elwl5515@gmail.com",
    "password1": "...",
    "password2": "..."
}
```

```응답
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk3NjM3LCJpYXQiOjE3MDAxOTQwMzcsImp0aSI6IjUyYzYzNDg3NjVlMzQzYWVhZTEzM2M1ZDRmMGFmOTIwIiwidXNlcl9pZCI6MX0.jet1DjgOTtyTRvwY9xatJDWO3krADbEKu5i6fevMJ4s",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MDQzNywiaWF0IjoxNzAwMTk0MDM3LCJqdGkiOiI0MWIwZjRlNjcxMTA0NWRjOGZlNTIwNTNkNTRhYjNiOCIsInVzZXJfaWQiOjF9.ADeLhZKK-ac29uTuMxU0cNfOvh7hCzlcJgKnd6iiAU4",
  "user": {
    "pk": 1,
    "email": "elwl5515@gmail.com",
    "first_name": "",
    "last_name": ""
  }
}
```

### login 테스트
```POST
http://127.0.0.1:8000/account/login/
{
    "email": "elwl5515@gmail.com",
    "password": "..."
}
```

```응답
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk3ODYyLCJpYXQiOjE3MDAxOTQyNjIsImp0aSI6IjU4ZDU4N2E0NzQ5NzQ5YTBhOGExM2M3MThkOTc3ZTg5IiwidXNlcl9pZCI6MX0.xNOoJ9lLGzEVyEKOYpvzIzVe1kHZnkjvgs5PnTv7lyM",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MDY2MiwiaWF0IjoxNzAwMTk0MjYyLCJqdGkiOiIxMjQxZWQzMDJiOTg0MmE5YmQ4NzNkZGU1ZmU1ZTBhOSIsInVzZXJfaWQiOjF9.QU0zTpAAxyUK6h5UDSD4orS3IJ9ZgprrxBR5biJs47E",
  "user": {
    "pk": 1,
    "email": "elwl5515@gmail.com",
    "first_name": "",
    "last_name": ""
  }
}
```

### logout 테스트
```POST
http://127.0.0.1:8000/account/logout/
```

```응답
{
  "detail": "Successfully logged out."
}
```

### accounts > urls.py
```
...
urlpatterns = [
    ...
    path("mypage/", views.mypage),
]
...
```

### accounts > views.py
```
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    content = {'message': 'It is my page', 'user': str(request.user)}
    return Response(content)
```

### mypage 테스트
```GET - 로그인이 안된 경우 - 토큰이 없는 경우
http://127.0.0.1:8000/account/mypage
```

```응답
{
  "detail": "Authentication credentials were not provided."
}
```

```GET - 로그인된 경우 - 토큰이 있는 경우
http://127.0.0.1:8000/account/mypage
'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTk4NzgwLCJpYXQiOjE3MDAxOTUxODAsImp0aSI6ImYyMGY0YzA2Yzc3MDRhODE5NzQyOGY4ZjRhM2Q5MTZkIiwidXNlcl9pZCI6MX0.tMFyyFtQIvAENLgMW6cyP87Gj6BPACZjUUazohk9i5Y'
```

```응답
{
  "message": "It is my page",
  "user": "elwl5515@gmail.com"
}
```