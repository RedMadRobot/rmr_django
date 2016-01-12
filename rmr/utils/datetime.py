from datetime import datetime

from django.utils import timezone


def fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())


def strptime(date_string, format, default_tz=timezone.utc):
    dt = datetime.strptime(date_string, format)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone=default_tz)
    return timezone.localtime(dt)
