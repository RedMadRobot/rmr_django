import contextlib
import logging

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import last_modified
from django.utils.functional import lazy
from django.views.generic import View

import rmr

from rmr.utils.decorators import conditional


class HttpCacheHeaders(type):

    dispatch_original = None

    def expires(cls):
        """
        Lazy evaluated value of cache TTL in seconds
        """
        return 0

    def cache_control(cls):
        return dict(
            public=True,
            max_age=lazy(cls.expires, int)(),
        )

    def last_modified(cls, request: HttpRequest, *args, **kwargs):
        pass

    @staticmethod
    def cache_headers_allowed(view, request, *args, **kwargs):
        return request.method in ('GET', 'HEAD')

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dispatch = cls.dispatch_original = cls.dispatch_original or cls.dispatch
        dispatch = method_decorator(last_modified(cls.last_modified))(dispatch)
        dispatch = method_decorator(cache_control(**cls.cache_control()))(dispatch)
        cls.dispatch = conditional(cls.cache_headers_allowed, dispatch)(cls.dispatch)


class Json(View, metaclass=HttpCacheHeaders):

    http_code = 200

    logger = logging.getLogger('rmr.request')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        http_code = self.http_code
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            api_result = dict(
                data=result,
            )
        except rmr.Error as error:

            self.logger.log(
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

        self.logger.debug(
            'request_method: %(request_method)s, '
            'request_path: %(request_path)s, '
            'request_headers: %(request_headers)s, '
            'request_params: %(request_params)s, '
            'request_data: %(request_data)s, '
            'response_code: %(response_code)s, '
            'response_data: %(response_data)s',
            dict(
                request_method=request.method,
                request_path=request.path,
                request_headers=request.META,
                request_params=request.GET,
                request_data=request.POST,
                response_code=http_code,
                response_data=api_result,
            ),
        )

        response = JsonResponse(api_result, status=http_code)
        response['Content-Length'] = str(len(response.content))

        return response

    @staticmethod
    def get_range(offset=None, limit=None, limit_default=None, limit_max=None):
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

            return start, stop

        raise rmr.ClientError(
            'Limit and offset must be a numbers if provided',
            code='incorrect_limit_or_offset',
        )
