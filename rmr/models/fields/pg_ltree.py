from django.contrib.postgres import lookups
from django.db import models


class PgLtreeField(models.TextField):

    description = 'Ltree'

    def db_type(self, connection):
        return 'ltree'

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        return super(models.TextField, self).formfield()


@PgLtreeField.register_lookup
class AncestorOf(lookups.PostgresSimpleLookup):
    lookup_name = 'ancestor_of'
    operator = '@>'


@PgLtreeField.register_lookup
class DescendantOf(lookups.PostgresSimpleLookup):
    lookup_name = 'descendant_of'
    operator = '<@'


@PgLtreeField.register_lookup
class Match(lookups.PostgresSimpleLookup):
    lookup_name = 'match'
    operator = '~'
