"""
Range fields placed here are actual only for Django <= 1.8

Django 1.9 already has 'upper' and 'lower' lookups for the range fields
"""

from django.contrib.postgres import fields
from django.db import models


class DateRangeField(fields.DateRangeField):
    pass


class DateTimeRangeField(fields.DateTimeRangeField):
    pass


class FloatRangeField(fields.FloatRangeField):
    pass


class BigIntegerRangeField(fields.BigIntegerRangeField):
    pass


class IntegerRangeField(fields.IntegerRangeField):
    pass


class Lower(models.Transform):
    lookup_name = 'lower'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return 'lower({lhs})'.format(lhs=lhs), params


class Upper(models.Transform):
    lookup_name = 'upper'

    def as_sql(self, compiler, connection):
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
