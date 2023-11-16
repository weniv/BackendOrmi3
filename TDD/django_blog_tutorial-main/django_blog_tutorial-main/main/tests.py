from django.test import TestCase

class Test(TestCase):
    def test_something_a(self):
        print('main app test a: 테스트 내용')
        self.assertEqual(True, True)

    def test_something_b(self):
        print('main app test b: 테스트 내용')
        self.assertEqual(True, True)
