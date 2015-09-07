from rmr.errors import ApiWarning

from .json import Json


def anonymous_required(fn):
    def _fn(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise ApiWarning(
                'User already registered',
                code='user_already_registered',
            )
        return fn(self, request, *args, **kwargs)
    return _fn


def login_required(fn):
    def _fn(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            raise ApiWarning(
                'User not authenticated',
                code='user_not_authenticated',
            )
        return fn(self, request, *args, **kwargs)
    return _fn
