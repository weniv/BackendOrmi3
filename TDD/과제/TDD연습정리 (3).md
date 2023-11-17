## 프로젝트 생성
[위니브 제공 블로그 프로젝트](https://github.com/weniv/django_blog_tutorial)
해당 프로젝트를 먼저 다운해서 생성한 프로젝트에 넣어주자

django_blog_tutorial-main


## 가상환경 및 프로젝트 실행
파워쉘을 열고
가상환경이 설치된 경로로 이동하여 가상환경을 실행하고

프로젝트에 필요한 패키지들을 설치하고 
평소처럼 프로젝트를 실행하자

```shell
# 가상환경 실행
.\venv\Scripts\activate


# 패키지 설치
pip install -r requirements.txt

# 프로젝트 실행
python manage.py runserver

```

![image](https://github.com/Ko-udon/dayone/assets/79897135/e2e5c81a-259d-4f6e-8c1c-a9a4c60a5a3a)



## 테스트 과제 

### 접속 확인
   - /
   - /about
   - /contact
   - /blog

blog > test.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from accounts.models import User

class Test(TestCase):
    def test_connection(self):
        
        # 접속확인
        print('# 접속확인 테스트')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
```

   

### 상속확인
- 위 4개 페이지에서 header, body, footer가 제대로 상속 되는지 확인

```python
def test_tag(self):
        print('# 상속 확인')

        ## ./
        response = self.client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        headbar = soup.head
        self.assertEqual(None, headbar)

        # bodybar = soup.body
        # self.assertIn('index', bodybar.text)

        # footer = soup.footer
        # self.assertIn(None, footer)

        ## /about/
        response = self.client.get('/about/')
        soup = BeautifulSoup(response.content, 'html.parser')
        headbar = soup.head
        self.assertIn('Document', headbar.text)

        bodybar = soup.body
        self.assertIn('about', bodybar.text)

        # footer = soup.footer
        # self.assertIn(None, footer)


        ## /contact/
        response = self.client.get('/contact/')
        soup = BeautifulSoup(response.content, 'html.parser')
        headbar = soup.head
        self.assertIn('Document', headbar.text)

        bodybar = soup.body
        self.assertIn('contact', bodybar.text)

        # footer = soup.footer
        # self.assertIn(None, footer)
        
        ## /blog/
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        headbar = soup.head
        self.assertIn('Blog', headbar.text)

        bodybar = soup.body
        self.assertIn('blog', bodybar.text)

        # footer = soup.footer
        # self.assertIn(None, footer)
        
```


### 게시물 리스트 확인
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

```python
def test_post_list(self):
        print('# 게시물 리스트 확인')
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        if Post.objects.count() == 0:
            print('게시물이 없는 경우')
            self.assertIn('아직 게시물이 없습니다.', soup.body.text)
        else:
            print('게시물이 있는 경우')
            print(Post.objects.count())
            print(len(soup.body.select('h2')))
            self.assertGreater(len(soup.body.select('h2')), 1) # h2태그가 1개 이상
```
### 게시물 상세페이지 확인
   - 제목 자리에 제목이 들어있는지
   - 내용 자리에 내용이 들어있는지
   - 최종 수정 날짜에 수정날짜가 들어가 있는지
   - 상속이 제대로 이뤄져 있는지
   	- 메뉴, 푸터
```python
def test_post_detail(self):
        print('게시물 상세페이지 확인')
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World.',
            author = self.user_hojun
        )

        # 상세페이지 정상적으로 불러오는지 확인
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        detail = soup.body.main.text
        detail_content = detail.split('\n')

        # 제목 자리에 제목이 들어있는지
        self.assertEqual(detail_content[1], '첫 번째 포스트입니다.')
        
        # 내용 자리에 내용이 들어있는지
        self.assertEqual(detail_content[2], 'Hello World.')

        # 최종 수정 날짜에 수정날짜가 들어가 있는지
        self.assertIn(detail_content[3][:-8], post_001.updated_at.strftime('%Y년 %m월 %d일'))
        
        # 상속이 제대로 이뤄져 있는지
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        self.assertIn('Blog', navbar.text)
```
  
   





