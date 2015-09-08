import django.http
import django.test

from rmr.tests import data_provider, DataSet, Parametrized


class DecoderTestCase(django.test.TestCase, metaclass=Parametrized):

    def test_wrong_charset(self):
        client = django.test.Client()
        response = client.post(
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
        client = django.test.Client()
        response = client.post(
            '/',
            data=data,
            content_type='application/json',
        )
        self.assertIsInstance(response, django.http.HttpResponseBadRequest)
        self.assertEqual(b'malformed data', response.content)
