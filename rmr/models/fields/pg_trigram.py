from django.contrib.postgres import lookups
from django.db import models


class PgTrigramCharField(models.CharField):
    pass


class PgTrigramTextField(models.TextField):
    pass


@PgTrigramCharField.register_lookup
@PgTrigramTextField.register_lookup
class SimilarTo(lookups.PostgresSimpleLookup):
    lookup_name = 'similar'
    operator = '%%'  # escaped '%'
