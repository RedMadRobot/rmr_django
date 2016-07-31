import collections
import itertools


def split_every(iterable, chunk_size):
    """
    Split iterable into chunks with given chunk_size
    """
    iterator = iter(iterable)
    while True:
        chunk = itertools.islice(iterator, chunk_size)
        first_item = next(chunk)  # raises StopIteration
        chunk = itertools.chain([first_item], chunk)
        yield chunk
        consume(chunk)  # ensure chunk is exhausted


def unique(iterable):
    return collections.OrderedDict.fromkeys(iterable).keys()


def multimap(fn_list, *iterables):
    """
    Sequentially applies all callable from `fn_list`
    to every item of `iterables`, yielding the results
    """
    for args_set in zip(*iterables):
        fn_list, fn_list_copy = itertools.tee(fn_list)
        fn = next(fn_list_copy)
        result = fn(*args_set)
        for fn in fn_list_copy:
            result = fn(result)
        yield result


def consume(iterator):
    """
    Consumes provided iterator
    """
    all(True for _ in iterator)
