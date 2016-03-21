import json
import urllib.parse

from datetime import datetime
from unittest import mock

import django.test

from django import forms
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.decorators import method_decorator

from rmr.errors import ClientError, ServerError
from rmr.utils.test import data_provider, DataSet, Parametrized
from rmr.views import Json
from rmr.views.decorators.validation import validate_request


class JsonWithWarning(Json):

    def get(self, request):
        raise ClientError('WARNING_TEST_CASE', code='warning_test_case')


class JsonWithError(Json):

    def get(self, request):
        raise ServerError('ERROR_TEST_CASE', code='error_test_case')


class JsonWithoutError(Json):

    def get(self, request):
        pass


class CacheJson(Json):

    timestamp = None

    @classmethod
    def last_modified(cls, request, *args, **kwargs):
        if cls.timestamp:
            return datetime.fromtimestamp(cls.timestamp)
        return datetime(2015, 1, 1, tzinfo=timezone.utc)

    @classmethod
    def expires(cls):
        return 3600

    def get(self, request):
        pass

    def post(self, request):
        pass


class ValidationJson(Json):

    class GetValidationForm(forms.Form):
        get_required = forms.IntegerField()
        get_not_required = forms.IntegerField(required=False)

    class PostValidationForm(forms.Form):
        post_required = forms.IntegerField()
        post_not_required = forms.IntegerField(required=False)

    @method_decorator(validate_request(get=GetValidationForm))
    def get(self, request):
        pass

    @method_decorator(validate_request(post=PostValidationForm))
    def post(self, request):
        pass

    @method_decorator(validate_request(
        get=GetValidationForm,
        post=PostValidationForm,
    ))
    def patch(self, request):
        pass


urlpatterns = [
    url(r'warning', JsonWithWarning.as_view(), name='warning'),
    url(r'error', JsonWithError.as_view(), name='error'),
    url(r'ok', JsonWithoutError.as_view(), name='ok'),
    url(r'cache', CacheJson.as_view(), name='cache'),
    url(r'last_modified', CacheJson.as_view(), name='last_modified'),
    url(r'validate', ValidationJson.as_view(), name='validate'),
]


@override_settings(ROOT_URLCONF=__name__)
class JsonTestCase(django.test.TestCase, metaclass=Parametrized):

    @data_provider(
        DataSet(
            timestamp1=None,
            timestamp2=None,
            cache_stale_expected=False,
        ),
        DataSet(
            timestamp1=1420070400,
            timestamp2=1420070401,
            cache_stale_expected=True,
        ),
    )
    def test_last_modified_as_cache_key(self, timestamp1, timestamp2, cache_stale_expected):
        client = django.test.Client()

        mocked_get = mock.MagicMock(return_value=None)
        with mock.patch.multiple(CacheJson, timestamp=timestamp1, get=mocked_get):
            client.get(
                reverse('last_modified'),
            )
            self.assertTrue(mocked_get.called)

        mocked_get = mock.MagicMock(return_value=None)
        with mock.patch.multiple(CacheJson, timestamp=timestamp1, get=mocked_get):
            client.get(
                reverse('last_modified'),
            )
            self.assertFalse(mocked_get.called)

        mocked_get = mock.MagicMock(return_value=None)
        with mock.patch.multiple(CacheJson, timestamp=timestamp2, get=mocked_get):
            client.get(
                reverse('last_modified'),
            )
            self.assertEqual(cache_stale_expected, mocked_get.called)

        mocked_get = mock.MagicMock(return_value=None)
        with mock.patch.multiple(CacheJson, timestamp=timestamp2, get=mocked_get):
            client.get(
                reverse('last_modified'),
            )
            self.assertFalse(mocked_get.called)

    @data_provider(
        DataSet('warning', ClientError.http_code),
        DataSet('error', ServerError.http_code),
        DataSet('ok', Json.http_code),
    )
    def test_status_code(self, url_name, expected_status_code):
        client = django.test.Client()
        response = client.get(reverse(url_name))
        self.assertEqual(expected_status_code, response.status_code)

    def test_response_headers(self):
        client = django.test.Client()

        # GET request of not cached content with If-Modified-Since provided
        response = client.get(
            reverse('cache'),
            HTTP_IF_MODIFIED_SINCE='Thu, 01 Jan 2015 00:00:00 GMT',
        )
        self.assertIn('Content-Length', response)
        self.assertIn('Last-Modified', response)
        self.assertIn('Expires', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('max-age=3600', response['Cache-Control'])
        self.assertEqual('Thu, 01 Jan 2015 00:00:00 GMT', response['Last-Modified'])
        self.assertEqual('0', response['Content-Length'])
        self.assertEqual(304, response.status_code)

        # GET request of cachable content
        response = client.get(reverse('cache'))
        self.assertEqual(Json.http_code, response.status_code)
        self.assertIn('Content-Length', response)
        self.assertIn('Content-Type', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('Expires', response)
        self.assertIn('Last-Modified', response)
        self.assertEqual('14', response['Content-Length'])
        self.assertIn('max-age=3600', response['Cache-Control'])
        self.assertEqual('Thu, 01 Jan 2015 00:00:00 GMT', response['Last-Modified'])
        self.assertEqual('application/json', response['Content-Type'])

        # POST request of cachable content
        response = client.post(reverse('cache'))
        self.assertEqual(Json.http_code, response.status_code)
        self.assertIn('Content-Length', response)
        self.assertIn('Content-Type', response)
        self.assertNotIn('Expires', response)
        self.assertNotIn('Cache-Control', response)
        self.assertNotIn('Last-Modified', response)
        self.assertEqual('14', response['Content-Length'])
        self.assertEqual('application/json', response['Content-Type'])

        # GET request of cached content with If-Modified-Since provided
        response = client.get(
            reverse('cache'),
            HTTP_IF_MODIFIED_SINCE='Thu, 01 Jan 2015 00:00:00 GMT',
        )
        self.assertIn('Content-Length', response)
        self.assertIn('Last-Modified', response)
        self.assertIn('Expires', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('max-age=3600', response['Cache-Control'])
        self.assertEqual('Thu, 01 Jan 2015 00:00:00 GMT', response['Last-Modified'])
        self.assertEqual('0', response['Content-Length'])
        self.assertEqual(304, response.status_code)

        # GET request of cached content without If-Modified-Since provided
        response = client.get(reverse('cache'))
        self.assertEqual(Json.http_code, response.status_code)
        self.assertIn('Content-Length', response)
        self.assertIn('Content-Type', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('Expires', response)
        self.assertIn('Last-Modified', response)
        self.assertEqual('14', response['Content-Length'])
        self.assertIn('max-age=3600', response['Cache-Control'])
        self.assertEqual('Thu, 01 Jan 2015 00:00:00 GMT', response['Last-Modified'])
        self.assertEqual('application/json', response['Content-Type'])

        # POST request of cachable content with If-Modified-Since provided
        response = client.post(
            reverse('cache'),
            HTTP_IF_MODIFIED_SINCE='Thu, 01 Jan 2015 00:00:00 GMT',
        )
        self.assertEqual(Json.http_code, response.status_code)
        self.assertIn('Content-Length', response)
        self.assertNotIn('Expires', response)
        self.assertNotIn('Cache-Control', response)
        self.assertNotIn('Last-Modified', response)
        self.assertEqual('14', response['Content-Length'])
        self.assertEqual('application/json', response['Content-Type'])

        # GET request of non-cachable content
        response = client.get(reverse('ok'))
        self.assertIn('Cache-Control', response)
        self.assertIn('Content-Length', response)
        self.assertIn('Content-Type', response)
        self.assertIn('max-age=0', response['Cache-Control'])
        self.assertEqual('14', response['Content-Length'])
        self.assertEqual('application/json', response['Content-Type'])

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
        DataSet(
            offset=None,
            limit=None,
            limit_default=None,
            limit_max=10,
            expected_error_code='limit_not_provided',
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

    def test_validate_request(self):
        client = django.test.Client()
        path = reverse('validate')

        # GET validation
        response = client.get(path, data=dict(
            get_required=123,
            get_not_required=123,
            unknown=123,
        ))
        self.assertEqual(
            200,
            response.status_code,
        )

        # POST validation
        response = client.post(
            path,
            data=json.dumps(dict(
                post_required=123,
                post_not_required=123,
                unknown=123,
            )),
            content_type='application/json',
        )
        self.assertEqual(
            200,
            response.status_code,
        )

        # GET and POST validation
        response = client.patch(
            '{path}?{query}'.format(
                path=path,
                query=urllib.parse.urlencode(dict(get_required=123)),
            ),
            data=json.dumps(dict(post_required=123)),
            content_type='application/json',
        )
        self.assertEqual(
            200,
            response.status_code,
        )

    @data_provider(
        DataSet(
            method='GET',
            query={},
            data={},
            invalid_params={'get_required'},
        ),
        DataSet(
            method='POST',
            query={},
            data={},
            invalid_params={'post_required'},
        ),
        DataSet(
            method='PATCH',
            query={},
            data={},
            invalid_params={'post_required', 'get_required'},
        ),
        DataSet(
            method='PATCH',
            query=dict(get_not_required='wrong_value'),
            data=dict(post_not_required='wrong_value'),
            invalid_params={'post_required', 'get_required', 'get_not_required', 'post_not_required'},
        ),
    )
    def test_validate_request_errors(self, method, query, data, invalid_params):
        client = django.test.Client()
        path = reverse('validate')
        response = client.generic(
            method=method,
            path='{path}?{query}'.format(
                path=path,
                query=urllib.parse.urlencode(query),
            ),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(
            400,
            response.status_code,
        )
        data = json.loads(response.content.decode())
        actual_invalid_params = data.get('error', {}).get('description', {}).keys()
        self.assertSetEqual(invalid_params, set(actual_invalid_params))
