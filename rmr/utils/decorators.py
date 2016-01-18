import functools


def conditional(condition, fn_true=None, fn_false=None):
    """
    Depending on result of `condition` executes either `fn_true` or `fn_false`
    """
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
