from django.utils import timezone


def previous_weekday(date):
    date -= timezone.timedelta(days=1)
    while date.weekday() > 4:  # Mon-Fri are 0-4
        date -= timezone.timedelta(days=1)
    return date
