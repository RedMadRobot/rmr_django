from django.db import models
from django.db.models import Lookup


class PgLtreeField(models.CharField):
    description = 'ltree (up to %(max_length)s)'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'ltree'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs


@PgLtreeField.register_lookup
class AncestorOf(Lookup):
    lookup_name = 'ancestor_of'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s @> %s' % (lhs, rhs), params


@PgLtreeField.register_lookup
class DescendantOf(Lookup):
    lookup_name = 'descendant_of'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <@ %s' % (lhs, rhs), params


@PgLtreeField.register_lookup
class Match(Lookup):
    lookup_name = 'match'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s ~ %s' % (lhs, rhs), params
