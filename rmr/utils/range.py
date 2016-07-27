def get_range(offset=None, limit=None, limit_default=None):
    """
    Converts offset/limit params to slice object

    For example, following two expressions are identical:
        some_list[get_range(offset=10, limit=5)]
        some_list[10:15]
    """
    start = offset or 0
    limit = limit or limit_default
    stop = limit and start + limit
    return slice(start, stop)
