from django.db import models
from django.contrib.auth.models import User


class TimeStatus(models.TextChoices):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    CANCELED = "CANCELED"


class RegistrationStatus(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class WeekChoices(models.TextChoices):
    NONE = "NONE"
    WEEK_0 = "WEEK_0"
    WEEK_1 = "WEEK_1"
    WEEK_2 = "WEEK_2"
    WEEK_3 = "WEEK_3"
    WEEK_4 = "WEEK_4"
    WEEK_5 = "WEEK_5"


def CharFieldWithChoice(Choices, default=None):
    return models.CharField(max_length=255, choices=Choices.choices, default=default)


class Event(models.Model):
    week = CharFieldWithChoice(WeekChoices, default=WeekChoices.NONE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=255, blank=True)
    time_status = CharFieldWithChoice(TimeStatus, default=TimeStatus.ON_TIME)
    readonly = models.BooleanField(null=False, default=False)
    hidden = models.BooleanField(null=False, default=False)
    is_fcfs = models.BooleanField(null=False, default=False, verbose_name="FCFS")
    start_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    manpower = models.IntegerField(default=1)


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = CharFieldWithChoice(RegistrationStatus, default=RegistrationStatus.PENDING)
