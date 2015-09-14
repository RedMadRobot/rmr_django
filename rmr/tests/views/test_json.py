import django.test
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from rmr.errors import ApiWarning, ApiError
from rmr.tests import data_provider, DataSet, Parametrized
from rmr.views import Json


class JsonWithWarning(Json):

    type = 'WARNING_TEST_CASE'

    def get(self, request):
        raise ApiWarning('WARNING_TEST_CASE', code='warning_test_case')


class JsonWithError(Json):

    type = 'ERROR_TEST_CASE'

    def get(self, request):
        raise ApiError('ERROR_TEST_CASE', code='error_test_case')


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
        DataSet('warning', ApiWarning.http_code),
        DataSet('error', ApiError.http_code),
        DataSet('ok', Json.http_code),
    )
    def test_status_code(self, url_name, expected_status_code):
        client = django.test.Client()
        response = client.get(reverse(url_name))
        self.assertEqual(expected_status_code, response.status_code)
