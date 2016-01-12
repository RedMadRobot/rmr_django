class DataSet:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return '(args={}, kwargs={})'.format(self.args, self.kwargs)


def data_provider(*data_sets):
    def _decorator(test_method):
        test_method.__data_sets__ = data_sets
        return test_method

    return _decorator


class Parametrized(type):

    def __new__(mcs, name, mro, attrs):
        actual_attrs = {}
        for method_name, method in attrs.items():
            data_sets = getattr(method, '__data_sets__', None)
            if not data_sets:
                actual_attrs[method_name] = method
                continue
            for data_set in data_sets:
                test_name = '{}_{}'.format(method_name, data_set)
                actual_attrs[test_name] = (lambda m, ds: (
                    lambda self: m(self, *ds.args, **ds.kwargs)
                ))(method, data_set)
        return super().__new__(mcs, name, mro, actual_attrs)
