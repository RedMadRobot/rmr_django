import json
import urllib.parse

import django.test

from django import forms
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils.decorators import method_decorator

from rmr.errors import ClientError, ServerError
from rmr.utils.test import data_provider, DataSet, Parametrized
from rmr.views import Json, validate_request


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
    url(r'validate', ValidationJson.as_view(), name='validate'),
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

    def test_validate_request(self):
        client = django.test.Client()
        path = reverse('validate')

        # GET validation
        response = client.get(path, data=dict(
            get_required=123,
            get_not_required=123,
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
