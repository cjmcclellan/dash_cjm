import unittest
from .formatting import convert_num_subscript
import codecs


class TestFormat(unittest.TestCase):

    def test_num_subscript(self):

        test = 'MoS2'

        test = convert_num_subscript(test)

        self.assertEqual(test, 'MoS\u2082', 'The formatting convert_num_subscript function is broken.')


if __name__ == '__main__':
    unittest.main()
