import functools

from rmr.errors import ClientError


def authentication_required(fn):
    @functools.wraps(fn)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise ClientError(
                'Authentication required',
                http_code=401,
                code='authentication_required',
            )
        return fn(request, *args, **kwargs)
    return _wrapper
