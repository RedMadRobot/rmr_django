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


class OffsetLimit(forms.Form):

    offset = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False)

    @classmethod
    def with_limit_required(cls, *, limit_max_value):
        limit = forms.IntegerField(
            required=True,
            max_value=limit_max_value,
        )
        return type('OffsetLimitRequired', (cls, ), dict(limit=limit))
