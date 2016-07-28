import warnings

from django import test, http

from rmr.utils.patch import patch


class DataSet:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        warnings.warn(
            'DataSet is deprecated and will be removed in rmr-django 2.0, '
            'use unittest.TestCase.subTest instead',
            DeprecationWarning,
        )

    def __str__(self):
        return '(args={}, kwargs={})'.format(self.args, self.kwargs)


def data_provider(*data_sets):
    warnings.warn(
        'data_provider is deprecated and will be removed in rmr-django 2.0, '
        'use unittest.TestCase.subTest instead',
        DeprecationWarning,
    )

    def _decorator(test_method):
        test_method.__data_sets__ = data_sets
        return test_method

    return _decorator


class Parametrized(type):

    def __new__(mcs, name, mro, attrs):
        warnings.warn(
            'Parametrized metaclass is deprecated and will be removed '
            'in rmr-django 2.0, use unittest.TestCase.subTest instead',
            category=RuntimeWarning, stacklevel=2,
        )

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


class Client(test.Client):

    def request(self, **request):
        with patch(http.HttpResponse, 'wsgi_request', _dummy_setter):
            with patch(http.HttpResponse, 'request', _dummy_setter):
                return super().request(**request)

_dummy_setter = property(fset=lambda *_: None)
