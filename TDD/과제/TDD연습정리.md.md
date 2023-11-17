# [과제] 11월 16일

**# [과제] 11월 16일**

## 과제

- 업로드 파일은 readme.md 파일
- readme.md 파일에는 가상환경 세팅부터 쳤던 명령어
- app은 하나
- 완성도 높은 블로그를 작성하는게 목적이 아니라 테스트 케이스 연습.

## URL 설계

| 이름 | URL | 비고 |
| --- | --- | --- |
| 메인 페이지 | / | main |
| 소개 페이지 | /about | main |
| 주소 페이지 | /contact | main |
| 블로그 페이지 | /blog | main, test 페이지 |
| 게시글 목록 | /blog |  |
| 게시글 상세보기 | /blog/<int:post_pk> | R |
| 게시글 검색 | /blog/?q=’keyword’ | 게시글 목록에서 구현 |
- model 설계

```python

class Post(models.Model):

title = models.CharField(max_length=100)

content = models.TextField()

created_at = models.DateTimeField(auto_now_add=True)

updated_at = models.DateField(auto_now=True)

```

- 요구사항

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

<aside>

💡 추가 테스트 구현은 자유입니다.

</aside>

# **Django 프로젝트 설정 및 테스트 가이드**

이 문서는 Django 프로젝트를 처음부터 설정하고, 테스트를 실행하는 방법을 단계별로 설명합니다.

## **프로젝트 설정**

1. **가상 환경 생성 및 활성화**
    
    ```bash
    python -m venv venv
    ./venv/Scripts/activate
    
    ```
    
2. **Django 설치**
    
    ```
    pip install django
    
    ```
    
3. **Django 프로젝트 및 앱 생성**
    
    ```css
    django-admin startproject tutorialdjango .
    python manage.py startapp main
    ```
    
4. **필요한 패키지 설치**
    - 필요한 추가 패키지가 있다면 이 단계에서 설치합니다.
    
    ```css
    pip freeze > requirements.txt
    pip install -r requirements.txt
    
    ```
    
5. **데이터베이스 마이그레이션**
    
    ```
    python manage.py migrate
    
    ```
    
6. **서버 실행 및 확인**
    
    ```
    python manage.py runserver
    
    ```
    
    - 브라우저에서 **`http://127.0.0.1:8000/`**을 열어 프로젝트가 정상적으로 작동하는지 확인합니다.


    

## Models.py

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
```

## Urls.py

```python
from django.urls import path
from .views import MainPageView, AboutPageView, ContactPageView, BlogListView, PostDetailView, BlogSearchView

urlpatterns = [
    path('', MainPageView.as_view(), name ='main'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('blog/search/', BlogSearchView.as_view(), name='blog_search')
]
```

## Templates

```python
#about.html
<!DOCTYPE html>
<html>
<head>
    <title>About</title>
</head>
<body>
    <header>
        <!-- 헤더 내용 -->
    </header>

    <main>
        <h1>About Us</h1>
        <!-- 소개 페이지 내용 -->
    </main>

    <footer>
        <!-- 푸터 내용 -->
    </footer>
</body>
</html>

#blog.html
<!DOCTYPE html>
<html>
<head>
    <title>About</title>
</head>
<body>
    <header>
        <!-- 헤더 내용 -->
    </header>

    <main>
        <h1>About Us</h1>
        <!-- 소개 페이지 내용 -->
    </main>

    <footer>
        <!-- 푸터 내용 -->
    </footer>
</body>
</html>

#contact.html
<!DOCTYPE html>
<html>
<head>
    <title>Contact</title>
</head>
<body>
    <header>
        <!-- 헤더 내용 -->
    </header>

    <main>
        <h1>Contact Us</h1>
        <!-- 연락처 정보 -->
    </main>

    <footer>
        <!-- 푸터 내용 -->
    </footer>
</body>
</html>

#index.html
<!DOCTYPE html>
<html>
<head>
    <title>Main Page</title>
</head>
<body>
    <header>
        <!-- 헤더 내용 -->
    </header>

    <main>
        <h1>Welcome to the Main Page</h1>
        <!-- 메인 페이지 내용 -->
    </main>

    <footer>
        <!-- 푸터 내용 -->
    </footer>
</body>
</html>

#post.html
<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
</head>
<body>
    <header>
        <!-- 헤더 내용 -->
    </header>

    <main>
        <h2>{{ post.title }}</h2>
        <p class='contents-updated'>{{ post.updated_at|date:"Y-m-d" }}</p>

        <!-- 포스트의 나머지 내용 -->
        <p class='contents-text'>{{ post.content }}</p>
        
    </main>

    <footer>
        <!-- 푸터 내용 -->
    </footer>
</body>
</html>
```

## Views.py

```python
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Post

class MainPageView(TemplateView):
    template_name = 'main/index.html'    

class AboutPageView(TemplateView):
    template_name = 'main/about.html'

class ContactPageView(TemplateView):
    template_name = 'main/contact.html'

class BlogListView(ListView):
    model = Post
    template_name = 'main/blog.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'main/post.html'
    context_object_name = 'post'

class BlogSearchView(ListView):
    model = Post
    template_name = 'main/blog.html'
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
```

## **테스트 설정 및 실행**

**테스트 코드 작성**
    - **`tests.py`** 파일에 테스트 클래스와 메소드를 작성합니다.
    
    ```python
    from django.test import TestCase, Client
    from .models import Post
    from bs4 import BeautifulSoup
    from datetime import datetime
    
    class BlogTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.post_001 = Post.objects.create(
                title='첫 번째 포스트입니다.',
                content='Hello World. We are the world.',
            )
            self.post_001.updated_at = datetime.now()
            self.post_001.save()
    
        def test_page_inheritance(self):
            pages = ['', '/about/', '/contact/', '/blog/']
            for page in pages:
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)
                soup = BeautifulSoup(response.content, 'html.parser')
                self.assertTrue(soup.find('header'))
                self.assertTrue(soup.find('body'))
                self.assertTrue(soup.find('footer'))
    
        def test_post_list(self):
            response = self.client.get('/blog/')
            soup = BeautifulSoup(response.content, 'html.parser')
    
            if Post.objects.count() == 0:
                self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', soup.body.text)
            else:
                self.assertTrue(len(soup.find_all('h2', class_='contents-heading')) >= 1)
    
        def test_post_detail(self):
            response = self.client.get(f'/blog/{self.post_001.id}/')
            soup = BeautifulSoup(response.content, 'html.parser')
    
            # 템플릿에 class 속성이 없는 경우
            h2_tag = soup.find('h2')
            self.assertIsNotNone(h2_tag)
            self.assertIn(self.post_001.title, h2_tag.text)
       # 기타 검증...
            self.assertIn(self.post_001.content, soup.find('p', class_='contents-text').text)
            self.assertIn(self.post_001.updated_at.strftime("%Y-%m-%d"), soup.find('p', class_='contents-updated').text)
    
            self.assertTrue(soup.find('header'))
            self.assertTrue(soup.find('body'))
            self.assertTrue(soup.find('footer'))
    ```

## Python [manage.py](http://manage.py) test