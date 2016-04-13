import django.http
import django.test

from django.conf.urls import url
from django.test.utils import override_settings
from django.views.generic import View

import rmr.views

from rmr.utils.test import data_provider, DataSet, Parametrized


class MultipleValuesJsonView(View):

    def post(self, request):
        return django.http.JsonResponse(
            {
                key: request.POST.getlist(key)
                for key in request.POST
            },
            safe=False,
        )


urlpatterns = [
    url(r'simple', lambda request: django.http.JsonResponse(request.POST, safe=False)),
    url(r'multiple', MultipleValuesJsonView.as_view()),
]


@override_settings(ROOT_URLCONF=__name__)
class RequestDecoderTestCase(django.test.TestCase, metaclass=Parametrized):

    def setUp(self):
        self.client = django.test.Client()

    def test_wrong_charset(self):
        response = self.client.post(
            '/simple',
            data=b'\xd0',
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.HttpResponseBadRequest)
        self.assertEqual(b'bad unicode', response.content)

    @data_provider(
        DataSet(data='"'),
        DataSet(data='{'),
        DataSet(data=']'),
        DataSet(data='hello'),
        DataSet(data='hello=world'),
    )
    def test_wrong_json(self, data):
        response = self.client.post(
            '/simple',
            data=data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.HttpResponseBadRequest)
        self.assertEqual(b'malformed data', response.content)

    @data_provider(
        DataSet(request_data='{"a": 1}', response_data=b'{"a": 1}'),
        DataSet(request_data='{}', response_data=b'{}'),
        DataSet(request_data='""', response_data=b'""'),
        DataSet(request_data='"foo"', response_data=b'"foo"'),
        DataSet(request_data='[]', response_data=b'[]'),
        DataSet(request_data='[1, 2, 3]', response_data=b'[1, 2, 3]'),
        DataSet(request_data='null', response_data=b'null'),
        DataSet(request_data='{"foo": {"bar": "bar"}}',
                response_data=b'{"foo": {"bar": "bar"}}'),
        DataSet(request_data='{"foo": {"bar": [1, 2, 3]}}',
                response_data=b'{"foo": {"bar": [1, 2, 3]}}'),
    )
    def test_valid_json(self, request_data, response_data):
        response = self.client.post(
            '/simple',
            data=request_data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.JsonResponse)
        self.assertEqual(rmr.views.Json.http_code, response.status_code)
        self.assertEqual(response_data, response.content)

    @data_provider(
        DataSet(request_data='{"foo": ["bar", "baz"]}',
                response_data=b'{"foo": ["bar", "baz"]}'),
        DataSet(request_data='{"foo": [{"bar": "bar"}, {"baz": "baz"}]}',
                response_data=b'{"foo": [{"bar": "bar"}, {"baz": "baz"}]}'),
    )
    def test_valid_json_with_multiple_values(self, request_data, response_data):
        response = self.client.post(
            '/multiple',
            data=request_data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.JsonResponse)
        self.assertEqual(rmr.views.Json.http_code, response.status_code)
        self.assertEqual(response_data, response.content)
