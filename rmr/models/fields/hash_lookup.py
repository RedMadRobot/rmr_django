import crcmod

from django.db import models

make_crc = crcmod.predefined.mkPredefinedCrcFun('crc-64')


class HashLookup(models.BigIntegerField):

    def __init__(self, *args, object_field, **kwargs):
        self.object_field = object_field
        super().__init__(*args, **kwargs)

    def make_hash(self, obj):
        crc = make_crc(bytes(obj, encoding='utf-8'))
        if crc > self.MAX_BIGINT:
            crc = -(crc >> 1)
        return crc

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['object_field'] = self.object_field
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        obj = getattr(model_instance, self.object_field)
        return None if obj is None else self.make_hash(obj)

    def get_prep_lookup(self, lookup_type, value):
        return self.make_hash(value)
