import warnings


class UpdateCacheMiddleware:

    def __init__(self):
        warnings.warn(
            'UpdateCacheMiddleware no longer needed to use cache '
            'and will be removed in rmr-django 2.0',
            RuntimeWarning,
        )


class CacheMiddleware:

    def __init__(self):
        warnings.warn(
            'CacheMiddleware no longer needed to use cache '
            'and will be removed in rmr-django 2.0',
            RuntimeWarning,
        )
