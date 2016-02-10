from unittest import mock

import django.test
from django.db import models

from rmr.models.utils import BulkModelCreator


class SampleModel(models.Model):
    field = models.CharField(max_length=10)


class TestBulkModelCreator(django.test.TestCase):

    @mock.patch.object(SampleModel.objects, 'bulk_create')
    def test_no_bulk_create_on_exception(self, bulk_create):
        try:
            with BulkModelCreator() as creator:
                for i in range(0, 10):
                    creator.add(SampleModel(field='test'))
                # Something goes wrong here:
                raise Exception
        except:
            pass
        self.assertFalse(bulk_create.called, 'bulk_create() was called, while should not!')
