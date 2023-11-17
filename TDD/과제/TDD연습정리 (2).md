# 1. todayproject 폴더 내에서 터미널
```
python -m venv venv

.\venv\Scripts\activate

pip install django

django-admin startproject tutorialdjango .

python manage.py startapp main
```
# 2. settings.py 코드 내에서 
```python
ALLOWED_HOST = ["*"]
.
.
.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]
.
.
.
```
# 3. todayproject 폴더 내에서 터미널
```
python manage.py migrate
```
# 4. tutorialdjango/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
```
# 5. main/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('blog/', views.blog, name = 'blog'),
    path('blog/<int:pk>', views.blogdetail, name = 'blogdetail'),
]
```
# 6. main/models.py
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
# 7. main/views.py
```python
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

class BlogView(ListView):
    model = Post
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs
    
blog = BlogView.as_view()

class BlogDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.save()
        return super().get_object(queryset)
    
blogdetail = BlogDetailView.as_view()
```
# 8. templates/base.html
```html
<body>
    <header>
        <a href="{% url 'index' %}">index</a>
        <a href="{% url 'about' %}">about</a>
        <a href="{% url 'contact' %}">contact</a>
        <a href="{% url 'blog' %}">blog</a>
    </header>

{% block content %}
{% endblock %}


    <footer>
        <p>상속 test용 푸터</p>
    </footer>
</body>
```
# 9. templates/index.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Index</title>
    </head>
        {% extends 'base.html' %}
        {% block content %}
            index입니다.
        {% endblock %}
</html>
```
# 10. templates/about.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About</title>
    </head>
    {% extends 'base.html' %}
    {% block content %}
        about입니다.
    {% endblock %}
</html>
```
# 11. templates/contact.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact</title>
    </head>
    {% extends 'base.html' %}
    {% block content %}
        contact입니다.
    {% endblock %}
</html>
```
# 12. templates/post_list.html
```html
{% extends 'base.html' %}
{% block content %}
        <h1>blog입니다.</h1>
        <form action="" method="get">
            <input type="text" name="q" value = "{{ request.get.q }}">
            <input type="submit" value = "검색">
        </form>

        <ul>
            {% for post in post_list %}
            <li>
                <a href="{% url 'blogdetail' post.pk %}">
                    {{ post.title }}
                </a>
            </li>
            {% endfor %}
        </ul>
{% endblock %}
```
# 13. templates/post_detail.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Detail</title>
    </head>
    {% extends 'base.html' %}
    {% block content %}
        <section class='contents-section'>
            <h2 class='contents-heading'>{{ post.title }}</h2>
            <p class='contents-text'>{{ post.content }}</p>
            <p class='contents-updated'>{{ post.updated_at }}</p>
        </section>
        <a href="{% url 'blog' %}">목록</a>
    {% endblock %}

```


# 14. 터미널
```
pip install bs4
```

# 15. main/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class Test(TestCase):
    def setup(self):
        print('--main app 테스트 시작 --')
        self.client = Client()
    
    def test_post_list(self):
        '''
        class Post(models.Model):
            title
            content
            created_at
            updated_at
        '''
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            updated_at = 'Nov. 16, 2023',
            )
        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            updated_at = 'Nov. 16, 2023',
        )
        
        print('--1차 테스트 시작--')
        
        print('--접속 확인--')
        # 1. 접속
        # 1.1 메인페이지 페이지를 가져온다.
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        
        # 1.1.1 정상 접속 시 타이틀은 'Index'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Index')
        
        # 1.2 about페이지 페이지를 가져온다.
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        
        # 1.2.1 정상 접속 시 타이틀은 'About'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'About')
        
        # 1.3 contact페이지 페이지를 가져온다.
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        
        # 1.3.1 정상 접속 시 타이틀은 'Contact'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Contact')
        
        # 1.4 blog페이지 페이지를 가져온다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        
        # 1.4.1 정상 접속 시 타이틀은 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        
        print('--상속 확인--')
        # 2. 상속 확인
        # 2.1 페이지 상속이 제대로 되었다면 header, footer 태그가 있어야 합니다.
        # 2.2 header태그에는 index, about, contact, blog가 있어야 합니다.
        # 2.3 footer 태그에는 "상속 test용 푸터" 글이 있어야 합니다.
        header = soup.header
        self.assertIn('index', header.text)
        self.assertIn('about', header.text)
        self.assertIn('contact', header.text)
        self.assertIn('blog', header.text)
        
        footer = soup.footer
        self.assertIn('상속 test용 푸터', footer.text)
        
        print('--게시물 리스트 확인--')
        # 3. 게시물 리스트 확인
        # 3.1 포스트 목록이 하나도 없다면 '아직 게시물이 없습니다.'라는 문구가 나와야 합니다.
        # 3.2 포스트가 2개 있다면, 포스트의 개수만큼 posttitle 클래스가 있어야 합니다.
        if Post.objects.count() == 0:
            print('게시물이 없는 경우')
            self.assertIn('아직 게시물이 없습니다.', soup.body.text)
        else:
            print('게시물이 있는 경우')
            print(Post.objects.count())
            print(len(soup.body.select('.posttitle')))
            self.assertGreater(len(soup.body.select('.posttitle')), 1)
        
        # 4. 게시물 상세 페이지 확인
        # 4.1 게시물이 1개 있다면 해당 포스트의 제목(title)이 포스트 영역에 있어야 합니다.
        # 4.2 게시물이 1개 있다면 해당 포스트의 내용(content)이 포스트 영역에 있어야 합니다.
        # 4.3 게시물이 1개 있다면 해당 포스트의 수정날짜(updated_at)이 포스트 영역에 있어야 합니다.
        print('--상세 게시물 접속 확인--')
        def test_post_detail(self):
            post_001 = Post.objects.create(
                title = '첫 번째 포스트입니다.',
                content = 'Hello World. We are the world.',
                updated_at = 'Nov. 16, 2023',
            )
            # 4.4 접속
            # 4.4.1 게시물 상세 페이지를 가져온다.
            response = self.client.get('/blog/1/')
            self.assertEqual(response.status_code, 200)

            # 4.4.2 정상 접속이 되면 페이지 타이틀에 'Detail'라는 문구입니다.
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(soup.title.text, 'Detail')
            
            # 4.5 상속 확인
            # 4.5.1 페이지 상속이 제대로 되었다면 header, footer 태그가 있어야 합니다.
            # 4.5.2 header태그에는 index, about, contact, blog가 있어야 합니다.
            # 4.5.3 footer 태그에는 "상속 test용 푸터" 글이 있어야 합니다.
            header = soup.header
            self.assertIn('index', header.text)
            self.assertIn('about', header.text)
            self.assertIn('contact', header.text)
            self.assertIn('blog', header.text)
            
            footer = soup.footer
            self.assertIn('상속 test용 푸터', footer.text)
```