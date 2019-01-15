__author__ = 'zc'

import unittest



class demoSkipTest(unittest.TestCase):
    a = 70
    b = 50

    print(a%b)
    def test_add(self):
        """加法"""
        result = self.a + self.b
        self.assertEqual(result, 40)

    def test_add_2(self):
        self.skipTest("强制跳过示例")
        result = self.a + self.b
        self.assertEqual(result, 9)

    @unittest.skipIf(a > b, u"a>b，正确就强制跳过")
    def test_sub(self):
        """减法"""
        result = self.a - self.b
        self.assertTrue(result == -30)

    @unittest.skipUnless(a%b == 2, u"错误就跳过")
    def test_div(self):
        """除法"""
        result = self.a / self.b
        self.assertTrue(result == 1)

    @unittest.expectedFailure
    def test_mul01(self):
        """乘法"""
        result = self.a * self.b
        self.assertTrue(result == 350)

    @unittest.expectedFailure
    def test_mul02(self):
        """乘法"""
        result = self.a * self.b
        self.assertTrue(result == 3500)


if __name__ == "__main__":
    unittest.main()