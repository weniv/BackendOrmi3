# DRF 연습정리

## 1. 가상환경 설정
### 1-1. 프로젝트 디렉토리 생성 및 이동
```bash
mkdir drf-practice
cd drf-practice
```
### 1-2. 가상환경 생성
```bash
python -m venv venv
```
### 1-3. 가상환경 활성화
```bash
source ./venv/bin/activate
```
### 1-4. 필요 모듈 설치
```bash
pip install django djangorestframework
```
## 2. 장고 프로젝트 기본 설계
### 2-1. 장고 프로젝트 생성
```bash
django-admin startproject project .
```
### 2-2. blog 앱 생성
```bash
python manage.py startapp blog
```
### 2-3. project/settings.py 수정
```python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog',
]
...
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
...
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
    }
}
```

## 3. Model 작성
### 3-1. blog/models.py
```python
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Notice(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3-2. 모델 변경사항 적용
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. URL 연결
### 4-1. project/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blog.urls')),
]
```

### 4-2. blog/urls.py
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('blog', views.PostViewSet)
router.register('notice', views.NoticeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

## 5. Views 설정
### 5-1. blog/serializers.py
```python
from rest_framework.serializers import ModelSerializer
from .models import Post, Notice

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class NoticeSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
```

### 5-2. blog/permissions.py
```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

### 5-3. blog/views.py
```python
from rest_framework.viewsets import ModelViewSet
from .models import Post, Notice
from .serializers import PostSerializer, NoticeSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthorOrReadOnly]
```

## 6. 테스트를 하기 위한 선작업
### 6-1. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

### 6-2. 서버 실행
```bash
python manage.py runserver
```

### 6-3. 새로운 계정 생성 (일반계정)
- http://127.0.0.1:8000/admin/auth/user/ 에 가서 사용자를 추가한다.

## 7. Blog CRUD 테스트
### 7-1. 글 작성 (Create)
#### 7-1-1. 로그인 O
**Request**
- URL: http://127.0.0.1:8000/blog/
- Method: POST
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "Testest",
 "content": "testestest",
 "author": 2
}
```

**Response**
```json
Status: 201 Created
Size: 144 Bytes
Time: 656 ms
{
  "id": 5,
  "author": 2,
  "title": "Testest",
  "content": "testestest",
  "created_at": "2023-11-20T15:36:36.645341",
  "updated_at": "2023-11-20T15:36:36.645374"
}
```

#### 7-1-2. 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 403 Forbidden
Size: 96 Bytes
Time: 6 ms
{
  "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```

### 7-2. 글 조회 (Read)
#### 7-2-1. 목록보기, 로그인 O
**Request**
- URL: http://127.0.0.1:8000/blog/
- Method: GET
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 200 OK
Size: 676 Bytes
Time: 672 ms
[
  {
    "id": 1,
    "author": 1,
    "title": "1",
    "content": "11",
    "created_at": "2023-11-20T15:13:53.235948",
    "updated_at": "2023-11-20T15:13:53.236018"
  },
  {
    "id": 2,
    "author": 1,
    "title": "2",
    "content": "22",
    "created_at": "2023-11-20T15:13:59.574850",
    "updated_at": "2023-11-20T15:13:59.574884"
  },
  {
    "id": 3,
    "author": 1,
    "title": "3",
    "content": "33",
    "created_at": "2023-11-20T15:14:04.885616",
    "updated_at": "2023-11-20T15:14:04.885656"
  },
  {
    "id": 4,
    "author": 2,
    "title": "44up",
    "content": "444up",
    "created_at": "2023-11-20T15:27:52.078566",
    "updated_at": "2023-11-20T15:28:14.467518"
  },
  {
    "id": 5,
    "author": 2,
    "title": "Testest",
    "content": "testestest",
    "created_at": "2023-11-20T15:36:36.645341",
    "updated_at": "2023-11-20T15:36:36.645374"
  }
]
```

#### 7-2-2. 목록보기, 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 403 Forbidden
Size: 96 Bytes
Time: 15 ms
{
  "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```

#### 7-2-3. 상세보기, 로그인 O
**Request**
- URL: http://127.0.0.1:8000/blog/1/
- Method: GET
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 200 OK
Size: 130 Bytes
Time: 431 ms
{
  "id": 1,
  "title": "1",
  "content": "11",
  "created_at": "2023-11-20T15:13:53.235948",
  "updated_at": "2023-11-20T15:13:53.236018",
  "author": 1
}
```

#### 7-2-4. 상세보기, 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 403 Forbidden
Size: 96 Bytes
Time: 7 ms
{
  "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```

### 7-3. 글 수정 (Update)
#### 7-3-1. 글 작성자일 경우
**Request**
- URL: http://127.0.0.1:8000/blog/5/
- Method: PATCH
- Auth의 Basic에 글 쓴 계정의 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "Testupdate",
 "content": "testupdatete"
}
```

**Response**
```json
Status: 200 OK
Size: 149 Bytes
Time: 597 ms
{
  "id": 5,
  "author": 2,
  "title": "Testupdate",
  "content": "testupdatete",
  "created_at": "2023-11-20T15:36:36.645341",
  "updated_at": "2023-11-20T15:46:03.719022"
}
```

#### 7-3-2. 글 작성자가 아닐 경우
**Request**
- URL: http://127.0.0.1:8000/blog/5/
- Method: PATCH
- Auth의 Basic에 글 쓴 계정이 아닌 다른 계정의 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "Testupdate11",
 "content": "testupdatete11"
}
```

**Response**
```json
Status: 403 Forbidden
Size: 72 Bytes
Time: 656 ms
{
  "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
```

### 7-4. 글 삭제 (Delete)
#### 7-4-1. 글 작성자일 경우
**Request**
- URL: http://127.0.0.1:8000/blog/5/
- Method: DELETE
- Auth의 Basic에 글 쓴 계정의 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 204 No Content
Size: 0 Bytes
Time: 598 ms
```

#### 7-4-2. 글 작성자가 아닐 경우
**Request**
- URL: http://127.0.0.1:8000/blog/5/
- Method: DELETE
- Auth의 Basic에 글 쓴 계정이 아닌 다른 계정의 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 403 Forbidden
Size: 72 Bytes
Time: 616 ms
{
  "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
```

## 8. Notice CRUD 테스트
### 8-1. 글 작성 (Create)
#### 8-1-1. 로그인 O
**Request**
- URL: http://127.0.0.1:8000/notice/
- Method: POST
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "noticetest",
 "content": "noticetestest",
 "author": 1
}
```

**Response**
```json
Status: 201 Created
Size: 150 Bytes
Time: 676 ms
{
  "id": 5,
  "title": "noticetest",
  "content": "noticetestest",
  "created_at": "2023-11-20T16:45:22.856486",
  "updated_at": "2023-11-20T16:45:22.856670",
  "author": 1
}
```

#### 8-1-2. 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 403 Forbidden
Size: 96 Bytes
Time: 8 ms
{
  "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```

### 8-2. 글 조회 (Read)
#### 8-2-1. 목록보기, 로그인 O
**Request**
- URL: http://127.0.0.1:8000/notice/
- Method: GET
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 200 OK
Size: 726 Bytes
Time: 900 ms
[
  {
    "id": 1,
    "title": "notice11",
    "content": "noticee11",
    "created_at": "2023-11-20T16:10:54.824960",
    "updated_at": "2023-11-20T16:10:54.825003",
    "author": 2
  },
  {
    "id": 2,
    "title": "notice2",
    "content": "noticee2",
    "created_at": "2023-11-20T16:31:42.051989",
    "updated_at": "2023-11-20T16:31:42.052083",
    "author": 2
  },
  {
    "id": 3,
    "title": "notice3",
    "content": "noticee3",
    "created_at": "2023-11-20T16:33:04.215799",
    "updated_at": "2023-11-20T16:33:04.215822",
    "author": 2
  },
  {
    "id": 4,
    "title": "notice3",
    "content": "noticee3",
    "created_at": "2023-11-20T16:35:25.512174",
    "updated_at": "2023-11-20T16:35:25.512259",
    "author": 2
  },
  {
    "id": 5,
    "title": "noticetest",
    "content": "noticetestest",
    "created_at": "2023-11-20T16:45:22.856486",
    "updated_at": "2023-11-20T16:45:22.856670",
    "author": 1
  }
]
```

#### 8-2-2. 목록보기, 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 200 OK
Size: 726 Bytes
Time: 15 ms
[
  {
    "id": 1,
    "title": "notice11",
    "content": "noticee11",
    "created_at": "2023-11-20T16:10:54.824960",
    "updated_at": "2023-11-20T16:10:54.825003",
    "author": 2
  },
  {
    "id": 2,
    "title": "notice2",
    "content": "noticee2",
    "created_at": "2023-11-20T16:31:42.051989",
    "updated_at": "2023-11-20T16:31:42.052083",
    "author": 2
  },
  {
    "id": 3,
    "title": "notice3",
    "content": "noticee3",
    "created_at": "2023-11-20T16:33:04.215799",
    "updated_at": "2023-11-20T16:33:04.215822",
    "author": 2
  },
  {
    "id": 4,
    "title": "notice3",
    "content": "noticee3",
    "created_at": "2023-11-20T16:35:25.512174",
    "updated_at": "2023-11-20T16:35:25.512259",
    "author": 2
  },
  {
    "id": 5,
    "title": "noticetest",
    "content": "noticetestest",
    "created_at": "2023-11-20T16:45:22.856486",
    "updated_at": "2023-11-20T16:45:22.856670",
    "author": 1
  }
]
```

#### 8-2-3. 상세보기, 로그인 O
**Request**
- URL: http://127.0.0.1:8000/notice/1/
- Method: GET
- Auth의 Basic에 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 200 OK
Size: 144 Bytes
Time: 372 ms
{
  "id": 1,
  "title": "notice11",
  "content": "noticee11",
  "created_at": "2023-11-20T16:10:54.824960",
  "updated_at": "2023-11-20T16:10:54.825003",
  "author": 2
}
```

#### 8-2-4. 상세보기, 로그인 X
**Request**
- 위와 같은데 Auth 항목만 비운다.

**Response**
```json
Status: 200 OK
Size: 144 Bytes
Time: 14 ms
{
  "id": 1,
  "title": "notice11",
  "content": "noticee11",
  "created_at": "2023-11-20T16:10:54.824960",
  "updated_at": "2023-11-20T16:10:54.825003",
  "author": 2
}
```

### 8-3. 글 수정 (Update)
#### 8-3-1. 글 작성자일 경우
**Request**
- URL: http://127.0.0.1:8000/notice/5/
- Method: PATCH
- Auth의 Basic에 글 쓴 계정의 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "Testupdate",
 "content": "testupdatete"
}
```

**Response**
```json
Status: 200 OK
Size: 149 Bytes
Time: 665 ms
{
  "id": 5,
  "title": "Testupdate",
  "content": "testupdatete",
  "created_at": "2023-11-20T16:45:22.856486",
  "updated_at": "2023-11-20T16:49:54.068525",
  "author": 1
}
```

#### 8-3-2. 글 작성자가 아닐 경우
**Request**
- URL: http://127.0.0.1:8000/notice/5/
- Method: PATCH
- Auth의 Basic에 글 쓴 계정이 아닌 다른 계정의 로그인 정보를 입력한다. (Username, Password)
- Body
```json
{
 "title": "Testupdate11",
 "content": "testupdatete11"
}
```

**Response**
```json
Status: 403 Forbidden
Size: 72 Bytes
Time: 537 ms
{
  "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
```

### 8-4. 글 삭제 (Delete)
#### 8-4-1. 글 작성자일 경우
**Request**
- URL: http://127.0.0.1:8000/notice/5/
- Method: DELETE
- Auth의 Basic에 글 쓴 계정의 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 204 No Content
Size: 0 Bytes
Time: 415 ms
```

#### 8-4-2. 글 작성자가 아닐 경우
**Request**
- URL: http://127.0.0.1:8000/notice/5/
- Method: DELETE
- Auth의 Basic에 글 쓴 계정이 아닌 다른 계정의 로그인 정보를 입력한다. (Username, Password)

**Response**
```json
Status: 403 Forbidden
Size: 72 Bytes
Time: 420 ms
{
  "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
```