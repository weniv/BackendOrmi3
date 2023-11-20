# 목표
일반 게시판    /notice : 회원이 아닌 사람도 R 가능, 회원인 사람만 C
일반 게시판 상세보기    /notice/int:post_pk: 회원이 아닌 사람도 R 가능, 작성자만 UD 가능
게시글 목록    /blog : 회원인 사람만 R, C 가능
게시글 상세보기    /blog/int:post_pk: 회원인 사람만 R, 작성자만 UD 가능

###################################################################
```shell
py -3.11 -m venv venv
```
###################################################################
```shell
.\venv\Scripts\activate
```
###################################################################
```shell
pip install django
pip install djangorestframework
django-admin startproject project .
```
###################################################################
```python
# project > settings.py
...
ALLOWED_HOSTS = ['*']
...
```
###################################################################
```shell
python manage.py startapp main
python manage.py startapp blog
```
###################################################################
```python
# project > settings.py
...
INSTALLED_APPS = [
    ...
    'rest_framework',
    'main',
    'blog',
]
...
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False
...
```
###################################################################
```python
# project > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
]
```
###################################################################
```python
# main > urls.py
from django.urls import path, include
from . import views

urlpatterns = [
]
```
###################################################################
```python
# blog > urls.py
from django.urls import path, include
from . import views

urlpatterns = [
]
```
###################################################################
```python
# main > models.py
from django.db import models
from django.conf import settings

class Notice(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
###################################################################
```python
# blog > models.py
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
###################################################################
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
###################################################################
```python
# main > tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Notice

class NoticeTest(TestCase):
    def setUp(self):
        print('-- main app 테스트 BEGIN --')
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = 'byeong',
            password = 'qudgjs01!@',
        )

    def test_notice_read(self):
        '''
        회원이 아닌 사람이 notice를 읽으려 할 때
        notice Read 가능 테스트
        '''
        print('-- notice read 테스트 BEGIN --')
        response = self.client.get('/notice/')
        self.assertEqual(response.status_code, 200)
        print('-- notice read 테스트 END --')

    def test_notice_member(self):
        '''
        회원인 사람만 notice CUD 가능 테스트
        '''
        print('-- notice 회원 CUD 테스트 BEGIN')
        self.client.force_authenticate(user=self.user)
        self.user.save()
        response = self.client.post('/notice/', {'title': 'test title', 'content': 'test content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.put(f'/notice/1/', {'title': 'update title', 'content': 'update_content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(f'/notice/1/')
        self.assertEqual(response.status_code, 204)
        print('-- notice 회원 CUD 테스트 END')

    def test_notice_nonmember(self):
        '''
        비회원인 사람은 notice CUD 불가능 테스트
        '''
        print('-- notice 비회원 CUD 테스트 BEGIN')
        response = self.client.post('/notice/', {'title': 'test title', 'content': 'test content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.put(f'/notice/1/', {'title': 'update title', 'content': 'update_content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f'/notice/1/')
        self.assertEqual(response.status_code, 403)
        print('-- notice 비회원 CUD 테스트 END')
```
###################################################################
```python
# main > serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Notice

class NoticeSerializers(ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
```
###################################################################
```python
# main > views.py
from rest_framework.viewsets import ModelViewSet
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
```
###################################################################
```python
# main > permissions.py
from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    # 인증이 되어있는지 확인하여 조회만 가능하게 하고, 작성자만 수정, 삭제가 가능하게 합니다.
    def has_permission(self, request, view):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 True
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
```
###################################################################
```python
# main > views.py
from rest_framework.viewsets import ModelViewSet
from .models import Notice
from .serializers import NoticeSerializer
from .permissions import IsAuthenticatedOrReadOnly

class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```
###################################################################
```python
# blog > tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post

class PostTest(TestCase):
    def setUp(self):
        print('-- post app 테스트 BEGIN --')
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = 'byeong',
            password = 'qudgjs01!@',
        )

    def test_post_member(self):
        '''
        회원
        post CR 가능
        작성자만 UD 가능
        '''
        print('-- post 회원 CRUD 테스트 BEGIN')
        self.client.force_authenticate(user=self.user)
        self.user.save()

        response = self.client.get('/blog/post/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/blog/post/', {'title': 'test title', 'content': 'test content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.put(f'/blog/post/1/', {'title': 'update title', 'content': 'update_content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(f'/blog/post/1/')
        self.assertEqual(response.status_code, 204)
        print('-- post 회원 CRUD 테스트 END')

    def test_post_nonmemer(self):
        '''
        비회원
        CRUD 모두 권한 없음
        '''
        response = self.client.get('/blog/post/')
        self.assertEqual(response.status_code, 403)

        Post.objects.create(title='1', content='11').save()
        response = self.client.post('/blog/post/', {'title': 'test title', 'content': 'test content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.put(f'/blog/post/1/', {'title': 'update title', 'content': 'update_content', 'author': self.user.pk}, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f'/blog/post/1/')
        self.assertEqual(response.status_code, 403)
```
###################################################################
```python
# blog > serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```
###################################################################
```python
# blog > permissions.py
from rest_framework import permissions


class IsAuthorOrCreateRead(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        '''
        회원은 읽기, 작성 가능
        작성자는 수정, 삭제 가능
        '''
        if request.method in permissions.SAFE_METHODS + ('POST'):
            return True
        return obj.author == request.user
```
###################################################################
```python
# blog > views.py
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrCreateRead

class NoticeViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrCreateRead]
```
###################################################################
```python
# blog > urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]