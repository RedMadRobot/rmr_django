import logging


class ApiError(Exception):

    level = logging.ERROR

    http_status_code = 500

    def __init__(self, message, code=None, level=None, *args, **kwargs):
        super().__init__(message, code)
        self.message = message
        self.code = code
        self.level = level or self.level

    def __str__(self):
        return '[{code}] {message}'.format(message=self.message, code=self.code)


class ApiWarning(ApiError):

    level = logging.WARNING

    http_status_code = 400


def handle_error(error, exception=None):
    def _decorator(fn):
        def _fn(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except error:
                if exception:
                    raise exception
        return _fn
    return _decorator
