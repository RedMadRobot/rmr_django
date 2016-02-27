from django.middleware import cache
from django.utils.cache import patch_cache_control
from django.utils.http import parse_http_date
from django.utils.timezone import now


class CacheMiddleware(cache.CacheMiddleware):
    """
    Despite of original one this middleware supports callable 'key_prefix'
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callable(self.key_prefix):
            self.key_function = self.key_prefix

    def key_function(self, request, *args, **kwargs):
        return self.key_prefix

    def patch_key_prefix(self, request):
        self.key_prefix = self.key_function(
            request,
            *request.resolver_match.args,
            **request.resolver_match.kwargs
        )

    def process_request(self, request):
        self.patch_key_prefix(request)
        return super().process_request(request)

    def process_response(self, request, response):
        self.patch_key_prefix(request)
        if 'Expires' in response:
            # Replace 'max-age' value of 'Cache-Control' header by one
            # calculated from the 'Expires' header's date.
            # This is necessary because of Django's `FetchFromCacheMiddleware`
            # gets 'Cache-Control' header from the cache
            # where 'max-age' corresponds to the moment original response
            # was generated and thus may be already stale for the current time
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)
        return super().process_response(request, response)
