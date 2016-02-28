import contextlib


@contextlib.contextmanager
def patch(obj, attr, value, default=None):
    """
    Context manager inside of which `obj`'s `attr` will be equal `value`
    """
    original = getattr(obj, attr, default)
    setattr(obj, attr, value)
    yield
    setattr(obj, attr, original)
