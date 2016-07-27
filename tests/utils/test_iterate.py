import unittest

from rmr.utils.iterate import split_every


class TestUtilsTestCase(unittest.TestCase):

    def test_split_every(self):
        expected_result = [[0, 1], [2, 3], [4]]
        result = [list(x) for x in split_every(range(5), 2)]
        self.assertEqual(expected_result, result)
