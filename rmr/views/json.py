import logging

from django.http import JsonResponse, HttpResponse
from django.views.generic import View

import rmr


class Json(View):

    http_code = 200

    logger = logging.getLogger('backend')

    def dispatch(self, request, *args, **kwargs):
        http_code = self.http_code
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            api_result = dict(
                data=result,
            )
        except rmr.Error as error:

            self.logger.log(
                error.level,
                '%(code)s: %(message)s',
                dict(message=error.message, code=error.code),
            )

            http_code = error.http_code

            api_result = dict(
                error=dict(
                    code=error.code,
                    description=error.message,
                ),
            )

        return JsonResponse(api_result, status=http_code)

    @staticmethod
    def get_device_id(request):
        return request.META.get('HTTP_DEVICE_ID')
