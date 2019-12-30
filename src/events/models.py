from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    class EventTimeStatus(models.TextChoices):
        ON_TIME = 'ON_TIME', "On time"
        DELAYED = 'DELAYED', "Delayed"
        CANCELED = 'CANCELED', "Canceled"

    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    time_status = models.CharField(
        max_length=255,
        choices=EventTimeStatus.choices,
        default=EventTimeStatus.ON_TIME,
    )
    event_start_at = models.DateTimeField()
    event_ended_at = models.DateTimeField()
    register_start_at = models.DateTimeField()
    result_release_at = models.DateTimeField()
    register_ended_at = models.DateTimeField()


class Registration(models.Model):

    class RegistrationStatus(models.TextChoices):
        PENDING = 'PENDING', "Pending"
        ACCEPTED = 'ACCEPTED', "Accepted"
        REJECTED = 'REJECTED', "Rejected"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
    )
