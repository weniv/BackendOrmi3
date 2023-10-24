```
mkdir router
cd router

django-admin startproject tutorialdjango .
python manage.py migrate

# settings.py에서 접속할 수 있는 사람 설정
ALLOWED_HOSTS = ['*'] # 28번째 줄에 접속할 수 있는 사람을 모든 사람으로 변경

python manage.py startapp book

# settings.py 에서 33번째 라인 수정
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book',
]

###################################

python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준123!@

###################################
# book > models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)

    def __str__(self):
        return self.title

###################################

python manage.py makemigrations
python manage.py migrate

###################################

# tutorialdjango > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
]

###################################
# book > urls.py

from django.urls import path
from . import views

urlpatterns = []

###################################
# book > admin.py

from django.contrib import admin
from .models import Book

admin.site.register(Book)

###################################

# runserver로 게시물 3개 생성

###################################
book > serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

###################################
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'book',
]

###################################
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() # CRUD 대상이 되는 데이터를 지정
    serializer_class = BookSerializer

###################################

http://127.0.0.1:8000/book/
http://127.0.0.1:8000/book/1/

http://127.0.0.1:8000/book/book. => 없기 때문에 전체 url 구조를 받을 수 있습니다.
router로 자동 생성이 된 url구조

admin/
book/ ^$ [name='book-list']
book/ ^\.(?P<format>[a-z0-9]+)/?$ [name='book-list']
book/ ^(?P<pk>[^/.]+)/$ [name='book-detail']
book/ ^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='book-detail']
book/ ^$ [name='api-root']
book/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']

###################################

공식 문서 : https://www.django-rest-framework.org/api-guide/viewsets/#viewset

###################################
# views.py

from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = Book.objects.all() # CRUD 대상이 되는 데이터를 지정
    serializer_class = BookSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user) # user는 현재 로그인한 사용자
    # 이렇게 사용할 것이면 model에 user 필드가 있어야 합니다.


###################################

http://127.0.0.1:8000/book/ => 게시물 1개 새로 생성
http://127.0.0.1:8000/admin/ => 로그아웃
http://127.0.0.1:8000/book/ => 로그인이 안되어 있어 조회가 안됨

###################################

앞에서 했었던 token방식에 인증 코드 그대로 router방식에 합치면
token방식에 로그인이 됩니다.

DRF에서 제공하는 token말고 JWT 사용해서 인증을 하실 수도 있습니다.

```