from django.db import models


class Event(models.Model):

    class TimeStatus:
        ON_TIME = 'ON_TIME'
        DELAYED = 'DELAYED'
        CANCELED = 'CANCELED'

    TIME_STATUS_CHOICE = [
        (TimeStatus.ON_TIME, "On time"),
        (TimeStatus.DELAYED, "Delayed"),
        (TimeStatus.CANCELED, "Canceled"),
    ]

    title = models.TextField()
    description = models.TextField()
    venue = models.TextField()
    time_status = models.CharField(
        max_length=255,
        choices=TIME_STATUS_CHOICE
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
