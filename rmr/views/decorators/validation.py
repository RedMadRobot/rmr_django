import functools

from django import forms, http

import rmr


def validate_request(*, get=forms.Form, post=forms.Form):
    def _decorator(view):
        @functools.wraps(view)
        def _view(request: http.HttpRequest, *args, **kwargs):
            form_get = get(request.GET)
            form_post = post(request.POST)
            if False in (form_get.is_valid(), form_post.is_valid()):
                raise rmr.ClientError(
                    code='validation_error',
                    message=dict(form_post.errors, **form_get.errors),
                )
            data_get = http.QueryDict(mutable=True)
            data_post = http.QueryDict(mutable=True)
            data_get.update(form_get.cleaned_data)
            data_post.update(form_post.cleaned_data)
            data_get._mutable = data_post._mutable = False
            request.GET = data_get
            request.POST = data_post
            return view(request, *args, **kwargs)
        return _view
    return _decorator
