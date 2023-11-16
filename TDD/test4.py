import unittest


class TestAdd(unittest.TestCase):
    def test_add(self):
        print(dir(self)) # 이걸로 어떤 메서드가 있는지 한 번 쭉 눈으로 확인해보세요.
        self.assertEqual(1 + 2, 3) # 같은지 판별
        self.assertTrue(10 == 10) # True인지 판별
        self.assertFalse(1 == 10) # False인지 판별
        self.assertGreater(10, 1) # 앞에 것이 뒤에 것보다 큰지
        self.assertLess(1, 10) # 앞에 것이 뒤에 것보다 작은지
        self.assertIn(1, [1, 2, 3, 4, 5]) # 포함하고 있는지
        self.assertIsInstance('a', str) # 인스턴스인지

if __name__ == '__main__':
    unittest.main()