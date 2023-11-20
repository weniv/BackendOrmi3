$ python -m venv venv
$ cd 1120
$ mkdir DRF_training
$ cd DRF_training
$ ./venv/Script/activate

pip install django
pip install djangorestframework

django-admin startproject drfproject .
python manage.py startapp blog 
python manage.py startapp notice

----------------------------------------------------------------
# drfproject > settings.py

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'rest_framework',
    'blog',
    'accounts',
]

'
'
'

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True
USE_TZ = False

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

----------------------------------------------------------------
# drfproject > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls')),
    path('notice/', include('notice.urls')),
]

----------------------------------------------------------------
--------------------------- notice -----------------------------
----------------------------------------------------------------
# notice > models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

----------------------------------------------------------------

python manage.py makemigrations
python manage.py migrate

----------------------------------------------------------------

# notice > serializers.py

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

----------------------------------------------------------------
# notice > urls.py

from django.urls import include, path
from . import views

urlpatterns = [
    path('post/', views.post_list),
    path('post/<int:pk>/', views.post_detail), 
    path('post/new/', views.post_new), 
]

----------------------------------------------------------------
# notice > models.py

from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

----------------------------------------------------------------

python manage.py makemigrations
python manage.py migrate
1
1

----------------------------------------------------------------
# notice > permissions.py

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

----------------------------------------------------------------
# notice > views.py

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

post_list = PostListAPIView.as_view()

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

post_detail = PostDetailAPIView.as_view()

class PostNewAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

post_new = PostNewAPIView.as_view()

----------------------------------------------------------------
--------------------------- blog -------------------------------
----------------------------------------------------------------
# blog > models.py

from django.db import models
from django.conf import settings

class Postblog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

----------------------------------------------------------------

python manage.py makemigrations
python manage.py migrate

----------------------------------------------------------------
# blog > serializers.py

from rest_framework.serializers import ModelSerializer
from .models import Postblog
from django.contrib.auth import get_user_model

class PostSerializer(ModelSerializer):
    class Meta:
        model = Postblog
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

----------------------------------------------------------------
# blog > views.py

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Postblog
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Postblog.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


----------------------------------------------------------------
# blog > urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

----------------------------------------------------------------
# notice > permissions.py

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

----------------------------------------------------------------
----------------------------------------------------------------
----------------------------------------------------------------
----------------------------------------------------------------
----------------------------------------------------------------
