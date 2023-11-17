### 가상환경 설치

```
python -m venv venv
```

### 가상환경 진입

```
.\venv\Scripts\activate
```

### 라이브러리 설치

```requirements.txt
asgiref             3.7.2
certifi             2023.7.22
charset-normalizer  3.3.2
Django              4.2.7
django-extensions   3.2.3
djangorestframework 3.14.0
idna                3.4
Pillow              10.1.0
pip                 23.3.1
pytz                2023.3.post1
requests            2.31.0
sqlparse            0.4.4
tzdata              2023.3
urllib3             2.1.0
```

### 장고 프로젝트 생성

```
django-admin startproject django_JWT .
python manange.py startapp accounts
```

### django_JWT/settings.py

```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    'accounts',
]

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
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

### migrate

```
python manage.py migrate
```

## URL

### django_JWT/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls"))
]
```

### accounts/urls.py

```python
from django.urls import path, include

urlpatterns = [
    path('join/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
]
```

## Custom User모델 구현

### accounts/managers.py

```python
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

### accounts/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```

### admin site추가

admin.py

```python
from .models import CustomUser

admin.site.register(CustomUser)
```

### migration

```
python manage.py makemigrations
python manage.py migrate
```

### accounts/views.py 마이페이지 추가

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage_view(request):

    content = {'message': f'반갑습니다!, {request.user}님!'}
    return Response(content)
```

### accounts/url.py 추가

```python
from .views import mypage_view

urlpatterns = [
    ...
    path('test/', mypage_view),
]
```

## 테스트

### 회원가입 (POST)

/account/join
{
"email":"test123@test123.com",
"password1":"chang123",
"password2":"chang123"
}

### 로그인 (POST)

/account/login
{
"email":"test123@test123.com",
"password":"chang123"
}

### 로그아웃 (POST)

/account/logout

### 마이페이지 (GET)

/account/mypage

headers
Authorization: Bearer + 토큰값
