import datetime
import unittest

from rmr.utils.test import mocked_datetime


class TestUtilsTestCase(unittest.TestCase):

    def test_mocked_datetime(self):
        expected_datetime = datetime.datetime(2015, 1, 1, 18, 45, 30)
        mocked_datetime_class = mocked_datetime(expected_datetime)
        self.assertEqual(
            expected_datetime,
            mocked_datetime_class.now(),
        )
        self.assertEqual(
            expected_datetime,
            mocked_datetime_class.today(),
        )
