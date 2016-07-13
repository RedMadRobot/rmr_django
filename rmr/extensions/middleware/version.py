import os


class VersionMiddleware:

    @staticmethod
    def process_response(request, response):
        version = os.environ.get('APP_VERSION')
        if version:
            response['App-Version'] = version
        return response
