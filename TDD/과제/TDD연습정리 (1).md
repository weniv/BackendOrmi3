# django_test_prac 프로젝트 테스트
## url 및 model
### url
|이름|url|비고|
|:---|:---|:---|
|메인 페이지|/|main|
|소개 페이지|/about|main|
|주소 페이지|/contact|main|
|블로그 페이지|/blog|main, test페이지|
|게시글 목록|/blog||
|게시글 상세보기|/blog/\<int:post_pk\>/|R|
|게시글 검색|/blog/?q=\'keyword\'||
### model
#### blog.models.py
```python
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```


---
## test
### /test
#### 테스트 목표
> * 접속 확인
> * * `/` 접속 확인
> * * `/about` 접속 확인
> * * `/contact` 접속 확인
> * * `/blog` 접속 확인

#### template 상속
> ✨ base.html  
> └  index.html  
> └  about.html  
> └  contact.html  
> └  blog/post_list.html  
> └  blog/post_detail.html  


#### tests.py
```python
from typing import assert_type
from django.test import TestCase, Client
from bs4 import BeautifulSoup
# Create your tests here.


class Test(TestCase):
    """
    ----- main app test -----
    
    # 1. 접속 확인
    # 1. 1 '/' 접속 확인
    # 1. 2 '/about' 접속 확인
    # 1. 3 '/contact' 접속 확인
    # 1. 4 '/blog' 접속 확인
    
    
    # 2. 상속 확인
    # 2. 1 '/' 상속 확인
    # 2. 2 '/about' 상속 확인
    # 2. 3 '/contact' 상속 확인
    # 2. 4 '/blog' 상속 확인
    """
    
    def setUp(self):
        print('\n---blog app 테스트 시작---')
        self.client = Client()
        

    def test_connection(self):
        '''
        # 접속 확인
        # 1 '/' 접속 확인
        # 2 '/about' 접속 확인
        # 3 '/contact' 접속 확인
        # 4 '/blog' 접속 확인
        '''

        print('접속 테스트 시작')
        
        print('└"/" 접속 테스트')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        print('└"/about/" 접속 테스트')
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        
        print('└"/contact/" 접속 테스트')
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        
        print('└"/blog/" 접속 테스트')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        
            
    def test_template_inheritance(self):        
        '''
        # 상속 확인
        # 1 '/' 상속 확인
        # 2 '/about' 상속 확인
        # 3 '/contact' 상속 확인
        # 4 '/blog' 상속 확인
        '''

        print('템플릿 상속 테스트 시작')
        
        
        print('└"/" 게시물 상속 확인 테스트')
        response = self.client.get('/')
        print('\t└header 상속 확인 테스트')
        self.assertContains(response, '<header>')
        print('\t└footer 상속 확인 테스트')
        self.assertContains(response, '<footer>')
        
        print('└"/about/" 게시물 상속 확인 테스트')
        response = self.client.get('/about/')
        print('\t└header 상속 확인 테스트')
        self.assertContains(response, '<header>')
        print('\t└footer 상속 확인 테스트')
        self.assertContains(response, '<footer>')
        
        print('└"/contact/" 게시물 상속 확인 테스트')
        response = self.client.get('/contact/')
        print('\t└header 상속 확인 테스트')
        self.assertContains(response, '<header>')
        print('\t└footer 상속 확인 테스트')
        self.assertContains(response, '<footer>')
        
        print('└"/blog/" 게시물 상속 확인 테스트')
        response = self.client.get('/blog/')
        print('\t└header 상속 확인 테스트')
        self.assertContains(response, '<header>')
        print('\t└footer 상속 확인 테스트')
        self.assertContains(response, '<footer>')
        
```

### blog/test
#### 테스트 목표
> * 게시물 리스트(post_list) 확인
> * * 게시물이 없으면 "게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!"가 출력되어야 합니다.
> * * 게시물이 있으면 \<h2\> 태그가 1개 이상이어야 합니다.
> * 게시물 상세페이지(post_detail) 확인
> * * 제목(title) 자리에 제목이 있는지
> * * 내용(content) 자리에 내용이 있는지
> * * 최종 수정 날짜(updated_at) 자리에 수정 날짜가 있는지
> * * 상속(상속 받을 대상: menu, footer)이 제대로 이루어져 있는지

#### template 상속
>
> ✨ base.html  
> └  blog/post_list.html  
> └  blog/post_detail.html  

#### blog/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class Test(TestCase):
    """
    ----- blog app test -----
    
    # 1. 게시물 리스트(post_list) 확인
    # 1. 1 게시물이 없으면 "게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!"가 출력되어야 합니다.
    # 1. 2 게시물이 있으면 <h2> 태그가 1개 이상이어야 합니다.
    
    # 2. 게시물 상세페이지(post_detail) 확인
    # 2. 1 제목(title) 자리에 제목이 있는지
    # 2. 2 내용(content) 자리에 내용이 있는지
    # 2. 3 최종 수정 날짜(updated_at) 자리에 수정 날짜가 있는지
    # 2. 4 상속(상속 받을 대상: menu, footer)이 제대로 이루어져 있는지
    """
    
    def setUp(self):
        print('\n---blog app 테스트 시작---')
        self.client = Client()
        
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World._1',
        )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='Hello World._2',
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='Hello World._3',
        )
        self.post_004 = Post.objects.create(
            title='네 번째 포스트입니다.',
            content='Hello World._4',
        )
        
        

    def test_post_list(self):
        '''
        # 게시물 리스트(post_list) 확인
        # 1. 게시물이 없으면 "게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!"가 출력되어야 합니다.
        # 2. 게시물이 있으면 <h2> 태그가 1개 이상이어야 합니다.
        '''

        print('post_list 테스트 시작')
        
        print('└post_list 게시물 리스트 접속 테스트')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        
        print('└post_list 게시물 리스트 항목 테스트')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if Post.objects.count == 0:
            self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!', soup.body.text)
        else:
            self.assertGreater(len(soup.body.select('h2')), 0)
            
    def test_post_detail(self):        
        '''
        # 게시물 상세페이지(post_detail) 확인
        # 1 제목(title) 자리에 제목이 있는지
        # 2 내용(content) 자리에 내용이 있는지
        # 3 최종 수정 날짜(updated_at) 자리에 수정 날짜가 있는지
        # 4 상속(상속 받을 대상: menu, footer)이 제대로 이루어져 있는지
        '''

        print('post_detail 테스트 시작')
        
        print('└post_detail 게시물 리스트 접속 테스트')
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print('└post_detail 게시물 제목 테스트')        
        self.assertIn(self.post_001.title, soup.body.text)
        
        print('└post_detail 게시물 내용 테스트')        
        self.assertIn(self.post_001.content, soup.body.text)
        
        print('└post_detail 게시물 수정 날짜 테스트')        
        self.assertIn(str(self.post_001.updated_at), soup.body.text)
        
        print('└post_detail 게시물 상속 확인 테스트')
        print('\t└post_detail header 상속 확인 테스트')
        self.assertContains(response, '<header>')
        print('\t└post_detail footer 상속 확인 테스트')
        self.assertContains(response, '<footer>')
```