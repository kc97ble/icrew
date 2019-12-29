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

    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    time_status = models.CharField(
        max_length=255,
        choices=TIME_STATUS_CHOICE
    )
    event_start_at = models.DateTimeField()
    event_ended_at = models.DateTimeField()
    register_start_at = models.DateTimeField()
    result_release_at = models.DateTimeField()
    register_ended_at = models.DateTimeField()
