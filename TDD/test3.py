import unittest

# 우리가 구현한 코드
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y


# 테스트 코드
class TestAdd(unittest.TestCase):
    def test_add(self):
        print('더하기 테스트')
        self.assertEqual(add(1, 2), 3)

    def test_sub(self):
        print('빼기 테스트')
        self.assertEqual(sub(3, 1), 2)

    def test_mul(self):
        print('곱하기 테스트')
        self.assertEqual(mul(3, 4), 12)

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