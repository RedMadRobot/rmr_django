from datetime import datetime

from django.utils import timezone


def fromtimestamp(timestamp):
    datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())
