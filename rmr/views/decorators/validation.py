import functools

from django import forms
from django.http import HttpRequest

from rmr import ClientError


def validate_request(*, get=forms.Form, post=forms.Form):
    def _decorator(view):
        @functools.wraps(view)
        def _view(request: HttpRequest, *args, **kwargs):
            form_get = get(request.GET)
            form_post = post(request.POST)
            if False in (form_get.is_valid(), form_post.is_valid()):
                raise ClientError(
                    code='validation_error',
                    message=dict(
                        form_post.errors,
                        **form_get.errors
                    ),
                )
            return view(request, *args, **kwargs)
        return _view
    return _decorator
