# Access Token이 유효한 경우에만 접근이 가능한 마이페이지를 만들어주세요.

1. 로그인하여 Access Token을 발급받습니다.
2. 마이페이지 접속시 header에 Access Token을 담아보냅니다. Access Token이 유효한 경우에만 마이페이지에 접근이 가능합니다.
3. 마이페이지에 접속하면(포스트맨 또는 다른 API 툴로 하셔도 됩니다.) "반갑습니다, {유저이메일}님!"이 화면에 출력되도록 해주세요.

# 구현되어야할 엔드 포인트는(API) 아래와 같습니다.

/account/join # 회원가입
/account/login # 로그인
/account/logout # 로그아웃
/account/mypage # 로그인한 사용자만 확인가능

# 가상환경 설정
python -m venv venv 
.\venv\Scripts\activate # window

# Django 설치
pip install django

django-admin startproject project . 

python manage.py startapp accounts 

# settings.py 
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', <- app 추가 
]
```

# accounts/managers.py
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
# accounts/models.py
모델 추가
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
# settings.py 
```
...
AUTH_USER_MODEL = 'accounts.CustomUser' <- 마지막 줄에 추가
...
```
# terminal(powershell)
데이터베이스 적용
```
python manage.py makemigrations
python manage.py migrate
```
# accounts/admin
admin 등록
```
from django.contrib import admin
from accounts.models import CustomUser

admin.site.register(CustomUser)
```
# 라이브러리 설치
```
# requirements.txt
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
```
pip install -r requirements.txt
```
# settings.py
```
INSTALLED_APPS = [
...
    # 설치한 라이브러리들
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
...
]
```
```
from datetime import timedelta
... 

# dj-rest-auth
REST_USE_JWT = True # JWT 사용 여부
JWT_AUTH_COOKIE = 'my-app-auth' # 호출할 Cookie Key 값
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' # Refresh Token Cookie Key 값

# django-allauth
SITE_ID = 1 # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True # User email unique 사용 여부 / -> 중복 NO
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # 사용자 이름 필드 지정 -> 필드 NO
ACCOUNT_USERNAME_REQUIRED = False # User username 필수 여부 -> USERNAME NO
ACCOUNT_EMAIL_REQUIRED = True # User email 필수 여부 -> EMAIL 필수
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 로그인 인증 수단 -> 로그인은 EMAIL로
ACCOUNT_EMAIL_VERIFICATION = 'none' # email 인증 필수 여부 -> EMAIL 인증 필수는 아님??

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # AccessToken 유효 기간 설정 60분
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # RefreshToken 유효 기간 설정 1일
}
```
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```
```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
# terminal(powershell)
```
python manage.py migrate
```
# project/urls.py
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls"))
]
```
```
# No module named 'pkg_resources'에러가 나면 아래 코드를 실행해주세요.
pip install --upgrade setuptools
# pip install --upgrade distribute # 위에것만 해도 되실텐데 안되시면 아래 명령어도 입력해주세요.
```
# <------------- 여기서 부터 과제 내용 ------------->

# accounts/urls.py 
```
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path('join/', include("dj_rest_auth.registration.urls")),
    path('test/', views.example_view),
    path('mypage/', views.mypage), <- mypage 추가
]
```

# accounts/views.py
```
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request):
    # request.user는 인증된 사용자의 정보를 담고 있습니다.
    # request에 POST에 담긴 data를 출력합니다.
    print(request.data)
    content = {'message': 'Hello, World!', 'user': str(request.user)}
    return Response(content)

<------------- 여기서 부터 과제 내용 ------------->
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    print(request.data)
    content = {'message': '반갑습니다', 'user': str(request.user)}
    return Response(f'{content["message"]}, {content["user"]}님!')
```

![Alt text](image.png)
login 할 떄 받은 토큰으로 mypage에 접근이 가능함.

```
"반갑습니다, jungbae@naver.com님!"
```