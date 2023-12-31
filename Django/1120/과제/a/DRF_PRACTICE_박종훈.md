# 요구사항

> * 일반 게시판 /notice : 회원이 아닌 사람도 R 가능, 회원인 사람만 C
> * 일반 게시판 상세보기 /notice/int:post_pk: 회원이 아닌 사람도 R 가능, 작성자만 UD 가능
> * 게시글 목록 /blog : 회원인 사람만 R, C 가능
> * 게시글 상세보기 /blog/int:post_pk: 회원인 사람만 R, 작성자만 UD 가능

# 프로젝트 설계

## URL 설계
|URL|기능|CREATE|READ|UPDATE|DELETE|
|:--|:--|:--:|:--:|:--:|:--:|
|blog/post/|블로그 글의 목록을 확인하는 페이지|비로그인: X<br/>로그인: O|비로그인: X<br/>로그인: O|X|X|
|blog/post/\<int:pk\>/|블로그의 포스트를 확인하는 페이지|X|비로그인: X<br/>로그인: O|비로그인: X<br/>로그인-작성자 비인증: X<br/>로그인-작성자 인증: O|비로그인: X<br/>로그인-작성자 비인증: X<br/>로그인-작성자 인증: O|
|notice/post/|공지사항 글의 목록을 확인하는 페이지|비로그인: X<br/>로그인: O|O|X|X|
|notice/post/\<int:pk\>/|공지사항의 포스트를 확인하는 페이지|X|O|비로그인: X<br/>로그인-작성자 비인증: X<br/>로그인-작성자 인증: O|비로그인: X<br/>로그인-작성자 비인증: X<br/>로그인-작성자 인증: O|

## 인증 설계
* blog/: 로그인 한 User만 GET, POST가능
  * blog/\<int:pk\>/: 로그인 한 User만 GET가능, 로그인 한 작성자 본인만 DELETE, PUT가능
* notice/: 로그인 관계 없이 모든 사용자가 GET가능, 로그인 한 사용자만 POST가능
  * notice/\<int:pk\>/: 모든 사용자가 GET가능, 로그인 한 작성자 본인만 DELETE, PUT가능

# 프로젝트 진행

## 프로젝트 사전 준비
```
console: `python -m venv venv`
console: `./venv/Script/activate`
console: `pip install -r requirement.txt` - requirement.txt는 별도 참고
console: `mkdir drf_practice`
console: `cd ./drf_practice`
console: `django-admin startproject drf_prac .`
root/settings.py 수정
console: `python ./manage.py startapp blog`
console: `python ./manage.py startapp notice`
```

## root/setting.py
```python
"""
Django settings for drf_prac project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9vts-!#_$ikmt62iu#g=+)xb1qn$$4ny#gku8yxr(^ddsz56nz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party apps
    'rest_framework',

    # custom apps
    'notice',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drf_prac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'drf_prac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

# 각 APP 별 설정 및 인증 구현
## blog app
### model.py
```python
from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

### views.py
```python
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserOrRestricted


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,
                          IsUserOrRestricted]
    # GET요청 로그인 된 사용자만 접근 가능
    # 로그인 한 인증 유저만 POST 가능
    # 로그인 한 인증 유저가 본인이 작성한 글에만 DELETE, PUT 가능

    def perform_create(self, serializer):
        # 현재 로그인 한 user가 post의 author에 자동으로 입력되도록 재정의
        # serializer(PostSerializer)에 author라는 이름을 통해 self.request.user가 전달된다.
        serializer.save(author=self.request.user)

```

### permissions.py
```python
from rest_framework import permissions


class IsUserOrRestricted(permissions.BasePermission):
    def has_permission(self, request, view):
        # 현재 유저가 인증받은 유저인 경우에만 허용
        if request.user and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # 'GET', 'HEAD', 'OPTIONS' - 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 'PUT' 'DELETE' - 현재 유저가 obj(post글)의 작성자 본인 경우에만 허용
        return obj.author == request.user
```

### serializers.py
```python
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post


class PostSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # views.py를 통해 전달받은 author(= views.py의 PostViewSet의 perform_create의 self.request.user)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]
```

## notice app
### models.py
```python
from django.db import models
from django.conf import settings


class Notice(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('post', views.NoticeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

### views.py
```python
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLoginOrRestricted


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsLoginOrRestricted]
    # GET 요청 - 모든 사용자 접근 가능하도록 설정
    # 로그인 한 인증 유저만 POST 가능
    # 로그인 한 인증 유저가 본인이 작성한 글에만 DELETE, PUT 가능

    def perform_create(self, serializer):
        # 현재 로그인 한 user가 post의 author에 자동으로 입력되도록 재정의
        # serializer(PostSerializer)에 author라는 이름을 통해 self.request.user가 전달된다.
        serializer.save(author=self.request.user)
```

### permissions.py
```python
from rest_framework import permissions


class IsLoginOrRestricted(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 'GET', 'HEAD', 'OPTIONS'
        if request.method in permissions.SAFE_METHODS:
            return True

        # 'PUT' 'DELETE'
        return obj.author == request.user
```

### serializers.py
```python
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Notice


class NoticeSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # views.py를 통해 전달받은 author(= views.py의 NoticeViewSet의 perform_create의 self.request.user)

    class Meta:
        model = Notice
        fields = [
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

```