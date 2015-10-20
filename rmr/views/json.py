import logging

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.generic import View

import rmr


class Json(View):

    http_code = 200

    logger = logging.getLogger('rmr')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        http_code = self.http_code
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            api_result = dict(
                data=result,
            )

            self.logger.debug(
                'request_headers: %(request_headers)s, '
                'request_params: %(request_params)s, '
                'request_data: %(request_data)s, '
                'response_data: %(response_data)s, ',
                request_headers=request.META,
                request_params=request.GET,
                request_data=request.POST,
                response_data=result,
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
