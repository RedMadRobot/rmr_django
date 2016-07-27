import warnings

from django import forms


class OffsetLimit(forms.Form):

    offset = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False, min_value=1)

    @classmethod
    def with_limit_required(cls, *, max_value=None, **kwargs):
        if 'limit_max_value' in kwargs:
            warnings.warn(
                'limit_max_value deprecated and will be removed '
                'in rmr-django 2.0, use max_value instead',
                category=RuntimeWarning, stacklevel=2,
            )
            max_value = kwargs['limit_max_value']
        limit = forms.IntegerField(
            required=True,
            max_value=max_value,
            min_value=1,
        )
        return type('OffsetLimitRequired', (cls, ), dict(limit=limit))
