from django.utils.cache import patch_cache_control
from django.utils.http import parse_http_date
from django.utils.timezone import now


class FixCacheControlMaxAge:

    @staticmethod
    def process_response(request, response):
        if 'Expires' in response:
            expires = parse_http_date(response['Expires'])
            timeout = expires - int(now().timestamp())
            patch_cache_control(response, max_age=timeout)
        return response
