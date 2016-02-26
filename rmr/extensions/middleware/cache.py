from django.middleware.cache import UpdateCacheMiddleware
from django.utils.cache import patch_cache_control
from django.utils.http import parse_http_date
from django.utils.timezone import now


class FixCacheControlMaxAge(UpdateCacheMiddleware):
    """
    Replaces 'max-age' value of 'Cache-Control' header by value calculated
    from 'Expires' header's date

    Django's FetchFromCacheMiddleware gets 'Cache-Control' header
    for the response from the cache where it's value corresponds
    to the moment original response was generated and thus maybe
    incorrect for the current time
    """

    def process_response(self, request, response):
        should_update_cache = self._should_update_cache(request, response)
        if not should_update_cache and 'Expires' in response:
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)
        return response
