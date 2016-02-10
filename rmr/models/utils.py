from collections import defaultdict


class BulkModelCreator:
    """
    BulkModelCreator accumulates instances of any Django models and saves them into the db (using bulk_create)
    when count of particular model instances reaches 'batch_size' parameter.
    On exit from context manager will create all instances, that left in collection.

    Example:

    with BulkModelCreator(100) as creator:
        for row in csv_reader.read():
            instance = get_instance(row)
            creator.add(instance)

    """

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

    def __exit__(self, exc_type, exc_value, traceback):
        exc_type is None and self.flush_all()
