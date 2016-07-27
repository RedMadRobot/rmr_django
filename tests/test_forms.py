import time

import mock

from django import test

from rmr import forms


class StartStopTestCase(test.SimpleTestCase):

    def test_start_time_stop_time_not_required(self):
        cases = dict(
            default=dict(
                form_data={},
                is_valid=True,
            ),
            lack_of_start_time=dict(
                form_data={'stop_time': '10'},
                is_valid=True,
            ),
            lack_of_stop_time=dict(
                form_data={'start_time': '90'},
                is_valid=True,
            ),
            regular=dict(
                form_data={'start_time': '1', 'stop_time': '5'},
                is_valid=True,
            ),
            start_time_greater_then_stop_time=dict(
                form_data={'start_time': '10', 'stop_time': '5'},
                is_valid=False,
            ),
        )
        for case, data in cases.items():
            with self.subTest(case=case):
                form = forms.StartStopTime(data['form_data'])
                is_valid = form.is_valid()
                self.assertEqual(data['is_valid'], is_valid, dict(form.errors))

    def test_start_time_stop_time_required(self):
        cases = dict(
            default=dict(
                form_data={},
                is_valid=False,
            ),
            lack_of_start_time=dict(
                form_data={'stop_time': '10'},
                is_valid=False,
            ),
            lack_of_stop_time=dict(
                form_data={'start_time': '0'},
                is_valid=False,
            ),
            regular=dict(
                form_data={'start_time': '0', 'stop_time': '10'},
                is_valid=True,
            ),
            start_time_greater_then_stop_time=dict(
                form_data={'start_time': '10', 'stop_time': '5'},
                is_valid=False,
            ),
            range_greater_then_max=dict(
                form_data={'start_time': '0', 'stop_time': '11'},
                is_valid=False,
            ),
        )

        class StartStopTime(forms.StartStopTime):
            max_range = 10

        for case, data in cases.items():
            with self.subTest(case=case):
                form = StartStopTime(data['form_data'])
                is_valid = form.is_valid()
                self.assertEqual(data['is_valid'], is_valid, dict(form.errors))


class StartStopTimeTestCase(test.SimpleTestCase):

    def test_start_time_stop_time_not_required(self):
        cases = dict(
            default=dict(
                form_data={},
                is_valid=True,
            ),
            lack_of_start_time=dict(
                form_data={'stop_time': '10'},
                is_valid=True,
            ),
            lack_of_stop_time=dict(
                form_data={'start_time': '90'},
                is_valid=True,
            ),
            regular=dict(
                form_data={'start_time': '1', 'stop_time': '5'},
                is_valid=True,
            ),
            start_time_greater_then_stop_time=dict(
                form_data={'start_time': '10', 'stop_time': '5'},
                is_valid=False,
            ),
        )
        for case, data in cases.items():
            with self.subTest(case=case):
                form = forms.StartStopTimeDefaultStop(data['form_data'])
                is_valid = form.is_valid()
                self.assertEqual(data['is_valid'], is_valid, dict(form.errors))

    @mock.patch.object(time, 'time', return_value=100)
    def test_start_time_required(self, mocked_time):
        cases = dict(
            default=dict(
                form_data={},
                is_valid=False,
            ),
            lack_of_start_time=dict(
                form_data={'stop_time': '10'},
                is_valid=False,
            ),
            lack_of_stop_time=dict(
                form_data={'start_time': '90'},
                is_valid=True,
            ),
            lack_of_stop_time_invalid_range=dict(
                form_data={'start_time': '89'},
                is_valid=False,
            ),
            regular=dict(
                form_data={'start_time': '0', 'stop_time': '10'},
                is_valid=True,
            ),
            start_time_greater_then_stop_time=dict(
                form_data={'start_time': '10', 'stop_time': '5'},
                is_valid=False,
            ),
            range_greater_then_max=dict(
                form_data={'start_time': '0', 'stop_time': '11'},
                is_valid=False,
            ),
        )

        class StartStopTimeDefaultStop(forms.StartStopTimeDefaultStop):
            max_range = 10

        for case, data in cases.items():
            with self.subTest(case=case):
                form = StartStopTimeDefaultStop(data['form_data'])
                is_valid = form.is_valid()
                self.assertEqual(data['is_valid'], is_valid, dict(form.errors))
