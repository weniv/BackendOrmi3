from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from accounts.models import User

class Test(TestCase):
    def setUp(self):
        '''
        테스트를 할 때에는 DB가 초기화 되어 있다고 가정하고,
        client도 새로 생성하여 테스트를 하게 됩니다.
        보통은 DB도 아래와 같이 세팅해서 진행합니다.
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        '''
        print('-- blog app 테스트 시작 --')
        self.client = Client()
        self.user_hojun = User.objects.create_user(
            username='hojun',
            password='nopassword'
        )

    def test_post_list(self):
        '''
        테스트 코드를 작성하는 일을 지루한 작업입니다.
        다만 코파일럿이 나오면서 테스트 코드를 작성하는 것이 쉬워졌습니다.
        여러분이 테스트하고자 하는 테스트만 주석으로 작성하면 코파일럿이 테스트 코드를 작성해줍니다.
        그렇기 때문에 요구사항 명세와 기능 명세가 중요합니다.
        '''
        '''
        class Post(models.Model):
            title 
            content
            head_image
            file_upload
            created_at
            updated_at
            author
            category
            tags
        '''
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_hojun,
        )
        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_hojun,
        )


        print('-- 1차 테스트 시작 --')
        # 테스트 목적 또는 시너리오, 기타 설명등을 주석으로 작성합니다.
        
        print('-- 접속 확인 --')
        # 1. 접속
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # 1.2 정상 접속이 되면 페이지 타이틀에 'Blog'라는 문구입니다.
        # self.assertTemplateUsed(response, 'blog/post_list.html')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        
        print('-- 상속 확인 --')
        # 2. 상속
        # 2.1 페이지 상속이 제대로 되었다면 nav태그가 있고, footer태그가 있어야 합니다.
        # 2.2 nav태그 내부에는 Home, About, Blog라는 문구(메뉴)가 있어야 합니다.
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        self.assertIn('Blog', navbar.text)

        # footer = soup.footer
        # self.assertIn('Instagram', footer.text)
        # self.assertIn('Facebook', footer.text)
        # self.assertIn('Twitter', footer.text)
        
        print('-- 포스트 목록 확인 --')
        # 3. 포스트 목록
        # 3.1 포스트 목록이 하나도 없다면 '아직 게시물이 없습니다.'라는 문구가 나와야 합니다.
        # 3.2 포스트가 2개 있다면, 포스트의 개수만큼 <div class="post-item">이 있어야 합니다.
        # 지금 게시물에서는 post-item이 없어서 h2로 대채합니다.
        if Post.objects.count() == 0:
            print('게시물이 없는 경우')
            self.assertIn('아직 게시물이 없습니다.', soup.body.text)
        else:
            print('게시물이 있는 경우')
            print(Post.objects.count())
            print(len(soup.body.select('h2')))
            self.assertGreater(len(soup.body.select('h2')), 1)

        print('-- 포스트 내용 확인 --')
        # 4. 포스트 내용
        # 4.1 포스트가 1개 있다면 해당 포스트의 제목(title)이 포스트 영역에 있어야 합니다.
        # 4.2 포스트가 1개 있다면 해당 포스트의 작성자(author)가 포스트 영역에 있어야 합니다.
        # 4.3 포스트가 1개 있다면 해당 포스트의 내용(content)이 포스트 영역에 있어야 합니다.
        # main_area = soup.find('div', id='main')
        # self.assertIn(self.post_001.title, main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_hojun,
        )
        # 1. 접속
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)

        # 1.2 정상 접속이 되면 페이지 타이틀에 'Blog'라는 문구입니다.
        # self.assertTemplateUsed(response, 'blog/post_list.html')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Document')
        
        print('-- 상속 확인 --')
        # 2. 상속
        # 2.1 페이지 상속이 제대로 되었다면 nav태그가 있고, footer태그가 있어야 합니다.
        # 2.2 nav태그 내부에는 Home, About, Blog라는 문구(메뉴)가 있어야 합니다.
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        self.assertIn('Blog', navbar.text)

        # 3. 포스트 내용
        # 3.1 포스트가 1개 있다면 해당 포스트의 제목(title)이 포스트 영역에 있어야 합니다.
        self.assertIn(post_001.title, soup.body.text)
        # 3.2 포스트가 1개 있다면 해당 포스트의 내용(content)이 포스트 영역에 있어야 합니다.
        self.assertIn(post_001.content, soup.body.text)
        # 3.3 포스트가 1개 있다면 해당 포스트의 작성자(author)가 포스트 영역에 있어야 합니다.
        self.assertIn(post_001.author.username, soup.body.text)