1. 환경 설정
가상 환경 설정

# 프로젝트 디렉토리 생성
mkdir myproject
cd myproject

# Python 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows
.\venv\Scripts\activate 
# macOS/Linux
source venv/bin/activate
Django 및 DRF 설치
가상 환경에서 Django와 Django Rest Framework를 설치합니다.

```
pip install django
pip install djangorestframework

django-admin startproject mysite .
python manage.py startapp blog
python manage.py startapp accounts
```

2. 프로젝트 설정
settings.py 수정

```
# mysite/settings.py

INSTALLED_APPS = [
    # 기존 앱들
    'rest_framework',
    'blog',
    'accounts',
    # ...
]
```

# 나머지 설정들...
URL 라우팅 설정

```
# mysite/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
]

```

3. 모델, 뷰, 시리얼라이저 생성
3-1. 모델 정의 (models.py)

```
from django.db import models
from django.conf import settings

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

3-2. 시리얼라이저 정의 (serializers.py)

```
from rest_framework import serializers
from .models import Notice, BlogPost

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
```

3-3. 권한 설정 (permissions.py)

```
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

3-4. 뷰셋 정의 (views.py)
```
from rest_framework import viewsets, permissions
from .models import Notice, BlogPost
from .serializers import NoticeSerializer, BlogPostSerializer
from .permissions import IsAuthorOrReadOnly

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```
3-5. URL 라우팅 (urls.py)
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet, BlogPostViewSet

router = DefaultRouter()
router.register(r'notice', NoticeViewSet)
router.register(r'blog', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# account/urls.py
urlpatterns = []
```
3-6 admin.py
from django.contrib import admin
from .models import Notice, BlogPost

admin.site.register(Notice)
admin.site.register(BlogPost)

4. 데이터베이스 마이그레이션

```
python manage.py makemigrations
python manage.py migrate
```
5. 관리자 계정 생성

```
python manage.py createsuperuser
```
6. 서버 실행

```
python manage.py runserver
```
