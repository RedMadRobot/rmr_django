import django.test

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from rmr.errors import ClientError, ServerError
from rmr.utils.test import data_provider, DataSet, Parametrized
from rmr.views import Json


class JsonWithWarning(Json):

    type = 'WARNING_TEST_CASE'

    def get(self, request):
        raise ClientError('WARNING_TEST_CASE', code='warning_test_case')


class JsonWithError(Json):

    type = 'ERROR_TEST_CASE'

    def get(self, request):
        raise ServerError('ERROR_TEST_CASE', code='error_test_case')


class JsonWithoutError(Json):

    type = 'NORMAL_TEST_CASE'

    def get(self, request):
        pass

urlpatterns = [
    url(r'warning', JsonWithWarning.as_view(), name='warning'),
    url(r'error', JsonWithError.as_view(), name='error'),
    url(r'ok', JsonWithoutError.as_view(), name='ok'),
]


@override_settings(ROOT_URLCONF=__name__)
class JsonTestCase(django.test.TestCase, metaclass=Parametrized):

    @data_provider(
        DataSet('warning', ClientError.http_code),
        DataSet('error', ServerError.http_code),
        DataSet('ok', Json.http_code),
    )
    def test_status_code(self, url_name, expected_status_code):
        client = django.test.Client()
        response = client.get(reverse(url_name))
        self.assertEqual(expected_status_code, response.status_code)

    @data_provider(
        DataSet(
            offset=None,
            limit=None,
            limit_default=None,
            limit_max=None,
            expected=(0, None),
        ),
        DataSet(
            offset=5,
            limit=10,
            limit_default=None,
            limit_max=None,
            expected=(5, 15),
        ),
        DataSet(
            offset='5',
            limit='10',
            limit_default=None,
            limit_max=None,
            expected=(5, 15),
        ),
        DataSet(
            offset=None,
            limit=10,
            limit_default=None,
            limit_max=None,
            expected=(0, 10),
        ),
        DataSet(
            offset=5,
            limit=None,
            limit_default=None,
            limit_max=None,
            expected=(5, None),
        ),
        DataSet(
            offset=None,
            limit=None,
            limit_default=10,
            limit_max=None,
            expected=(0, 10),
        ),
        DataSet(
            offset=5,
            limit=None,
            limit_default=10,
            limit_max=None,
            expected=(5, 15),
        ),
        DataSet(
            offset=5,
            limit=None,
            limit_default=10,
            limit_max=None,
            expected=(5, 15),
        ),
        DataSet(
            offset=5,
            limit=10,
            limit_default=None,
            limit_max=10,
            expected=(5, 15),
        ),
    )
    def test_get_range(self, offset, limit, limit_default, limit_max, expected):
        self.assertEqual(
            expected,
            Json.get_range(
                offset=offset,
                limit=limit,
                limit_default=limit_default,
                limit_max=limit_max,
            ),
        )

    @data_provider(
        DataSet(
            offset=None,
            limit=-1,
            limit_default=None,
            limit_max=None,
            expected_error_code='incorrect_limit',
        ),
        DataSet(
            offset=-1,
            limit=None,
            limit_default=None,
            limit_max=None,
            expected_error_code='incorrect_offset',
        ),
        DataSet(
            offset='blah',
            limit=None,
            limit_default=None,
            limit_max=None,
            expected_error_code='incorrect_limit_or_offset',
        ),
        DataSet(
            offset=None,
            limit='blah',
            limit_default=None,
            limit_max=None,
            expected_error_code='incorrect_limit_or_offset',
        ),
        DataSet(
            offset=None,
            limit=11,
            limit_default=None,
            limit_max=10,
            expected_error_code='max_limit_exceeded',
        ),
        DataSet(
            offset=None,
            limit=None,
            limit_default=11,
            limit_max=10,
            expected_error_code='max_limit_exceeded',
        ),
    )
    def test_get_range_errors(self, offset, limit, limit_default, limit_max, expected_error_code):
        with self.assertRaises(ClientError) as error:
            Json.get_range(
                offset=offset,
                limit=limit,
                limit_default=limit_default,
                limit_max=limit_max,
            )
        self.assertEqual(expected_error_code, error.exception.code)
