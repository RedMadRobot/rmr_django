from collections import defaultdict


class BulkModelCreator:

    def __init__(self, batch_size=300):
        self.batches = defaultdict(list)
        self.batch_size = batch_size

    def add(self, instance):
        self.batches[instance.__class__].append(instance)
        if len(self.batches[instance.__class__]) == self.batch_size:
            self.flush(instance.__class__)
            return True

    def flush(self, model_class):
        model_class.objects.bulk_create(
            self.batches[model_class],
            self.batch_size
        )
        self.batches[model_class] = []

    def flush_all(self):
        for key in self.batches:
            self.flush(key)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.flush_all()
