python -m venv venv
./venv/Script/activate
pip install -r requirements.txt >> 모듈설치

django-admin startproject main .

## settings.py수정

ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

python manage.py migrate
python manage.py runserver 후 종료

python manage.py startapp blog

## settings.py수정

INSTALLED_APPS = [
...
'blog',
]

## main/urls.py

from django.urls import path, include

urlpatterns = [
path('', include('blog.urls')),
]

## blog/models.py

class Post(models.Model):
title = models.CharField(max_length=100)
content = models.TextField()
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateField(auto_now=True)

## blog/urls.py

from django.urls import path
from . import views
urlpatterns =[
path('blog/', views.PostList.as_view(), name='postlist'),
path('blog/<int:pk>/', views.PostDetail.as_view(), name='postdetail'),
]

## blog/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.db.models import Q

class PostList(ListView):

    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('q', '')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(author__icontains=keyword))

        return queryset

class PostDetail(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'

## settings.py

TEMPLATES = 'DIRS': [BASE_DIR / 'templates'],

## templates/blog/

### post_list.html

<!DOCTYPE html>
<html lang="ko-KR">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>글목록</title>
  </head>
  <body>
    <h2>글 목록</h2>
    <input type="text" name="q" id="search-input">
    <button id="search-btn">검색</button>
    <section class='contents-section'>
    {% if posts %}{% for i in posts %}
    <h2 class='contents-heading'>{{ i.title }}</h2>
    <p class='contents-text'>{{ i.content }}</p>
    <p class='contents-updated'>{{ i.updated_at }}</p>
    {% endfor %}
    {% else %} <p>게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!</p>
    {% endif %}
    </section>
  </body>
  <header></header>
  <footer></footer>
    <script>
      document.querySelector('#search-btn').addEventListener('click', () => {
          const searchInput = document.querySelector('#search-input');
          const searchValue = searchInput.value;
          location.href = `/blog/?q=${searchValue}`;
      });
  </script>
</html>

post_detail.html 생성

<!DOCTYPE html>
<html lang="ko-KR">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
  </head>
  <body>
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
    <p>{{ post.created_at }}</p>
  </body>
</html>

## blog/admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

python manage.py makemigrations
python manage.py migrate
어드민 페이지 들어가서 게시물 생성

## test.py작성

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class Test(TestCase):

    def test_connect(self):
        print('-- 접속확인 테스트 --')
        self.client = Client()

        print('-- /about 페이지 접속확인 --')
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.header
        body = soup.body
        footer = soup.footer

        self.assertIsNotNone(header)
        self.assertIsNotNone(body)
        self.assertIsNotNone(footer)


        print('-- /contact 페이지 접속확인 --')
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.header
        body = soup.body
        footer = soup.footer

        self.assertIsNotNone(header)
        self.assertIsNotNone(body)
        self.assertIsNotNone(footer)

        print('-- /blog 페이지 접속확인 --')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.header
        body = soup.body
        footer = soup.footer

        self.assertIsNotNone(header)
        self.assertIsNotNone(body)
        self.assertIsNotNone(footer)

    def test_postlist(self):
        print('-- 게시물 리스트 확인 --')

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        if Post.objects.count() == 0:
            # content >> list형식으로 들어옴
            content = soup.select('.contents-text')
            self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', content[0].text)

        print('-- 게시물 생성 --')
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.body.select('h2')
        print('h2태그 갯수: ', len(content))
        self.assertGreater(len(content), 0)



    def test_postdetail(self):
        print('-- 게시물 상세 페이지 확인 --')

        response = self.client.get('/blog/1')
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.select('.contents-heading')
        print(title)
```
