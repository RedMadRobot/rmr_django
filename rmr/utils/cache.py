from django.utils.decorators import decorator_from_middleware_with_args

from rmr.extensions.middleware.cache import CacheMiddleware


def cache_page(cache_timeout, *, cache=None, key_prefix=None):
    """
    This decorator is very similar to `django.views.decorators.cache.cache_page`
    but instead of `django.middleware.cache.CacheMiddleware` it uses overridden
    version
    """
    return decorator_from_middleware_with_args(CacheMiddleware)(
        cache_timeout=cache_timeout, cache_alias=cache, key_prefix=key_prefix
    )
