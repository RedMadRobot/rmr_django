from django.http import HttpResponseNotModified
from django.middleware import cache
from django.utils.cache import patch_cache_control, get_conditional_response, patch_response_headers
from django.utils.http import parse_http_date, parse_http_date_safe
from django.utils.timezone import now

from rmr.utils.patch import patch


class UpdateCacheMiddleware(cache.UpdateCacheMiddleware):
    """
    Do the same as the original one but try first to use 'key_prefix' from
    the request where it might be saved earlier

    see https://code.djangoproject.com/ticket/15855
    """

    def process_response(self, request, response):
        key_prefix = getattr(request, '_cache_key_prefix', self.key_prefix)
        cache_timeout = getattr(request, '_cache_cache_timeout', self.cache_timeout)

        if isinstance(response, HttpResponseNotModified):
            patch_response_headers(response, cache_timeout=cache_timeout)
            return response
        elif 'Expires' in response:
            # Replace 'max-age' value of 'Cache-Control' header by one
            # calculated from the 'Expires' header's date.
            # This is necessary because of Django's `FetchFromCacheMiddleware`
            # gets 'Cache-Control' header from the cache
            # where 'max-age' corresponds to the moment original response
            # was generated and thus may be already stale for the current time
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)

        with patch(self, 'key_prefix', key_prefix):
            with patch(self, 'cache_timeout', cache_timeout):
                return super().process_response(request, response)


class CacheMiddleware(cache.CacheMiddleware):
    """
    Despite of the original one this middleware supports callable 'key_prefix'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callable(self.key_prefix):
            self.key_function = self.key_prefix

    def key_function(self, request, *args, **kwargs):
        return self.key_prefix

    def get_key_prefix(self, request):
        key_prefix = self.key_function(
            request,
            *request.resolver_match.args,
            **request.resolver_match.kwargs
        )
        if key_prefix is not None:
            key_prefix = str(key_prefix).replace(' ', '_')
        return key_prefix

    def process_request(self, request):
        self.key_prefix = self.get_key_prefix(request)
        request._cache_cache_timeout = int(self.cache_timeout)
        response = super().process_request(request)
        if response:
            etag = response.get('ETag')
            last_modified = response.get('Last-Modified')
            if not (etag or last_modified):
                return response
            response = get_conditional_response(
                request,
                etag=etag,
                last_modified=last_modified and parse_http_date_safe(last_modified),
                response=response,
            )
            response['Last-Modified'] = last_modified
            return response

    def process_response(self, request, response):
        request._cache_key_prefix = self.get_key_prefix(request)

        # you must add rmr's UpdateCacheMiddleware at the top of the
        # MIDDLEWARE_CLASSES to be able to save responses in the cache
        # see https://code.djangoproject.com/ticket/15855
        return response
