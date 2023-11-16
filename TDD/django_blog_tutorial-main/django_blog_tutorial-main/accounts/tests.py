from django.test import TestCase

class Test(TestCase):
    def test_something(self):
        print('accounts app test: 테스트 내용')
        self.assertEqual(True, True)