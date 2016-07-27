import functools
import warnings


def replace_if(condition, replacement):
    """
    If `condition(...)` is True then returns result of `replacement(...)`
    evaluation and result of original function otherwise
    """
    def _decorator(fn):
        @functools.wraps(fn)
        def _fn(*args, **kwargs):
            if condition(*args, **kwargs):
                return replacement(*args, **kwargs)
            return fn(*args, **kwargs)
        return _fn
    return _decorator


def conditional(condition, fn_true=None, fn_false=None):
    """
    Depending on result of `condition` executes either `fn_true` or `fn_false`
    """
    warnings.warn(
        '`conditional` decorator is deprecated and will be removed '
        'in rmr-django 2.0, use `replace_if` instead',
        DeprecationWarning,
    )

    def _decorator(fn):
        @functools.wraps(fn)
        def _fn(*args, **kwargs):
            callback = fn
            if condition(*args, **kwargs):
                if callable(fn_true):
                    callback = fn_true
            elif callable(fn_false):
                callback = fn_false
            return callback(*args, **kwargs)
        return _fn
    return _decorator
