from django.contrib.postgres import lookups
from django.contrib.postgres.fields.array import ArrayContainedBy, ArrayContains, \
    ArrayField
from django.db import models


class PgLtreeField(models.TextField):
    description = 'Ltree'
    
    def db_type(self, connection):
        return 'ltree'
    
    def get_internal_type(self):
        return "CharField"
    
    def get_prep_value(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            return [self.to_python(val) for val in value]
        return self.to_python(value)


class LtreeLookup(lookups.PostgresSimpleLookup):
    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        if isinstance(self.rhs, list) or isinstance(self.rhs, tuple):
            # Cast to array
            # With any clause GIST index will work
            rhs = 'ANY(%s::%s[])' % (
                rhs,
                self.lhs.output_field.db_type(connection)
            )

        return '%s %s %s' % (lhs, self.operator, rhs), lhs_params + rhs_params


@PgLtreeField.register_lookup
class AncestorOf(LtreeLookup):
    lookup_name = 'ancestor_of'
    operator = '@>'


@PgLtreeField.register_lookup
class DescendantOf(LtreeLookup):
    lookup_name = 'descendant_of'
    operator = '<@'


@PgLtreeField.register_lookup
class Match(LtreeLookup):
    lookup_name = 'match'
    operator = '~'


class LtreeArrayField(ArrayField):
    def __init__(self, **kwargs):
        kwargs['base_field'] = PgLtreeField()
        super().__init__(**kwargs)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if value:
            return '{%s}' % ','.join(value)
        return value
    
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        # value example: '{1.2,1.3,1.4}'
        # remove brackets {}, then split by comma
        # return ['1.2', '1.3', '1.4']
        return [] if value == '{}' else value[1:-1].split(',')


@LtreeArrayField.register_lookup
class ArrayAncestorOf(ArrayContainedBy):
    lookup_name = 'ancestor_of'


@LtreeArrayField.register_lookup
class ArrayDescendantOf(ArrayContains):
    lookup_name = 'descendant_of'


@LtreeArrayField.register_lookup
class ArrayMatch(lookups.PostgresSimpleLookup):
    lookup_name = 'match'
    operator = '~'
    
    def as_sql(self, qn, connection):
        sql, params = super().as_sql(qn, connection)
        sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
        return sql, params
