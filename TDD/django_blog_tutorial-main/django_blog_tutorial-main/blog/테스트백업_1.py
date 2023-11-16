from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

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

    def test_post_list(self):
        '''
        테스트 코드를 작성하는 일을 지루한 작업입니다.
        다만 코파일럿이 나오면서 테스트 코드를 작성하는 것이 쉬워졌습니다.
        여러분이 테스트하고자 하는 테스트만 주석으로 작성하면 코파일럿이 테스트 코드를 작성해줍니다.
        그렇기 때문에 요구사항 명세와 기능 명세가 중요합니다.
        '''
        print('-- 1차 테스트 시작 --')
        # 테스트 목적 또는 시너리오, 기타 설명등을 주석으로 작성합니다.
        
        print('-- 접속 확인 --')
        # 1. 접속
        # 1.1 포스트 목록 페이지를 가져온다.
        # 1.2 정상 접속이 되면 페이지 타이틀에 'Blog'라는 문구입니다.
        
        print('-- 상속 확인 --')
        # 2. 상속
        # 2.1 페이지 상속이 제대로 되었다면 nav태그가 있고, footer태그가 있어야 합니다.
        # 2.2 nav태그 내부에는 Home, About, Blog라는 문구(메뉴)가 있어야 합니다.
        
        print('-- 포스트 목록 확인 --')
        # 3. 포스트 목록
        # 3.1 포스트 목록이 하나도 없다면 '아직 게시물이 없습니다.'라는 문구가 나와야 합니다.
        # 3.2 포스트가 2개 있다면, 포스트의 개수만큼 <div class="post-item">이 있어야 합니다.

        print('-- 포스트 내용 확인 --')
        # 4. 포스트 내용
        # 4.1 포스트가 1개 있다면 해당 포스트의 제목(title)이 포스트 영역에 있어야 합니다.
        # 4.2 포스트가 1개 있다면 해당 포스트의 작성자(author)가 포스트 영역에 있어야 합니다.
        # 4.3 포스트가 1개 있다면 해당 포스트의 내용(content)이 포스트 영역에 있어야 합니다.