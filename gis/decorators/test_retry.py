import unittest

from retry import retry


class TestRetry(unittest.TestCase):

    @retry(ZeroDivisionError)
    def div(self):
        print(divmod(1, 0))

    def test_div(self):
        self.div()


if __name__ == '__main__':
    unittest.main()
