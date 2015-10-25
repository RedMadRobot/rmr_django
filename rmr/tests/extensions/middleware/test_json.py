import django.http
import django.test

from django.conf.urls import url
from django.test.utils import override_settings

import rmr.views

from rmr.utils.test import data_provider, DataSet, Parametrized

urlpatterns = [
    url(r'', lambda request: django.http.JsonResponse(request.POST)),
]


@override_settings(ROOT_URLCONF=__name__)
class RequestDecoderTestCase(django.test.TestCase, metaclass=Parametrized):

    def setUp(self):
        self.client = django.test.Client()

    def test_wrong_charset(self):
        response = self.client.post(
            '/',
            data=b'\xd0',
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.HttpResponseBadRequest)
        self.assertEqual(b'bad unicode', response.content)

    @data_provider(
        DataSet(data='"'),
        DataSet(data='""'),
        DataSet(data='[]'),
        DataSet(data='null'),
        DataSet(data='{'),
        DataSet(data='hello'),
        DataSet(data='hello=world'),
    )
    def test_wrong_json(self, data):
        response = self.client.post(
            '/',
            data=data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.HttpResponseBadRequest)
        self.assertEqual(b'malformed data', response.content)

    @data_provider(
        DataSet(data='{"a": 1}'),
        DataSet(data='{}'),
    )
    def test_valid_json(self, data):
        response = self.client.post(
            '/',
            data=data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.JsonResponse)
        self.assertEqual(rmr.views.Json.http_code, response.status_code)
        self.assertEqual(response.content.decode('utf-8'), data)
