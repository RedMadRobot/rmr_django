import warnings


def cache_page(*args, **kwargs):
    warnings.warn(
        'cache_page is deprecated and no longer needed to use cache, '
        'it will be removed in rmr-django 2.0',
        DeprecationWarning,
    )

    def _decorator(fn):
        return fn
    return _decorator
