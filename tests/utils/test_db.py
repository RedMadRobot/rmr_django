import contextlib

import django.test
import mock

from django.db import models

from rmr.utils.db import BulkModelCreator


class SampleModel(models.Model):

    class Meta:
        app_label = 'tests'


class TestBulkModelCreator(django.test.SimpleTestCase):

    @mock.patch.object(SampleModel.objects, 'bulk_create')
    def test_bulk_create_called_once(self, bulk_create):
        with contextlib.suppress(Exception):
            with BulkModelCreator(10) as creator:
                creator.append(SampleModel())
        bulk_create.assert_called_once()

    @mock.patch.object(SampleModel.objects, 'bulk_create')
    def test_bulk_create_not_called_on_exception(self, bulk_create):
        with contextlib.suppress(Exception):
            with BulkModelCreator(10) as creator:
                creator.append(SampleModel())
                # Something goes wrong here:
                raise Exception
        bulk_create.assert_not_called()
