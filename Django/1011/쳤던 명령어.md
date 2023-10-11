# 목표
1. 모델을 만들어 데이터를 DB에 저장하고 템플릿에 템플릿 태그로 출력
2. 템플릿 태그와 템플릿 상속이 어떻게 이뤄지는지 이해
3. 데이터 업로드 및 이미지 업로드
4. 웹 서비스를 하나 만들어 검색이 가능하게 하겠습니다.

# 명령어
```
mkdir mysite
cd mysite
python -m venv venv

# 가상환경속으로 들어가기
.\venv\Scripts\activate # window
.\venv\Script\activate.bat # window
source ./venv/bin/activate # mac, linux

# window에서 오류가 뜰 경우
+ CategoryInfo          : 보안 오류: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
# 이걸 입력해주세요.
Set-ExecutionPolicy Unrestricted

pip install django
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py runserver # 이미 충분히 익숙하시다면 안하셔도 됩니다!

# settings.py에서 접속할 수 있는 사람 설정
ALLOWED_HOSTS = ['*'] # 28번째 줄에 접속할 수 있는 사람을 모든 사람으로 변경

python manage.py startapp main
python manage.py startapp blog

# settings.py 에서 33번째 라인 수정
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'blog',
]

###################################
# urls 기획
1. 다음 url이 실제 작동하도록 해주세요.
1.1 ''
1.2 'blog/'
1.3 'blog/<int:pk>'
1.4 'blog/test' # 템플릿 태그와 템플릿 상속이 어떻게 이뤄지는지 확인

###################################
앱이름: main    views 함수이름	 html 파일이름	비고
''             index            index.html

앱이름: blog    views 함수이름   html 파일이름  비고
'blog/'         blog            blog.html	
'blog/<int:pk>' post            post.html
'blog/<int:pk>' test            test.html

* test라는 이름 자체를 사용하지 않기를 권합니다.

###################################
# tutorialdjango > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
]

###################################
# main > urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

###################################
# main > views.py
from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

###################################
# templates 기본 폴더 변경합시다!

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        # .. 생략 ..
    },
]

# mysite > templates > main > about.html
# mysite > templates > blog > blog.html # 어차피 만들 것이라 미리 생성하겠습니다.
# mysite > templates > blog > post.html # 어차피 만들 것이라 미리 생성하겠습니다.

###################################
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.post, name='post'),
    path('test/', views.test, name='test'),
]

###################################
# blog > views.py
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
# from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponseForbidden

def blog(request):
    return render(request, 'blog/blog.html')

def post(request, pk):
    return render(request, 'blog/post.html')

def test(request):
    # request => HttpRequest
    # return되는 응답값 => HttpResponse
    data = [
        {'title': 'Post 1', 'text': 'Text 1', 'pk': 1},
        {'title': 'Post 2', 'text': 'Text 2', 'pk': 2},
        {'title': 'Post 3', 'text': 'Text 3', 'pk': 3},
    ]
    # return HttpResponse('hello world') # 1
    # return HttpResponse('<h1>hello world</h1>') # 2

    s = '<h1>{{title}}</h1><p>{{text}}</p>'
    # return HttpResponse(s) # 3
    # return HttpResponse(s.replace('{{title}}', data[0]['title']).replace('{{text}}', data[0]['text'])) # 4 (그래서 내부에서 css나 js를 못읽는 것입니다.)

    header = '<h2>hell world</h2>'
    main = render_to_string('blog/test.txt', {'data': data[0]})
    footer = '<p>bye world</p>'

    '''
    blog/test.txt
    <p>hello blog</p>
    <p>{{data.title}}</p>
    <p>{{data.text}}</p>
    '''

    # return HttpResponse(header + main + footer) # 5

    # DRF, REST API
    # http://test.api.weniv.co.kr/mall 와 같이 만들 수 있습니다.
    # fetch로 쇼핑몰 만들어봤었죠?
    return JsonResponse(data, safe=False) # 6

###################################
# 마이크로식 운영 test
# index.html을 가상환경 바깥에 어딘가에 만듭니다. liveserver로 구동시키셔야 합니다.
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body>
    <script>
        // http://127.0.0.1:8000/blog 에서 fetch로 데이터를 json 형식으로 가져와서
        // 화면에 출력하는 코드입니다.
        // 다만 지금 cors 문제로 실행이 안됩니다.
        fetch('http://127.0.0.1:8000/blog/test/')
        .then(function(response) {
            return response.json();
        })
        .then(function(myJson) {
            console.log(myJson);
        });

        // https://blog.hometowndeveloper.com/63
    </script>
</body>
</html>
###################################
pip install django-cors-headers

# settings.py
INSTALLED_APPS = [
    'corsheaders', # 최상단에 놓으세요!
    ... 생략 ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 최상단에 놓으세요!
    ... 생략 ... 
]

CORS_ORIGIN_ALLOW_ALL = True # 모든 URL에 요청에 대해 허용!

CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = [
#         'http://127.0.0.1:5500',
#         'http://127.0.0.1:8000',
#         'http://localhost:8000',
#         'http://localhost:5500',
# ]

###################################

python manage.py runserver

# 모든 url 테스트해봅니다.
# http://127.0.0.1:8000
# http://127.0.0.1:8000/about/
# http://127.0.0.1:8000/blog/
# http://127.0.0.1:8000/blog/999

###################################
# blog > models.py
# django models fields
# https://docs.djangoproject.com/en/4.2/ref/models/fields/

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 처음 생성될 때만
    updated_at = models.DateTimeField(auto_now=True) # 수정될 때마다

###################################

python manage.py makemigrations # 0001_initial.py 파일 생성 => DB를 조작할 수 있는 코드!
python manage.py migrate # 실제 DB에 반영

###################################
# admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)

###################################
python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준123!@

###################################
# admin 들어가서 게시물 3개 작성
# 필드는 보기 좋게 다듬어주세요.

from django.db import models

class Post(models.Model):
    ... 생략 ...

    def __str__(self):
        time = self.created_at.strftime('%Y-%m-%d %H:%M')
        return f'제목: {self.title}, 시간: {time}'

###################################
# blog > views.py

from django.shortcuts import render
from .models import Post

def blog(request):
    db = Post.objects.all()
    context = {
        'db': db,
    }
    return render(request, 'blog/blog.html', context)

def post(request, pk):
    db = Post.objects.get(pk=pk)
    context = {
        'db': db,
    }
    return render(request, 'blog/post.html', context)

def test(request):
    return render(request, 'blog/test.txt')

###################################
# tamplates > blog > blog.html

<h1>게시판</h1>
<ul>
    {% for post_detail in db %}
    <li>
        <a href="{% url 'post' post_detail.id %}">{{ post_detail.title }}</a>
    </li>
    {% endfor %}
</ul>

<p>{% url 'blog' %}</p>
<p>{% url 'post' 1 %}</p>

###################################
# tamplates > blog > post.html

<h1>게시판</h1>
<p>{{db.title}}</p>
<p>{{db.contents}}</p>
<p>{{db.updated_at}}</p>
<a href="{% url 'blog' %}">뒤로가기</a>

###################################
ORM, Django Shell, QuerySet : https://paullabworkspace.notion.site/ORM-Django-Shell-QuerySet-4c1ad20735ce44c483d6ff9071bd092c?pvs=4
공식문서 : https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet
jupyter notebook 사용 : https://youtu.be/Di5CYnoHYRk


>>> from blog.models import Post
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 시간: 2023-10-11 02:19>, <Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: 3, 시간: 2023-10-11 02:19>]>
>>> a = Post.objects.all()
>>> type(a)
<class 'django.db.models.query.QuerySet'>
>>> dir(a)
[... 생략 ..., 'aaggregate', 'abulk_create', 'abulk_update', 'acontains', 'acount', 'acreate', 'adelete', 'aearliest', 'aexists', 'aexplain', 'afirst', 'aget', 'aget_or_create', 
'aggregate', 'ain_bulk', 'aiterator', 'alast', 'alatest', 'alias', 'all', 'annotate', 'as_manager', 'aupdate', 'aupdate_or_create', 'bulk_create', 'bulk_update', 'complex_filter', 'contains', 'count', 'create', 'dates', 'datetimes', 'db', 'defer', 'delete', 'difference', 'distinct', 'earliest', 'exclude', 'exists', 'explain', 'extra', 'filter', 'first', 'get', 'get_or_create', 'in_bulk', 'intersection', 'iterator', 'last', 'latest', 'model', 'none', 'only', 'order_by', 'ordered', 'prefetch_related', 'query', 'raw', 'resolve_expression', 'reverse', 'select_for_update', 'select_related', 'union', 'update', 'update_or_create', 'using', 'values', 'values_list']

# Read
>>> Post.objects.all().order_by('-pk')
<QuerySet [<Post: 제목: 3, 시간: 2023-10-11 02:19>, <Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: 1, 시간: 2023-10-11 02:19>]>
>>> Post.objects.all().count()
3   
>>> q = Post.objects.get(id=1)
>>> q
<Post: 제목: 1, 시간: 2023-10-11 02:19>
>>> q = Post.objects.get(pk=1) 
>>> q
<Post: 제목: 1, 시간: 2023-10-11 02:19>
>>> q.title
'1' 
>>> q.id
1   
>>> q.pk
1 

>>> Post.objects.filter(title='1')
>>> Post.objects.filter(id=1)
>>> Post.objects.filter(title__contains='test')
>>> Post.objects.filter(contents__contains='2')
>>> Post.objects.filter(contents__contains='2').filter(title__contains='test')
>>> Post.objects.filter(contents__contains='2').filter(title__contains='2')
>>> Post.objects.filter(id__lt=3)
>>> Post.objects.filter(id__lt=3)[0]
>>> Post.objects.filter(id__gt=3)


eq - equal ( = )
ne - not equal ( <> )
lt - little ( < )
le - little or equal ( <= )
gt - greater ( > )
ge - greater or equal ( >= )

# Create
# User에게 받아서 이 코드를 실행시키면 게시물을 생성할 수 있습니다!
>>> q = Post.objects.create(title='test sample', contents='222')   
>>> q
<Post: 제목: test sample, 시간: 2023-10-11 04:19>
>>> q.title
'test sample'
>>> q.save()

>>> Post.objects.all().filter(contents__contains='2')
<QuerySet [<Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: test sample, 시간: 2023-10-11 04:19>]>
>>> Post.objects.all().filter(contents__contains='2').filter(title__contains='sample')
<QuerySet [<Post: 제목: test sample, 시간: 2023-10-11 04:19>]>
>>> Post.objects.all().filter(contents__contains='2', title__contains='sample')


# Delete
>>> q = Post.objects.get(pk=4)
>>> q.delete()
(1, {'blog.Post': 1})
>>> q
<Post: 제목: test sample, 시간: 2023-10-11 04:19>
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 시간: 2023-10-11 02:19>, <Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: 3, 시간: 2023-10-11 02:19>]>


# Update
>>> q = Post.objects.all()[0]
>>> q
<Post: 제목: 1, 시간: 2023-10-11 02:19>
>>> q.title = 'hello world' 
>>> q
<Post: 제목: hello world, 시간: 2023-10-11 02:19>
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 시간: 2023-10-11 02:19>, <Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: 3, 시간: 2023-10-11 02:19>]>
>>> q.save()
>>> Post.objects.all()
<QuerySet [<Post: 제목: hello world, 시간: 2023-10-11 02:19>, <Post: 제목: 2, 시간: 2023-10-11 02:19>, <Post: 제목: 3, 
시간: 2023-10-11 02:19>]>


Create
Read
Update
Delete


###################################
# test 용도의 예제입니다.
# 이런 코드를 실무에서 사용하지 않습니다.

###################################
# 게시물 생성
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.post, name='post'),
    path('test/', views.test, name='test'),
    path('posttest/<int:pk>/', views.posttest, name='posttest'),
]

###################################
# 게시물 생성
# blog > views.py
from django.shortcuts import render, redirect
from .models import Post

def blog(request):
    db = Post.objects.all()
    context = {
        'db': db,
    }
    return render(request, 'blog/blog.html', context)

def post(request, pk):
    db = Post.objects.get(pk=pk)
    context = {
        'db': db,
    }
    return render(request, 'blog/post.html', context)

def test(request):
    return render(request, 'blog/test.txt')

def posttest(request, pk):
    q = Post.objects.create(title=f'{pk}', contents=f'{pk}{pk}')
    q.save()
    return redirect('blog')

###################################

http://127.0.0.1:8000/blog/posttest/5
http://127.0.0.1:8000/blog/posttest/6
http://127.0.0.1:8000/blog/posttest/7

###################################
# 게시물 삭제
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.post, name='post'),
    path('test/', views.test, name='test'),
    path('posttest/<int:pk>/', views.posttest, name='posttest'),
    path('postdel/<int:pk>/', views.postdel, name='postdel'),
]


###################################
# 게시물 삭제
# blog > views.py

from django.shortcuts import render, redirect
from .models import Post

def blog(request):
    db = Post.objects.all()
    context = {
        'db': db,
    }
    return render(request, 'blog/blog.html', context)

def post(request, pk):
    db = Post.objects.get(pk=pk)
    context = {
        'db': db,
    }
    return render(request, 'blog/post.html', context)

def test(request):
    return render(request, 'blog/test.txt')

def posttest(request, pk):
    q = Post.objects.create(title=f'{pk}', contents=f'{pk}{pk}')
    q.save()
    return redirect('blog')

def postdel(request, pk):
    q = Post.objects.get(pk=pk)
    q.delete()
    return redirect('blog')

###################################

http://127.0.0.1:8000/blog/postdel/5
http://127.0.0.1:8000/blog/postdel/6
http://127.0.0.1:8000/blog/postdel/7

###################################
* 간편하게 DB 정리 방법
1. 프로그램 사용
https://sqlitebrowser.org/dl/
다운로드 받아 실행한 후 '데이터베이스 구조' 말고 '데이터 보기' 탭 클릭하여 데이터 삭제하고 '변경사항 저장하기'한 다음 django에서 확인
2. 덮어쓰기
기존에 DB를 별도에 폴더에 넣어두었다가 덮어쓰기
3. GitHub commit 돌아가기 기능을 사용