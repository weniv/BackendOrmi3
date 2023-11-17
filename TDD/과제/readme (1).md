# TDD 과제 11.16

### 가상환경생성
```
python -m venv venv
```

### 가상환경 접속
```
source venv/bin/activate
```

### 장고프로젝트 생성
```
mkdir tddproject
cd tddproject

django-admin startproject tdd_django .
```

### migrate
```
python manage.py migrate
```

### app 생성
```
django-admin startapp main
```

### settings.py 
```python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
  
    'main'
]
```

### urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]
```

### main/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.detail, name='detail'),
    
]
```

### main/views.py
```python
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

from django.utils.text import slugify
from django.db.models import Q

def main(request):
  return render(request, 'main/index.html')

def about(request):
  return render(request, 'main/about.html')

def contact(request):
  return render(request, 'main/contact.html')




class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'main/blog.html'

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
    template_name = 'main/detail.html'



blog = PostList.as_view()
detail = PostDetail.as_view()

```

### templates 생성
- templates/main/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <p>index</p>
</body>
</html>
```
- templates/main/contact.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <p>contact</p>
</body>
</html>
```
- templates/main/about.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <p>about</p>
</body>
</html>
```
- templates/main/blog.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
</head>
<body>
    <h1>blog</h1>
    <input type="text" name="q" id="search-input">
    <button id="search-btn">검색</button>
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">About</a></li>
        </ul>
    </nav>
    <main id="main">
      <section class='contents-section'>
        {% if post_list.exists %}
        {% for post in post_list %}
            <h2 class='contents-heading'>{{ post.title }}</h2>
            <p class='content-text'>{{ post.content | truncatewords:45 }}</p>
            <p class='contents-updated'>{{ post.updated_at }}</p>
        {% endfor %}
        {% else %}
            <p>게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!</p>
        {% endif %}
      </section>
    </main>
    <script>
        document.querySelector('#search-btn').addEventListener('click', () => {
            const searchInput = document.querySelector('#search-input');
            const searchValue = searchInput.value;
            location.href = `/blog/?q=${searchValue}`;
        });
    </script>
</body>
</html>
```
- templates/main/detail.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <!-- fontawesome cdn -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<body>
    <h1>detail</h1>
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">About</a></li>
        </ul>
    </nav>
    <main id="main">
    <h2 class='contents-heading'>{{ post.title }}</h2>
    <p class='contents-text'>{{ post.content }}</p>
    <p class='contents-updated'>{{ post.updated_at|date:'Y.m.d' }}</p>
    </main>

</body>
</html>
```

### main/models.py
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

### makemigrations / migrate
```
python manage.py makemigrations
python manage.py migrate
```

### 접속확인
- main/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    
    self.urls = ['/', '/about/', '/contact/', '/blog/']
  
  def test_get_page(self):
    # 1. 접속 확인
    for url in self.urls:
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
```

### 상속확인
- main/test.py
```python
class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    
    self.urls = ['/', '/about/', '/contact/', '/blog/']
  def test_implements(self):
    # 2. 상속
    for url in self.urls:
      response = self.client.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      self.assertIsNotNone(soup.header)
      self.assertIsNotNone(soup.body)
      self.assertIsNotNone(soup.footer)
```

### 게시물 리스트 확인
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    
    post_001 = Post.objects.create(
        title = '첫 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
    post_002 = Post.objects.create(
        title = '두 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
  def test_post_list(self):
    response = self.client.get('/blog/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if Post.objects.count() == 0:
        self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', soup.body.text)
    else:
        self.assertGreater(len(soup.body.select('h2')), 1)
```

### 게시물 상세페이지 확인
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    post_001 = Post.objects.create(
        title = '첫 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
    post_002 = Post.objects.create(
        title = '두 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
  def test_post_detail(self):
    post = Post.objects.get(pk=1)
    response = self.client.get('/blog/1/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    self.assertEqual(soup.find('h2', class_='contents-heading').text, post.title)
    self.assertEqual(soup.find('p', class_='contents-text').text, post.content)
    self.assertEqual(soup.find('p', class_='contents-updated').text, post.updated_at.strftime('%Y.%m.%d'))
    self.assertIsNotNone(soup.header)
    self.assertIsNotNone(soup.body)
    self.assertIsNotNone(soup.footer)
```

### 검색
- main/tests.py
```python
class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    post_001 = Post.objects.create(
        title = '첫 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
    post_002 = Post.objects.create(
        title = '두 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
  def test_post_search(self):
    # 검색
    search_str = '첫 번째'
    response = self.client.get('/blog/?q='+search_str)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    self.assertEqual(soup.find('h2', class_='contents-heading').text, self.post_001.title)
    self.assertIn(search_str, soup.body.text)
```

### 최종 main/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

class TestMain(TestCase):
  def setUp(self):
    self.client = Client()
    
    self.urls = ['/', '/about/', '/contact/', '/blog/']
    self.post_001 = Post.objects.create(
        title = '첫 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
    self.post_002 = Post.objects.create(
        title = '두 번째 포스트입니다.',
        content = 'Hello World. We are the world.',
    )
  def test_get_page(self):
    
    # 1. 접속 확인
    # /
    for url in self.urls:
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
      
  def test_implements(self):
    # 2. 상속
    for url in self.urls:
      response = self.client.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      self.assertIsNotNone(soup.header)
      self.assertIsNotNone(soup.body)
      self.assertIsNotNone(soup.footer)
  
  def test_post_list(self):
    # 3. 게시물리스트 확인
    response = self.client.get('/blog/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if Post.objects.count() == 0:
        self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', soup.body.text)
    else:
        self.assertGreater(len(soup.body.select('h2')), 1)
        
  def test_post_detail(self):
    # 게시물 상세페이지 확인
    post = Post.objects.get(pk=1)
    response = self.client.get('/blog/1/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    self.assertEqual(soup.find('h2', class_='contents-heading').text, post.title)
    self.assertEqual(soup.find('p', class_='contents-text').text, post.content)
    self.assertEqual(soup.find('p', class_='contents-updated').text, post.updated_at.strftime('%Y.%m.%d'))
    self.assertIsNotNone(soup.header)
    self.assertIsNotNone(soup.body)
    self.assertIsNotNone(soup.footer)
  
  def test_post_search(self):
    # 검색
    search_str = '첫 번째'
    response = self.client.get('/blog/?q='+search_str)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    self.assertEqual(soup.find('h2', class_='contents-heading').text, self.post_001.title)
    self.assertIn(search_str, soup.body.text)
    
```