# TDD 연습정리
남영훈

## 순서
1. 가상환경 설정
2. 프로젝트 생성
3. 프로젝트 기본 설계
4. Model 작성
5. Urls, Views, Templates 작성
6. Test 코드 작성
7. Test 진행
8. Test 결과

## 가상환경 설정
1. 프로젝트 디렉터리 생성  
```
mkdir assignment
```

2. 가상환경 설정  
```
python -m venv venv
```

3. 가상환경 실행  
```
source venv/bin/activate
```

4. Django 설치  
```
pip install django
```

5. 프로젝트 디렉터리로 이동  
```
cd assingment
```

## 프로젝트 생성
```
django-admin startproject assignment .
```

## 프로젝트 기본 설계
1. DB 마이그레이트  
```
python manage.py migrate
```

2. Blog 앱 생성  
```
python manage.py startapp blog
```

3. assignment > settings.py 수정  
```python
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

4. 서버 실행 확인
```
python manage.py runserver
```

## Model 작성
1. blog > models.py
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```
2. model 변경사항 반영
```python
python manage.py makemigrations
python manage.py migrate
```
3. admin 페이지 등록
blog > admin.py
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## Urls, Views, Templates 작성
1. assignment > urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('blog.urls')),
]
```

2. blog > urls.py
```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>', views.blog_detail, name='blog_detail'),
]
```

3. blog > views.py
```python
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post
from django.db.models import Q

class IndexView(TemplateView):
    template_name = 'blog/index.html'

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class ContactView(TemplateView):
    template_name = 'blog/contact.html'

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q', '')
        if q:
            queryset = Post.objects.filter(
                Q(title__icontains=q)
            )

        return queryset

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


index = IndexView.as_view()
about = AboutView.as_view()
contact = ContactView.as_view()
blog_list = PostListView.as_view()
blog_detail = PostDetailView.as_view()
```

4. Templates 작성
- base.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Main</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>

</head>
<body>
    <!-- navbar -->
    <header>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'blog:index' %}">TDD TEST</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="{% url 'blog:index' %}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'blog:about' %}">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'blog:contact' %}">Contact</a>
                </li>
                </ul>
            </div>
            </div>
        </nav>
    </header>
    <!-- //navbar -->
    {% block contents %}
    {% endblock %}
    <!-- footer -->
    <footer class="footer mt-auto p-3 bg-white" style="bottom: 0;">
        <div class="d-flex container-fluid justify-content-between">
            <span class="text-muted fs-5">Copyright 2023. 남영훈 all rights reserved.</span>
            
        </div>
    </footer>
		<!-- //footer -->
</body>
</html>
```
- blog > index.html
```html
{% extends 'base.html' %}
{% block contents %}
<main>
    <div>
        Main 페이지 입니다.
    </div>
</main>
{% endblock %}
```
- blog > about.html
```html
{% extends 'base.html' %}
{% block contents %}
<main>
    <div>
        About 페이지 입니다.
    </div>
</main>
{% endblock %}
```
- blog > contact.html
```html
{% extends 'base.html' %}
{% block contents %}
<main>
    <div>
        Contact 페이지 입니다.
    </div>
</main>
{% endblock %}
```

- blog > post_list.html
```html
{% extends 'base.html' %}
{% block contents %}
<main>
    <form method="get">
        <div>
            <div class="row g-2">
                <div class="col">
                    <input class="form-control" type="search" name="q">
                </div>
                <div class="col">
                    <button class="btn btn-primary" type="submit">검색하기</button>
                </div>
            </div>
        </div>
    </form>
    {% if posts %}
        {% for post in posts %}
        <div>
            <section class='contents-section'>
                <h2 class='contents-heading'>{{ post.title }}</h2>
                <p class='contents-text'>{{ post.content }}</p>
                <p class='contents-updated'>{{ post.updated_at }}</p>
            </section>
        </div>
        {% endfor %}
    {% else %}
    <p>게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!</p>
    {% endif %}
</main>
{% endblock %}
```

- blog > post_detail.html
```html
{% extends 'base.html' %}
{% block contents %}
<main>
    <div>
        <section class='contents-section'>
            <h2 class='contents-heading'>{{ post.title }}</h2>
            <p class='contents-text'>{{ post.content }}</p>
            <p class='contents-updated'>{{ post.updated_at }}</p>
        </section>
    </div>
</main>
{% endblock %}
```

## Test 코드 작성
blog > tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class Test(TestCase):
    def setUp(self):
        '''
        테스트를 위해 새로운 클라이언트 생성
        '''

        self.client = Client()

    def test_connection(self):
        '''
        접속 상태 확인 테스트를 진행합니다
        '''

        print('---Main 페이지 접속 테스트---')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        print('---About 페이지 접속 테스트---')
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

        print('---Contact 페이지 접속 테스트---')
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        print('---About 페이지 접속 테스트---')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_template_inheritance(self):
        '''
        base.html에 대한 템플릿 상속 테스트를 진행합니다
        '''
        
        print('---Main 페이지 상속 테스트---')
        response = self.client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.find('header'))
        self.assertTrue(soup.find('body'))
        self.assertTrue(soup.find('footer'))

        print('---About 페이지 상속 테스트---')
        response = self.client.get('/about/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.find('header'))
        self.assertTrue(soup.find('body'))
        self.assertTrue(soup.find('footer'))

        print('---Contact 페이지 상속 테스트---')
        response = self.client.get('/contact/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.find('header'))
        self.assertTrue(soup.find('body'))
        self.assertTrue(soup.find('footer'))

        print('---Blog 페이지 상속 테스트---')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.find('header'))
        self.assertTrue(soup.find('body'))
        self.assertTrue(soup.find('footer'))

    def test_blog_list(self):
        '''
        게시물 목록에 값이 있을 경우를 테스트합니다.
        '''

        print('---Blog 페이지 리스트에 게시물이 있을 경우 테스트---')
        # Post 값 2개 넣기
        post_001 = Post.objects.create(
            title= '첫번째 게시물 제목입니다.',
            content= '첫번째 게시물 내용입니다.',
        )
        post_002 = Post.objects.create(
            title= '두번째 게시물 제목입니다.',
            content= '두번째 게시물 내용입니다.',
        )
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # 제목에 해당하는 태그 h2가 1개보다 많은 지 체크
        self.assertGreater(len(soup.body.select('h2')), 1)
        
    def test_blog_list_empty(self):
        '''
        게시물 목록이 비어져있을 경우를 테스트합니다
        '''

        print('---Blog 페이지 리스트가 비어져있을 경우 테스트---')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # Post 객체의 갯수가 0이라면, 게시물 없음 안내 문구 체크
        if Post.objects.count() == 0:
            self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', soup.body.text)
        
    def test_blog_detail(self):
        '''
        게시물 상세 페이지에 제목, 내용, 수정날짜 대해 검증합니다
        '''

        print('---Blog 상세 페이지 테스트---')
        # Post 값 넣기
        post_001 = Post.objects.create(
            title= '첫번째 게시물 제목입니다',
            content= '첫번째 게시물 내용입니다',
        )
        response = self.client.get('/blog/1')
        soup = BeautifulSoup(response.content, 'html.parser')

        # class 이름을 통해 제목, 내용, 수정날짜 가져오기
        title = soup.select('.contents-heading')[0].text
        content = soup.select('.contents-text')[0].text
        updated_at = soup.select('.contents-updated')[0].text

        # 넣은 값과 비교, 수정날짜는 정확히 알 수 없기 때문에 값 존재유무 판단
        self.assertIn('첫번째 게시물 제목입니다', title)
        self.assertIn('첫번째 게시물 내용입니다', content)
        self.assertTrue(updated_at)

    def test_blog_detail_template(self):
        '''
        게시물 상세 페이지 내 base.html 상속에 대한 테스트를 진행합니다
        '''
        print('---Blog 상세 페이지 상속 테스트---')
        # Post 값 넣기
        post_001 = Post.objects.create(
            title= '첫번째 게시물 제목입니다',
            content= '첫번째 게시물 내용입니다',
        )
        response = self.client.get('/blog/1')
        soup = BeautifulSoup(response.content, 'html.parser')

        # 헤더, 바디, 푸터 태그 존재유무 판단
        self.assertTrue(soup.find('header'))
        self.assertTrue(soup.find('body'))
        self.assertTrue(soup.find('footer'))
```

## Test 진행
```
python manage.py test
```

## Test 결과
![test](https://github.com/Nam-Younghoon/travelog/assets/58909988/ce37adb8-4656-4d1e-923a-b57ebe54f73f)