import warnings

from datetime import datetime, timedelta

import pytz

from django.utils import timezone, lru_cache

NOW = object()


def fromtimestamp(timestamp):
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())


def strptime(date_string, format, default_tz=timezone.utc):
    dt = datetime.strptime(date_string, format)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone=default_tz)
    return timezone.localtime(dt)


@lru_cache.lru_cache(maxsize=None)
def get_timezones_with_hour(hour):
    """
    Returns list of timezones where current hour equals to provided value
    """

    now = timezone.now()

    return [
        tz for tz
        in pytz.common_timezones_set
        if timezone.localtime(now, pytz.timezone(tz)).hour == hour
    ]


def get_date_range(
    start_date: int = None,
    end_date: int = NOW,
    max_range: int = None,
):
    """
    Get date range

    :rtype: (datetime, datetime)
    """
    warnings.warn(
        'get_date_range is deprecated and will be removed in rmr-django 2.0, '
        'use rmr.forms.StartStopTime to validate request params',
        category=DeprecationWarning,
    )
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
