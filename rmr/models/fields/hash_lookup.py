from django.db import models

from rmr.utils.hash import crc64


class HashLookup(models.BigIntegerField):

    def __init__(self, *args, object_field, **kwargs):
        self.object_field = object_field
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['object_field'] = self.object_field
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        obj = getattr(model_instance, self.object_field)
        return None if obj is None else crc64(obj)

    def get_prep_lookup(self, lookup_type, value):
        return crc64(value)
