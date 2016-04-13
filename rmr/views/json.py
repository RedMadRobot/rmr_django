import contextlib
import functools
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.utils.decorators import classonlymethod
from django.views.decorators.http import last_modified
from django.utils.functional import lazy
from django.views.generic import View

import rmr

from rmr.utils.cache import cache_page
from rmr.utils.decorators import conditional

request_logger = logging.getLogger('rmr.request')

response_logger = logging.getLogger('rmr.response')


class Json(View):

    http_code = 200

    logger = logging.getLogger('rmr.view')

    def __init__(self, request: HttpRequest=None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    @classmethod
    def expires(cls):
        """
        Lazy evaluated 'max-age' value of Cache-Control header
        """
        return settings.CACHE_MIDDLEWARE_SECONDS

    @classmethod
    def last_modified(cls, request, *args, **kwargs):
        """
        Lazy evaluated value of Last-Modified header
        """
        pass

    @classmethod
    def cache_headers_allowed(cls, request, *args, **kwargs):
        return request.method in ('GET', 'HEAD')

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = patched_view = super().as_view(**initkwargs)
        last_modified_evaluator = functools.lru_cache()(cls.last_modified)
        patched_view = last_modified(last_modified_evaluator)(patched_view)
        patched_view = cache_page(
            lazy(cls.expires, int)(),
            key_prefix=last_modified_evaluator,
        )(patched_view)
        view = conditional(cls.cache_headers_allowed, patched_view)(view)

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
        # TODO make another method with offset/limit validation delegated to rmr.forms.OffsetLimit
        # TODO make deprecated
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
