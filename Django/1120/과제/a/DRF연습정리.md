이름               |  URL                   |  GET	    |     POST    |      PUT        |  DELETE
일반 게시판         | /notice                |   O	     |    회원(O)  |  회원+작성자(O)  | 회원+작성자(O)
일반 게시판 상세보기 | /notice/<int:post_pk>  |   O	      |     -	    |  회원+작성자(O) | 회원+작성자(O)
게시글 목록         | /blog                  |  회원(O)	  |    회원(O)  | 회원+작성자(O)  | 회원+작성자(O)
게시글 상세 보기    | /blog/<int:post_pk>/   |  회원(O)	  |      -	    | 회원+작성자(O)  | 회원+작성자(O)

# 초기 세팅
mkdir mysite
cd mysite

python -m venv venv
.\venv\Scripts\activate

pip install django
pip install djangorestframework

django-admin startproject tutorialdrf .
python manage.py migrate

python manage.py startapp blog

# settings.py
...생략...
ALLOWED_HOSTS = ['*']
...생략...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		# library
    'rest_framework',
		# custom app
    'blog',
]
...생략...
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

# tutorialdrf > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blog.urls')),
]

# blog > models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# blog > serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# blog > views.py
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer

class NoticeViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# blog > urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('notice', views.NoticeViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]

# blog > admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)

# DB 반영
python manage.py makemigrations
python manage.py migrate

# superuser 생성
python manage.py create superuser

# runserver
python manage.py runserver

# 중간 점검 
# 127.0.0.1:8000/notice/ 에서 모든 사람이 GET, POST, PUT, DELETE 가 가능
# 요구사항: /notice 에서는 회원이 아닌 사람도 Read(GET) 가능, 회원인 사람만 Create(POST), 작성자만 Update(PUT), Delete(DELETE) 가능

# blog > permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''
		회원이 아닌 사람도 Read(GET) 가능, 회원인 사람만 Create(POST), 
		작성자만 Update(PUT), Delete(DELETE) 가능
		'''
    def has_permission(self, request, view):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 
				리턴합니다.
        '''
        if request.user:
            return True
        
    def has_object_permission(self, request, view, obj):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 
				리턴합니다. 
				그 외 요청(PUT, DELETE)에 대해서는 작성자에 한해서만 
				True를 리턴합니다.
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# blog > views.py
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class NoticeViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
# 확인 127.0.0.1:8000/notice/ 에서 회원이 아닌 사람도 Read(GET) 가능, 회원인 사람만 Create(POST), 작성자만 Update(PUT), Delete(DELETE) 가능

# 여기서부터는 Blog입니다.
# blog > models.py
...생략...
class Blogpost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# blog > urls.py
...생략...

blogrouter = DefaultRouter()
blogrouter.register('blog', views.BlogViewSet) 

urlpatterns = [
		...생략...
    path('', include(blogrouter.urls)),
]

# blog > views.py
...생략...
class BlogViewSet(ModelViewSet):
    queryset = Blogpost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

# blog > serializers.py
...생략...
class BlogPostSerializer(ModelSerializer):
    class Meta:
        model = Blogpost
        fields = [
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

# 확인 127.0.0.1:8000/blog/ 에서 회원인 사람만 Read(GET), Create(POST) 가능, 작성자만 Update(PUT), Delete(DELETE) 가능
