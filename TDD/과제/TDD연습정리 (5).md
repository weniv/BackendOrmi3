# 가상환경 설정

1. 가상환경 설정
```
python -m venv venv
```
2. 가상환경 실행  
```
./venv/scripts/activate
```
3. Django 설치  
```
pip install django
```

# 프로젝트 생성
```
django-admin startproject django_TDD .
```
1. DB 마이그레이트  
```
python manage.py migrate
```
2. main 앱 생성  
```
python manage.py startapp main
```
3. django_TDD > settings.py 수정  
```
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    "blog",
]

TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR/'templates'],
        ...
    },
]
```
# Model 작성
1. blog > models.py
```
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

2. model 변경사항 반영
```
python manage.py makemigrations
python manage.py migrate
```

3. admin 페이지 등록
blog > admin.py
```
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

# URL 작성
1. django_TDD > urls.py
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

```

2. main > urls.py
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.PostList.as_view(), name='blog'),
    path('blog/<int:pk>', views.PostDetail.as_view(), name='postdetail'),
    path('write/', views.PostCreate.as_view(), name='postwrite'),
]
```

# test 작성

## 요구사항
- 접속 확인
    - /
    - /about
    - /contact
    - /blog
- 상속확인
    - 위 4개 페이지에서 header, body, footer가 제대로 상속 되는지 확인
- 게시물 리스트 확인
    - 게시물이 없으면 ‘게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!’가 출력되어야 합니다.
    - 게시물이 있으면 h2가 1개 이상이어야 합니다.
    - 게시물 작성은 아래 구조로 되어 있습니다.
        
        ```html
        <section class='contents-section'>
            <h2 class='contents-heading'>제목</h2>
            <p class='contents-text'>내용</p>
            <p class='contents-updated'>최종수정날짜</p>
        </section>
        ```
        
- 게시물 상세페이지 확인
    - 제목 자리에 제목이 들어있는지
    - 내용 자리에 내용이 들어있는지
    - 최종 수정 날짜에 수정날짜가 들어가 있는지
    - 상속이 제대로 이뤄져 있는지
        - 메뉴, 푸터

1. main > test.py
```python
from django.test import TestCase
from bs4 import BeautifulSoup
from .models import Post

class TestTDD(TestCase):
    def setUp(self):
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
    
    def test_main(self):
        print('접속 확인')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_templecheck(self):
        print('상속 확인')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.header.text, '헤더')
        self.assertEqual(soup.footer.text, '푸터')

    def test_postlist(self):
        print('게시물 리스트 확인')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        if Post.objects.count() == 0:
            print('게시물이 없는 경우')
            self.assertIn('첫번째 게시물에 주인공이 되세요!', soup.body.text)
        else:
            print('게시물이 있는 경우')
            print(Post.objects.count())
            print(len(soup.body.select('h2')))
            print(soup.body.select('p'))

    def test_postdetail(self):
        print('게시물 상세 확인')
        response = self.client.get('/blog/1')
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.body.select('.contents-heading'))
        print(soup.body.select('.contents-text'))
        print(soup.body.select('.contents-updated'))
        self.assertEqual(soup.header.text, '헤더')
        self.assertEqual(soup.footer.text, '푸터')
```

# views.py 작성

1. main > views.py
```
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Post
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')


class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/bloglist.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get('q')

        if search_keyword:
            # queryset = queryset.filter(title__icontains=search_keyword)
            # distinct()는 중복을 제거합니다.
            # Q는 |(or), &(and), ~(not) 연산자를 사용할 수 있습니다.
            # icontains는 대소문자를 구분하지 않는 검색입니다.
            queryset = queryset.filter(
                Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword)).distinct()

        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        return context
    
class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/blog/'

    def form_valid(self, form):
        post = form.save(commit=False)
        return super().form_valid(form)
```

# 템플릿 작성

1. templates 파일 생성

2. templates > base.html
```
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <header class="headera">헤더</header>
    {% block content %}{% endblock %}
    <footer class="footera">푸터</footer>
</body>
</html>
```

3. templates > blog > bloglist.html
```
{% extends 'base.html' %}
{% block content %}
{% load static %}
    <h1>blog</h1>
    <input type="text" name="q" id="search-input">
    <button id="search-btn">검색</button>
    {% if post_list.exists %}
        {% for post in post_list %}
            <section class="contents-section">
                <h2 class='contents-heading'>{{ post.title }}</h2>
                <p class='contents-text'>{{ post.content }}</p>
                <p class='contents-updated'>{{ post.updated_at }}</p>
            </section>
        {% endfor %}
    {% else %}
        <p>글이 없습니다.</p>
    {% endif %}
    <script>
        document.querySelector('#search-btn').addEventListener('click', () => {
            const searchInput = document.querySelector('#search-input');
            const searchValue = searchInput.value;
            location.href = `/blog/?q=${searchValue}`;
        });
    </script>
{% endblock %}
```

4. templates > blog > post_detail.html

```
{% extends 'base.html' %}
{% block content %}
{% load static %}
    <section class='contents-section'>
        <h2 class='contents-heading'>{{post.title}}</h2>
        <p class='contents-text'>{{post.content}}</p>
        <p class='contents-updated'>{{post.updated_at}}</p>
    </section>
{% endblock %}
```

# test 실행
```
python manage.py test
```