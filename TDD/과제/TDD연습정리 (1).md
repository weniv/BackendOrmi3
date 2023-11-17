# 목표
- 테스트 케이스 작성

# 명령어
```py
- 프로젝트 디렉토리 생성

mkdir 1116
cd 1116

- 가상환경 생성

python3 -m venv venv
source venv/bin/activate

- Django 설치

pip install django
pip install bs4

- 프로젝트 생성

django-admin startproject tddpractice .
python3 manage.py migrate

- blog 앱 생성

python3 manage.py startapp blog


# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

########################################

- blog 모델 설계
# blog > models.py

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

########################################

python3 manage.py makemigrations
python3 manage.py migrate

########################################

- blog urls 설정
# tddpractice > urls.py

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'))
]

# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('contact/', views.contact),
    path('blog/', views.postlist),
    path('<int:pk>/', views.postdetail),
]


########################################

- blog views 작성
# blog > views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.db.models import Q


def index(request):
    return render(request, 'blog/post_list.html')


def about(request):
    return render(request, 'blog/post_list.html')


def contact(request):
    return render(request, 'blog/post_list.html')


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']


postlist = PostList.as_view()
postdetail = PostDetail.as_view()
write = PostCreate.as_view()


########################################

- blog 테스트 코드 작성
blog > tests.py
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class Test(TestCase):
    def setUp(self):
        '''
        setUp 메서드는 테스트 케이스 초기화를 담당하는 메서드이며 각각의 테스트 메서드가
        실행되기 전에 호출되며, 테스트 환경을 설정하고 초기 상태를 정의하는데 사용됩니다.
        '''
        print('-- blog app 테스트 시작 --')
        # Client는 가상의 HTTP 요청을 생성하는데 사용됩니다.
        self.client = Client()

    # 1. 접속 확인
    def test_page_connect(self):
        '''
        접속 확인을 하는 테스트 코드입니다.
        '''
        print('접속 테스트 시작')
        print('index 접속 테스트 시작')
        index = self.client.get('/')
        self.assertEqual(index.status_code, 200)

        print('about 접속 테스트 시작')
        about = self.client.get('/about/')
        self.assertEqual(about.status_code, 200)

        print('contact 접속 테스트 시작')
        contact = self.client.get('/contact/')
        self.assertEqual(contact.status_code, 200)

        print('blog 접속 테스트 시작')
        blog = self.client.get('/blog/')
        self.assertEqual(blog.status_code, 200)

        print('접속 테스트 완료')

    def test_page_inherit(self):
        '''
        상속 확인을 하는 테스트 코드입니다.
        '''
        index = self.client.get('/')
        about = self.client.get('/about/')
        contact = self.client.get('/contact/')
        blog = self.client.get('/blog/')

        print('상속 테스트 시작')
        for page in [index, about, contact, blog]:
            soup = BeautifulSoup(page.content, 'html.parser')
            self.assertTrue(soup.header)
            self.assertTrue(soup.body)
            self.assertTrue(soup.footer)
        print('상속 테스트 완료')

    def test_post_list(self):
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='Hello World. We are the world.',
        )

        '''
        게시물 리스트 확인을 하는 테스트 코드입니다.
        '''
        print('게시판 리스트 테스트 시작')
        blog = self.client.get('/blog/')
        soup = BeautifulSoup(blog.content, 'html.parser')

        # 게시물 여부 확인
        if Post.objects.count() == 0:
            self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!', soup.body.text)

        # h2가 1개 이상인지 확인
        else:
            print(f'게시물의 개수 : {Post.objects.count()}개')
            print(f'해당 게시물의 h2의 수 {len(soup.body.select("h2"))//2}개')
            self.assertGreater(len(soup.body.select('h2')), 1)
        print('게시판 리스트 테스트 완료')


```