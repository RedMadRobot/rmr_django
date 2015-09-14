import logging

from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from rmr.errors import ApiError


class Json(View):

    http_code = 200

    error_code_success = ''

    logger = logging.getLogger('backend')

    def dispatch(self, request, *args, **kwargs):
        http_code = self.http_code
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            api_result = dict(
                error_code=self.error_code_success,
                result=result,
            )
        except ApiError as error:

            self.logger.log(
                error.level,
                '%(code)s: %(message)s',
                dict(message=error.message, code=error.code),
            )

            http_code = error.http_code

            api_result = dict(
                error_code=error.code,
                result=None,
            )

        return JsonResponse(api_result, status=http_code)

    @staticmethod
    def get_device_id(request):
        return request.META.get('HTTP_DEVICE_ID')
