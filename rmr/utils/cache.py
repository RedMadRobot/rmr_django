from django.core.cache.backends import memcached
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.functional import cached_property


class CacheTimeout:
    """Lazy evaluated cache_timeout value
    for `django.views.decorators.cache.cache_page` decorator

    To use this decorator you must set :code:`rmr.utils.cache.RmrLibMCCache`
    as custom cache backend
    """

    def __init__(self, get_cache_timeout):
        self.get_cache_timeout = get_cache_timeout

    @cached_property
    def cache_timeout(self):
        return self.get_cache_timeout()

    def __eq__(self, other):
        return self.cache_timeout == other

    def __lt__(self, other):
        return self.cache_timeout < other

    def __radd__(self, other):
        return self.cache_timeout + other

    def __str__(self):
        return str(self.cache_timeout)


class RmrLibMCCache(memcached.PyLibMCCache):
    """Custom cache backend which enables to use
    :code:`rmr.utils.cache.CacheTimeout`
    """

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        if timeout is not DEFAULT_TIMEOUT:
            timeout = 0 + timeout
        return super().get_backend_timeout(timeout=timeout)
