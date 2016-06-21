from datetime import datetime, timedelta

import django.test
from django.utils import timezone

from django.test.utils import override_settings

from rmr.utils.datetime import get_date_range, fromtimestamp
from rmr.utils.test import Parametrized


@override_settings(ROOT_URLCONF=__name__)
class JsonTestCase(django.test.TestCase, metaclass=Parametrized):

    maxDiff = None

    def test_get_date_range_errors(self):
        cases = dict(
            test_exception_with_end_date_is_none_while_max_range_passed=dict(
                start_date=int(datetime(2077, 9, 23).timestamp()),
                end_date=None,
                max_range=86400,
            ),
            test_exception_when_diff_between_start_date_and_end_date_greater_than_max_range=dict(
                start_date=int((datetime.now() - timedelta(seconds=42)).timestamp()),
                end_date=int(datetime.now().timestamp()),
                max_range=1,
            ),
            end_date_not_none_max_range_not_none=dict(
                start_date=None,
                end_date=int(datetime(2241, 7, 25).timestamp()),
                max_range=86400,
                expected_start_date=datetime(2241, 7, 24),
                expected_end_date=datetime(2241, 7, 25),
            ),
        )
        for case, params in cases.items():
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    get_date_range(
                        start_date=params['start_date'],
                        end_date=params['end_date'],
                        max_range=params['max_range'],
                    )

    def test_get_date_range_results(self):
        cases = dict(
            all_parameters_none=dict(
                start_date=None,
                end_date=None,
                max_range=None,
                expected_start_date=None,
                expected_end_date=None,
            ),
            start_date_end_date_not_none=dict(
                start_date=int(datetime(2077, 9, 23).timestamp()),
                end_date=None,
                max_range=None,
                expected_start_date=fromtimestamp(datetime(2077, 9, 23).timestamp()),
                expected_end_date=None,
            ),
            max_range_is_none=dict(
                start_date=int(datetime(2077, 9, 23).timestamp()),
                end_date=int(datetime(2241, 7, 25).timestamp()),
                max_range=None,
                expected_start_date=fromtimestamp(datetime(2077, 9, 23).timestamp()),
                expected_end_date=fromtimestamp(datetime(2241, 7, 25).timestamp()),
            ),
            end_date_not_none=dict(
                start_date=None,
                end_date=int(datetime(2241, 7, 25).timestamp()),
                max_range=None,
                expected_start_date=None,
                expected_end_date=fromtimestamp(datetime(2241, 7, 25).timestamp()),
            ),
        )

        for case, params in cases.items():
            with self.subTest(case=case):
                start_date, end_date = get_date_range(
                    start_date=params['start_date'],
                    end_date=params['end_date'],
                    max_range=params['max_range'],
                )
                self.assertEqual(start_date, params['expected_start_date'])
                self.assertEqual(end_date, params['expected_end_date'])
