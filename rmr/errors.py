import logging


class Error(Exception):

    level = logging.NOTSET

    http_code = NotImplemented

    message = NotImplemented

    code = NotImplemented

    def __init__(self, message=None, *, code=None, level=None, http_code=None):
        super().__init__(message)
        self.message = message or self.message
        self.code = code or self.code
        self.level = level or self.level
        self.http_code = http_code or self.http_code

    def __str__(self):
        return '[{code}] {message}'.format(message=self.message, code=self.code)


class ServerError(Error):

    level = logging.ERROR

    http_code = 500


class ClientError(Error):

    level = logging.WARNING

    http_code = 400


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
