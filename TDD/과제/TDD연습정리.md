### 가상환경 설치  
```
python -m venv venv
```

### 가상환경 진입
```
.\venv\Scripts\activate
```

### 라이브러리 설치
```
pip install django
pip install bs4
```

### 장고 프로젝트 생성
```
django-admin startproject django_blog .
```

### django_blog > settings.py
```
...
ALLOWED_HOSTS = ['*']
...
```

### 장고 앱 생성
```
python manage.py startapp blog
```

### django_blog > settings.py
```
...
INSTALLED_APPS = [
    ...
    'blog',
]
...
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
...

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
...
```

### 마이그레이트
```
python manage.py migrate
```

### 슈퍼 유저 생성
python manage.py createsuperuser

### 프로젝트 url
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

### blog > urls.py
```
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.about, name='about'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
]
```

### blog > views.py
```
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

class IndexView(View):
    pass

class AboutView(View):
    pass

class ContactView(View):
    pass

class PostListView(ListView):
    pass

class PostDetailView(DetailView):
    pass

index = IndexView.as_view()
about = AboutView.as_view()
contact = ContactView.as_view()
post_list = PostListView.as_view()
post_detail = PostDetailView.as_view()
```

### blog > models.py
```
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

### 마이그레이트
```
python manage.py makemigrations
python manage.py migrate
```

### blog > admin.py
```
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

### blog > tests.py > Test
```
class Test(TestCase):
    def setUp(self):
        print('-- blog 테스트 시작 --')
        self.client = Client()

    def test_access_index(self):
        '''
        index 페이지 접속 테스트
        '''
        print('-- index 페이지 접속 테스트 시작 --')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print('-- index 페이지 접속 테스트 종료 --')

    def test_extends_index(self):
        '''
        index 페이지 상속 테스트
        '''
        print('-- index 페이지 상속 테스트 시작 --')
        response = self.client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.select('header'))
        self.assertTrue(soup.select('body'))
        self.assertTrue(soup.select('footer'))
        print('-- index 페이지 상속 테스트 종료 --')
```

### blog > views.py > IndexView
```
class IndexView(View):
    def get(self, request):
        return render(request, 'main/index.html')
```

### templates > base.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <style></style>
</head>
<body>
    <header>{% block header %}{% endblock %}</header>
    {% block body %}{% endblock %}
    <footer>{% block footer %}{% endblock %}</footer>
</body>
</html>
```

### templates > main > index.html
```
{% extends 'base.html' %}
{% block title %}
index
{% endblock %}
{% block header %}
index header
{% endblock %}
{% block body %}
index body
{% endblock %}
{% block footer %}
index footer
{% endblock %}
```

### blog > tests.py
```
class Test(TestCase):
    ...
    def test_access_about(self):
        '''
        about 페이지 접속 테스트
        '''
        print('-- about 페이지 접속 테스트 시작 --')
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        print('-- about 페이지 접속 테스트 종료 --')

    def test_extends_about(self):
        '''
        about 페이지 상속 테스트
        '''
        print('-- about 페이지 상속 테스트 시작 --')
        response = self.client.get('/about/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.select('header'))
        self.assertTrue(soup.select('body'))
        self.assertTrue(soup.select('footer'))
        print('-- about 페이지 상속 테스트 종료 --')
```

### blog > views.py > AboutView
```
class AboutView(View):
    def get(self, request):
        return render(request, 'main/about.html')
```

### templates > main > about.html
```
{% extends 'base.html' %}
{% block title %}
about
{% endblock %}
{% block header %}
about header
{% endblock %}
{% block body %}
about body
{% endblock %}
{% block footer %}
about footer
{% endblock %}
```

### blog > tests.py
```
class Test(TestCase):
    ...
    def test_access_contact(self):
        '''
        contact 페이지 접속 테스트
        '''
        print('-- contact 페이지 접속 테스트 시작 --')
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        print('-- contact 페이지 접속 테스트 종료 --')

    def test_extends_contact(self):
        '''
        contact 페이지 상속 테스트
        '''
        print('-- contact 페이지 상속 테스트 시작 --')
        response = self.client.get('/contact/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.select('header'))
        self.assertTrue(soup.select('body'))
        self.assertTrue(soup.select('footer'))
        print('-- contact 페이지 상속 테스트 종료 --')
```

### blog > views.py > ContactView
```
class ContactView(View):
    def get(self, request):
        return render(request, 'main/contact.html')
```

### templates > contact.html
```
{% extends 'base.html' %}
{% block title %}
contact
{% endblock %}
{% block header %}
contact header
{% endblock %}
{% block body %}
contact body
{% endblock %}
{% block footer %}
contact footer
{% endblock %}
```

### blog > tests.py
```python
class Test(TestCase):
    ...
    def test_access_blog(self):
        '''
        blog 페이지 접속 테스트
        '''
        print('-- blog 페이지 접속 테스트 시작 --')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        print('-- blog 페이지 접속 테스트 종료 --')

    def test_extends_blog(self):
        '''
        blog 페이지 상속 테스트
        '''
        print('-- blog 페이지 상속 테스트 시작 --')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.select('header'))
        self.assertTrue(soup.select('body'))
        self.assertTrue(soup.select('footer'))
        print('-- blog 페이지 상속 테스트 종료 --')

    def test_post_list_non(self):
        '''
        blog 게시물이 없는 경우 리스트 테스트
        '''
        print('-- blog 게시물이 없는 경우 리스트 테스트 시작 --')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!', soup.text)
        print('-- blog 게시물이 없는 경우 리스트 테스트 종료 --')

    def test_post_list(self):
        '''
        blog 게시물이 있는 경우 리스트 테스트
        '''
        print('-- blog 게시물이 있는 경우 리스트 테스트 시작 --')
        post_001 = Post.objects.create(
            title = '첫 번째 포스트',
            content = 'Hello world. we are the world.',
        )
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertGreater(len(soup.body.select('h2')), 0)
        print('-- blog 게시물이 있는 경우 리스트 테스트 종료 --')
```

### blog > views.py > PostListView
```
class PostListView(ListView):
    model = Post
```

### templates > blog > post_list.html
```
{% extends 'base.html' %}
{% block title %}
    blog
{% endblock %}
{% block header %}
    post_list header
{% endblock %}
{% block body %}
    {% if object_list %}
        {% for object in object_list %}
            <section class='contents-section'>
                <a href="{% url 'blog:post_detail' object.pk %}">
                    <h2>{{ object.title }}</h2>
                    <p>{{ object.content }}</p>
                    <p>{{ object.created_at }}</p>
                </a>
            </section>
        {% endfor %}
    {% else %}
        <p>게시물이 존재하지 않습니다. 첫번째 게시물에 주인공이 되세요!</p>
    {% endif %}
{% endblock %}
{% block footer %}
    post_list footer
{% endblock %}
```

### blog > tests.py
```
class Test(TestCase):
    ...
    def test_post_detail(self):
        '''
        blog 상세 페이지 제목, 내용, 수정날짜 유무 테스트
        '''
        print('-- blog 상세 페이지 제목, 내용, 수정날짜 유무 테스트 시작 --')
        post_001 = Post.objects.create(
            title = '첫 번째 포스트',
            content = 'Hello world. we are the world.',
        )
        response = self.client.get('/blog/1/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.body.select('.contents-heading')[0].text)
        self.assertTrue(soup.body.select('.contents-text')[0].text)
        self.assertTrue(soup.body.select('.contents-updated')[0].text)
        print('-- blog 상세 페이지 제목, 내용, 수정날짜 유무 테스트 --')

    def test_extends_blog_detail(self):
        '''
        blog detail 페이지 상속 테스트
        '''
        print('-- blog detail 페이지 상속 테스트 시작 --')
        post_001 = Post.objects.create(
            title = '첫 번째 포스트',
            content = 'Hello world. we are the world.',
        )
        response = self.client.get('/blog/1/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.select('header'))
        self.assertTrue(soup.select('body'))
        self.assertTrue(soup.select('footer'))
        print('-- blog detail 페이지 상속 테스트 종료 --')
```

### blog > views.py
```
class PostDetailView(DetailView):
    model = Post
```

### templates > post_detail.html
```
{% extends 'base.html' %}
{% block title %}
    blog
{% endblock %}
{% block header %}
    post_detail header
{% endblock %}
{% block body %}
    <section class='contents-section'>
        <h2 class='contents-heading'>{{ object.title }}</h2>
        <p class='contents-text'>{{ object.content }}</p>
        <p class='contents-updated'>{{ object.created_at }}</p>
    </section>
{% endblock %}
{% block footer %}
    post_detail footer
{% endblock %}
```