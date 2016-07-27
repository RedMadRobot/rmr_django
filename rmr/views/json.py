import contextlib
import functools
import logging
import warnings

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.utils import six
from django.utils.decorators import classonlymethod
from django.views.decorators import http
from django.views.generic import View

from djangocache import cache_page

import rmr

from rmr.utils import decorators

request_logger = logging.getLogger('rmr.request')

response_logger = logging.getLogger('rmr.response')


class Json(View):

    http_code = 200

    logger = logging.getLogger('rmr.view')

    def __init__(self, request: HttpRequest=None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    @classmethod
    def _expires(cls, request, *args, **kwargs):
        if not six.get_function_defaults(cls.expires):
            warnings.warn(
                'In rmr-django 2.0 Json.expires() will be called with '
                'additional arguments: (request, *args, **kwargs)',
                category=RuntimeWarning,
            )
        return cls.expires()

    @classmethod
    def expires(cls, request=None, *args, **kwargs):
        """
        Lazy evaluated response cache TTL in seconds,
        corresponds to the Cache-Control's max-age value
        and also used to evaluate Expires header
        """
        return 0  # cache disabled

    @classmethod
    def last_modified(cls, request, *args, **kwargs):
        """
        Lazy evaluated value of Last-Modified header
        """
        pass

    @classmethod
    def etag(cls, request, *args, **kwargs):
        """
        Lazy evaluated value of ETag header
        """
        pass

    @classonlymethod
    def as_view(cls, **initkwargs):
        def normalize_key_prefix(key_prefix):
            def _key_prefix(request, *args, **kwargs):
                return str(
                    key_prefix(request, *args, **kwargs)
                ).replace(' ', '_')
            return _key_prefix

        patched_view = view = super().as_view(**initkwargs)

        patched_view = http.etag(cls.etag)(patched_view)
        patched_view = http.last_modified(cls.last_modified)(patched_view)
        patched_view = cache_page(
            cache_timeout=cls._expires,
            key_prefix=normalize_key_prefix(cls.last_modified),
        )(patched_view)

        view = decorators.replace_if(
            lambda request, *args, **kwargs: request.method in ('GET', 'HEAD'),
            replacement=patched_view,
        )(view)

        @functools.wraps(cls.as_view)
        def logging_view(request, *args, **kwargs):

            request_logger.debug(
                'request_method: %(request_method)s, '
                'request_path: %(request_path)s, '
                'request_headers: %(request_headers)s, '
                'request_params: %(request_params)s, '
                'request_data: %(request_data)s, ',
                dict(
                    request_method=request.method,
                    request_path=request.path,
                    request_headers=request.META,
                    request_params=request.GET,
                    request_data=request.POST,
                ),
            )

            response = view(request, *args, **kwargs)

            response_logger.debug(
                'response_code: %(response_code)s, '
                'response_headers: %(response_headers)s, '
                'response_data: %(response_data)s',
                dict(
                    response_code=response.status_code,
                    response_headers=response.items(),
                    response_data=response.content,
                ),
            )

            return response

        return logging_view

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.request = request
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            http_code = self.http_code
            api_result = dict(
                data=result,
            )
        except rmr.Error as error:

            response_logger.log(
                error.level,
                '%(code)s: %(message)s',
                dict(message=error.message, code=error.code),
            )

            http_code = error.http_code
            api_result = dict(
                error=dict(
                    code=error.code,
                    description=error.message,
                ),
            )

        response = JsonResponse(api_result, status=http_code, safe=False)
        response.setdefault('Content-Length', len(response.content))
        return response

    @staticmethod
    def get_range(offset=None, limit=None, limit_default=None, limit_max=None):
        warnings.warn(
            'rmr.views.Json.get_range() is deprecated and will be removed '
            'in rmr-django 2.0, use rmr.utils.range.get_range() instead and/or '
            'rmr.forms.OffsetLimit form to validate offset/limit request '
            'params',
            category=DeprecationWarning,
        )
        start = 0
        stop = None
        with contextlib.suppress(ValueError):
            start = offset and int(offset) or start
            if start < 0:
                raise rmr.ClientError(
                    'Offset must be a positive number',
                    code='incorrect_offset',
                )
            limit = limit and int(limit) or limit_default
            if limit is not None:
                if limit <= 0:
                    raise rmr.ClientError(
                        'Limit must be a positive number',
                        code='incorrect_limit',
                    )
                if limit_max and limit > limit_max:
                    raise rmr.ClientError(
                        'Maximum value of limit must be '
                        'less then or equal {}'.format(limit_max),
                        code='max_limit_exceeded',
                    )
                stop = start + limit
            elif limit_max:
                raise rmr.ClientError(
                    'Limit must be provided',
                    code='limit_not_provided',
                )

            return start, stop

        raise rmr.ClientError(
            'Limit and offset must be a numbers if provided',
            code='incorrect_limit_or_offset',
        )
