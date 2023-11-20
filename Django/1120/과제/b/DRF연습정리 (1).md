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
django-admin startproject project .
python manange.py startapp post
python manange.py startapp blog
```

### django_JWT/settings.py

```python
INSTALLED_APPS = [
    'rest_framework',

    'post',
    'blog',
]

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
```

### superuser생성

python manage.py createsuperuser

### project/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notice/', include('post.urls')),
    path('blog/', include('blog.urls')),

    path('api-auth/', include('rest_framework.urls')),
]
```

## blog

### blog/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

### blog/models.py

모델 생성

```python
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

```

### blog/views.py

```python
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

```

### blog/serializers.py

```python
from rest_framework import serializers
from .models import BlogPost
from django.contrib.auth import get_user_model

class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields =[
            'id',
            'title',
            'content',
        ]
```

여기까지 로그인한 유저만 블로그 글을 CRUD할 수 있음.
UD는 그 글의 작성자만 할 수 있도록 변경

### blog/models.py

내용 추가

```python
from django.conf import settings

class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ...
```

python manage.py makemigrations
python manage.py migrate

### blog/permissions.py

```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 리턴합니다.
        그 외 요청(PUT, DELETE)에 대해서는 작성자에 한해서만 True를 리턴합니다.
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

### post/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```

## post

### post/models.py

```python
from django.db import models
from django.conf import settings

class Post(models.Model):
author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
title = models.CharField(max_length=100)
content = models.TextField()
```

### post/views.py

```python
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from ..blog.permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
```

### post/serializers.py

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fileds = ['title', 'content']
```

### post/permissions.py

모든 사용자가 읽을 수 있고
회원만 생성
작성자만 수정, 삭제할 수 있음.

```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
            return True

    def has_object_permission(self, request, view, obj):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 리턴합니다.
        그 외 요청(PUT, DELETE)에 대해서는 작성자에 한해서만 True를 리턴합니다.
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

### 모델 적용

python manage.py makemigrations
python manage.py migrate
