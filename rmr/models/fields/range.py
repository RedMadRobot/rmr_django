import warnings

from django.contrib.postgres import fields
from django.db import models


class DateRangeField(fields.DateRangeField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            'DateRangeField is deprecated and will be removed in '
            'rmr-django 2.0, use '
            'django.contrib.postgres.fields.DateRangeField instead',
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)


class DateTimeRangeField(fields.DateTimeRangeField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            'DateTimeRangeField is deprecated and will be removed in '
            'rmr-django 2.0, use '
            'django.contrib.postgres.fields.DateTimeRangeField instead',
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)


class FloatRangeField(fields.FloatRangeField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            'FloatRangeField is deprecated and will be removed in '
            'rmr-django 2.0, use '
            'django.contrib.postgres.fields.FloatRangeField instead',
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)


class BigIntegerRangeField(fields.BigIntegerRangeField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            'BigIntegerRangeField is deprecated and will be removed in '
            'rmr-django 2.0, use '
            'django.contrib.postgres.fields.BigIntegerRangeField instead',
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)


class IntegerRangeField(fields.IntegerRangeField):

    def __init__(self, *args, **kwargs):
        warnings.warn(
            'IntegerRangeField is deprecated and will be removed in '
            'rmr-django 2.0, use '
            'django.contrib.postgres.fields.IntegerRangeField instead',
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)


class Lower(models.Transform):
    lookup_name = 'lower'

    def as_sql(self, compiler, connection, *args, **kwargs):
        lhs, params = compiler.compile(self.lhs)
        return 'lower({lhs})'.format(lhs=lhs), params


class Upper(models.Transform):
    lookup_name = 'upper'

    def as_sql(self, compiler, connection, *args, **kwargs):
        lhs, params = compiler.compile(self.lhs)
        return 'upper({lhs})'.format(lhs=lhs), params


@DateRangeField.register_lookup
class DateRangeLowerTransform(Lower):
    output_field = models.DateField()


@DateRangeField.register_lookup
class DateRangeUpperTransform(Upper):
    output_field = models.DateField()


@DateTimeRangeField.register_lookup
class DateRangeLowerTransform(Lower):
    output_field = models.DateTimeField()


@DateTimeRangeField.register_lookup
class DateRangeUpperTransform(Upper):
    output_field = models.DateTimeField()


@FloatRangeField.register_lookup
class DateRangeLowerTransform(Lower):
    output_field = models.FloatField()


@FloatRangeField.register_lookup
class DateRangeUpperTransform(Upper):
    output_field = models.FloatField()


@BigIntegerRangeField.register_lookup
class DateRangeLowerTransform(Lower):
    output_field = models.BigIntegerField()


@BigIntegerRangeField.register_lookup
class DateRangeUpperTransform(Upper):
    output_field = models.BigIntegerField()


@IntegerRangeField.register_lookup
class DateRangeLowerTransform(Lower):
    output_field = models.IntegerField()


@IntegerRangeField.register_lookup
class DateRangeUpperTransform(Upper):
    output_field = models.IntegerField()
