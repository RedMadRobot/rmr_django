import warnings

from django import forms


class MultipleValueField(forms.TypedMultipleChoiceField):

    def valid_value(self, value):
        return True

    def to_python(self, value):
        return value


class MultiValueField(MultipleValueField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "MultiValueField is deprecated and will be removed "
            "in rmr-django 2.0use MultipleValueField instead",
            DeprecationWarning,
        )
        super(MultipleValueField, self).__init__(*args, **kwargs)


class BooleanField(forms.Field):

    empty_values = {None}

    def to_python(self, value):
        if value in (True, False):
            return value
        return None
