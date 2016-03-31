import functools

from rmr.errors import ClientError


def authentication_required(func):
    @functools.wraps(func)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise ClientError(
                'Authentication required',
                http_code=401,
                code='authentication_required',
            )
        return func(request, *args, **kwargs)
    return _wrapper
