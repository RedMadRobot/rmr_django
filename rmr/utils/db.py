import warnings

from collections import defaultdict


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return (
        dict(zip(columns, row))
        for row in cursor.fetchall()
    )


class BulkModelCreator:
    """
    BulkModelCreator context manager accumulates instances of any Django model
    and flushes them to the DB (using bulk_create) when count
    of particular model instances reaches 'batch_size' parameter.
    All remaining items will be proceeded after exiting context.
    """

    def __init__(self, batch_size=300):
        self.batches = defaultdict(list)
        self.batch_size = batch_size

    def add(self, instance):
        warnings.warn(
            'BulkModelCreator.add is deprecated and will be removed '
            'in rmr-django 2.0, use BulkModelCreator.append instead',
            DeprecationWarning,
        )
        flushed = False
        self.batches[instance.__class__].append(instance)
        if len(self.batches[instance.__class__]) == self.batch_size:
            self.flush(instance.__class__)
            flushed = True
        return flushed

    def append(self, instance):
        self.batches[instance.__class__].append(instance)
        if len(self.batches[instance.__class__]) == self.batch_size:
            self.flush(instance.__class__)

    def flush(self, model_class):
        model_class.objects.bulk_create(
            self.batches[model_class],
            self.batch_size,
        )
        self.batches[model_class].clear()

    def flush_all(self):
        for key in self.batches:
            self.flush(key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.flush_all()
