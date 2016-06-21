from datetime import datetime, timedelta

from django.utils import timezone

NOW = object()


def fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())


def strptime(date_string, format, default_tz=timezone.utc):
    dt = datetime.strptime(date_string, format)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone=default_tz)
    return timezone.localtime(dt)


def get_date_range(
    start_date: int = None,
    end_date: int = NOW,
    max_range: int = None,
):
    """
    Get date range

    :rtype: (datetime, datetime)
    """
    max_range = max_range or None
    if max_range and None in (start_date, end_date):
        raise ValueError(
            'Both start_date and end_date must be not None '
            'when max_range used'
        )

    if end_date is NOW:
        end = timezone.now()
    elif end_date is None:
        end = None
    else:
        end = fromtimestamp(end_date)

    if start_date is None:
        start = max_range and end - timedelta(seconds=max_range)
        return start, end
    else:
        start = fromtimestamp(start_date)

    if max_range and (end - start).seconds > max_range:
        raise ValueError('Date range exceeds max_range')

    return start, end
