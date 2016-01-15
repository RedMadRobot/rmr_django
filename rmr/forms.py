from django import forms


class MultiValueField(forms.TypedMultipleChoiceField):

    def valid_value(self, value):
        return True


class BooleanField(forms.Field):

    empty_values = {None}

    def to_python(self, value):
        if value in (True, False):
            return value
        return None
