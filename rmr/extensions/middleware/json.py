import json

from django.conf import settings
from django.http import HttpResponseBadRequest, QueryDict


class RequestDecoder:

    content_type = 'application/json'

    allowed_methods = {
        'POST', 'PUT', 'PATCH',
    }

    def process_request(self, request):
        if request.method not in self.allowed_methods:
            return
        content_type = request.META.get('CONTENT_TYPE', '')
        if not content_type.startswith(self.content_type):
            return
        encoding = request.encoding or settings.DEFAULT_CHARSET
        try:
            body = request.body.decode(encoding=encoding)
        except UnicodeDecodeError:
            return HttpResponseBadRequest('bad unicode')
        try:
            request.POST = self.json_decode(body, encoding=encoding)
        except ValueError:
            return HttpResponseBadRequest('malformed data')

    @staticmethod
    def json_decode(body, encoding=None):
        data = json.loads(body, encoding=encoding)
        query_dict = QueryDict(mutable=True)
        try:
            query_dict.update(data)
        except AttributeError:
            # data is not a mapping (hasn't items() method)
            raise ValueError
        query_dict._mutable = False
        return query_dict
