import collections
import itertools


def split_every(iterable, chunk_size):
    """Split given iterator into chunks with given length."""
    iterator = iter(iterable)
    while True:
        chunk = itertools.islice(iterator, chunk_size)
        first_item = next(chunk)  # raises StopIteration when `iterator` is empty
        chunk = itertools.chain((first_item,), chunk)
        yield chunk
        collections.deque(chunk, 0)  # Exhaust unused `chunk`


def unique(iterable):
    return collections.OrderedDict.fromkeys(iterable).keys()


def multimap(fn_list, *iterables):
    """Sequentially applies all callable from `fn_list`
    to every item of `iterables`, yielding the results
    """
    for args in zip(*iterables):
        fn_list, fns = itertools.tee(fn_list)
        fn = next(fns)
        result = fn(*args)
        for fn in fns:
            result = fn(result)
        yield result
