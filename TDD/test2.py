import unittest

class TestAdd(unittest.TestCase):
    def test_add(self):
        print('더하기 테스트')
        self.assertEqual(1, 1)

    def test_sub(self):
        print('빼기 테스트')
        self.assertEqual(2, 2)

    def test_mul(self):
        print('곱하기 테스트')
        self.assertEqual(3, 3)

    def hojun(self):
        '''
        테스트 이름을 마음대로 정할 수 있는지 체크
        'test_'로 시작하지 않으면 테스트로 인식하지 않는다.
        '''
        self.assertEqual(5, 4)

    def test_hojun(self):
        '''
        테스트 이름을 마음대로 정할 수 있는지 체크
        '''
        self.assertEqual(5, 5)

if __name__ == '__main__':
    unittest.main()