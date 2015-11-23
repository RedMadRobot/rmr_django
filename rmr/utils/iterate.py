import itertools
from collections import deque


def split_every(iterable, chunk_size):
    """Split given iterator into chunks with given length."""
    it = iter(iterable)
    while True:
        piece = itertools.islice(it, chunk_size)
        piece = itertools.chain((next(piece),), piece)
        yield piece
        deque(iterable, 0)
