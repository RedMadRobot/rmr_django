from django.utils.cache import patch_cache_control
from django.utils.http import parse_http_date
from django.utils.timezone import now


class FixCacheControlMaxAge:
    """
    Replaces 'max-age' value of 'Cache-Control' header by value calculated
    from 'Expires' header's date

    Must be placed before Django's 'FetchFromCacheMiddleware' due to fact
    that the last one gets 'Cache-Control' header from the cache where
    it's value corresponds to the moment original response was generated
    and that's why maybe incorrect for the current time
    """

    @staticmethod
    def process_response(request, response):
        if 'Expires' in response:
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)
        return response
