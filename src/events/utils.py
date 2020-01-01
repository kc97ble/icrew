from django.utils import timezone
from datetime import datetime

from .models import WEEK_OFFSET

CURRENT_YEAR = timezone.now().year

import datetime


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)


def datetime_from_week_no(week_no, day_of_week):
    return iso_to_gregorian(CURRENT_YEAR, week_no - WEEK_OFFSET, day_of_week + 1)

def current_week_no():
    now = timezone.now()
    return max(now.isocalendar()[1] + WEEK_OFFSET, 0)
