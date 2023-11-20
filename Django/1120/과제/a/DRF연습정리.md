## 가상환경 설정
```zsh
python3 -m venv venv
source ./venv/bin/activate

pip install django
pip install djangorestframework
```

## 프로젝트 생성
```zsh
django-admin startproject drftutorial .
python3 manage.py startapp notice
python3 manage.py startapp blog
```

## 프로젝트 설정
```py
drftutorial > settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'notice',
    'rest_framework'
]

REST_FRAMEWORK = {

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',  # 1000번의 요청을 하루에 할 수 있습니다.
        # 비인증 요청 거부는 views.py에서 처리합니다.
    }
}
```

## drftutorial > urls.py

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blog.urls')),
    path('', include('notice.urls')),
]

```

## blog > models.py

```py

from django.conf import settings
from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

```

## 마이그레이션

``` shell
python3 manage.py makemigrations
python3 manage.py migrate
```

## urls.py

```py
# notice > urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('notice', views.NoticeViewset)

urlpatterns = [
    path('', include(router.urls)),
]

```

```py
#blog > urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('blog', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```

## serializers.py
```py
#blog > serializers.py

from rest_framework.serializers import ModelSerializer
from .models import Post
from django.contrib.auth import get_user_model


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

## views.py

``` py
# notice > views.py

from rest_framework.viewsets import ModelViewSet
from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class NoticeViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

```


```py
# blog> views.py

from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

```

## permissions.py
```py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    # 인증이 되어있는지 확인하여 조회만 가능하게 하고, 작성자만 수정, 삭제가 가능하게 합니다.
    def has_permission(self, request, view):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 리턴합니다.
        '''
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

## 테스트

### notice

- 인증되지 않은 사용자
    - http://127.0.0.1:8000/notice/ | GET 
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/ | POST
        - ```bash
            Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | GET
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | PUT
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | DELETE
        - ``` bash
            Status: 403 Forbidden
            ```

- 인증된 사용자

    - http://127.0.0.1:8000/notice/ | GET 
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/ | POST
        - ```bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | GET
        - ``` bash
            Status: 200 OK
            ```

- 인증된 사용자 (작성자 O)
    - http://127.0.0.1:8000/notice/int:post_pk/ | PUT
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | DELETE
        - ``` bash
            Status: 200 OK
            ```

- 인증된 사용자 (작성자 X)
    - http://127.0.0.1:8000/notice/int:post_pk/ | PUT
        - ``` bash
            Status: 403 Forbidden            
            ```

    - http://127.0.0.1:8000/notice/int:post_pk/ | DELETE
        - ``` bash
            Status: 403 Forbidden
            ```

### blog

- 인증되지 않은 사용자
    - http://127.0.0.1:8000/blog/ | GET 
        - ``` bash
            Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/blog/ | POST
        - ```bash
            Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | GET
        - ``` bash
            Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | PUT
        - ``` bash
            Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | DELETE
        - ``` bash
            Status: 403 Forbidden
            ```

- 인증된 사용자

    - http://127.0.0.1:8000/blog/ | GET 
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/blog/ | POST
        - ```bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | GET
        - ``` bash
            Status: 200 OK
            ```

- 인증된 사용자 (작성자 O)
    - http://127.0.0.1:8000/blog/int:post_pk/ | PUT
        - ``` bash
            Status: 200 OK
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | DELETE
        - ``` bash
            Status: 200 OK
            ```

- 인증된 사용자 (작성자 X)
    - http://127.0.0.1:8000/blog/int:post_pk/ | PUT
        - ``` bash
             Status: 403 Forbidden
            ```

    - http://127.0.0.1:8000/blog/int:post_pk/ | DELETE
        - ``` bash
            Status: 403 Forbidden
            ```
