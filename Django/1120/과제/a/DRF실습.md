# 목표
일반 게시판    /notice : 회원이 아닌 사람도 R 가능, 회원인 사람만 C
일반 게시판 상세보기    /notice/int:post_pk: 회원이 아닌 사람도 R 가능, 작성자만 UD 가능
게시글 목록    /blog : 회원인 사람만 R, C 가능
게시글 상세보기    /blog/int:post_pk: 회원인 사람만 R, 작성자만 UD 가능

-----------------------------------


python -m venv venv
-----------------------------------
./venv/Script/activate

-----------------------------------

pip install django
pip install djangorestframework
django-admin startproject tutorialblog .

-----------------------------------

settings.py -> 28번째 줄
ALLOWED_HOSTS = ['*']
-----------------------------------
python manage.py startapp blog
python manage.py startapp notice

-----------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog',
    'notice',
]
-----------------------------------
# project > urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls')),
    path('notice/', include('notice.urls')),
]
```
-----------------------------------
# blog > models.py
```python
from django.conf import settings
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

# notice > models.py
```python
from django.db import models
from django.conf import settings


class NoticePost(models.Model):
    Notice_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
-----------------------------------
python manage.py makemigrations
python manage.py migrate
-----------------------------------
settings.py
```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False
```
-----------------------------------
# blog > serializers.py
```python
from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
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

# notice > serializers.py
```python
from rest_framework.serializers import ModelSerializer
from .models import NoticePost

class NoticePostSerializer(ModelSerializer):
    class Meta:
        model = NoticePost
        fields = [
            'id',
            'Notice_author',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]
```
-----------------------------------
# blog > views.py

```python
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
```

# notice > views.py

```python
from rest_framework.viewsets import ModelViewSet
from .models import NoticePost
from .serializers import NoticePostSerializer
from .permissions import IsAuthorOrReadOnly

class NoticePostViewSet(ModelViewSet):
    queryset = NoticePost.objects.all()
    serializer_class = NoticePostSerializer
    permission_classes = [IsAuthorOrReadOnly]
```
-----------------------------------
# blog > urls.py

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

# notice > urls.py

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('post', views.NoticePostViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
```
-----------------------------------
-----------------------------------
-----------------------------------
-----------------------------------
-----------------------------------
