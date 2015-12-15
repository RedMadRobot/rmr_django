from datetime import timedelta, timezone

# pytz's 'Europe/Moscow' is broken now
MSK = timezone(timedelta(hours=3), "Europe/Moscow")

# pytz haven't CEST timezone now
CEST = timezone(timedelta(hours=2), "CEST")
