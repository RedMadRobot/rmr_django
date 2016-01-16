from django.utils.functional import cached_property


class CacheTimeout:
    """Lazy evaluated cache_timeout value
    for `django.views.decorators.cache.cache_page` decorator
    """

    def __init__(self, get_cache_timeout=None):
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
