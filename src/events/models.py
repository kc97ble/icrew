from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

WEEK_OFFSET = -2


class TimeStatus(models.TextChoices):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    CANCELED = "CANCELED"


class RegistrationStatus(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class LockingReason(models.TextChoices):
    NONE = "NONE"
    UNOPENED = "UNOPENED"
    EVENT_CANCELED = "EVENT_CANCELED"
    REGISTRATION_CLOSED = "REGISTRATION_CLOSED"


class EventStatus(models.TextChoices):
    CLOSED_NONE = "CLOSED_NONE", "Closed"
    CLOSED_UNOPENED = "CLOSED_UNOPENED", "Closed - Unopened"
    CLOSED_EVENT_CANCELLED = "CLOSED_EVENT_CANCELLED", "Closed - Event cancelled"
    CLOSED_REGISTRATION_CLOSED = (
        "CLOSED_REGISTRATION_CLOSED",
        "Closed - Registration closed",
    )
    OPEN_REGISTER_AND_WAIT = "OPEN_REGISTER_AND_WAIT", "Open - Register and wait"
    OPEN_FIRST_COME_FIRST_SERVE = (
        "OPEN_FIRST_COME_FIRST_SERVE",
        "Open - First come first serve",
    )
    CLOSED_UNFULFILLED = "CLOSED_UNFULFILLED", "Closed - Unfulfilled"
    CLOSED_DEMAND_FULFILLED = "CLOSED_DEMAND_FULFILLED", "Closed - Demand fulfilled"


def CharFieldWithChoice(Choices, default=None):
    return models.CharField(max_length=255, choices=Choices.choices, default=default)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=255, blank=True)
    time_status = CharFieldWithChoice(TimeStatus, default=TimeStatus.ON_TIME)
    locked = models.BooleanField(null=False, default=False)
    locking_reason = CharFieldWithChoice(LockingReason, default=LockingReason.NONE)
    hidden = models.BooleanField(null=False, default=False)
    is_fcfs = models.BooleanField(null=False, default=False, verbose_name="FCFS")
    start_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    demand = models.IntegerField(default=1, help_text="number of members needed")

    def week_no(self):
        return self.start_at.isocalendar()[1] + WEEK_OFFSET

    def day_of_week(self):
        return self.start_at.weekday()

    def is_demand_fulfilled(self):
        num_reg_accepted = Registration.objects.filter(
            event=self, status=RegistrationStatus.ACCEPTED
        ).count()
        return num_reg_accepted >= self.demand

    def status(self):
        if self.locked:
            if self.locking_reason == LockingReason.NONE:
                return EventStatus.CLOSED_NONE
            elif self.locking_reason == LockingReason.UNOPENED:
                return EventStatus.CLOSED_UNOPENED
            elif self.locking_reason == LockingReason.EVENT_CANCELED:
                return EventStatus.CLOSED_EVENT_CANCELLED
            elif self.locking_reason == LockingReason.REGISTRATION_CLOSED:
                return EventStatus.CLOSED_REGISTRATION_CLOSED
            else:
                raise Exception("Unknown locking_reason")
        elif not self.is_fcfs:
            now = timezone.now()
            return EventStatus.OPEN_REGISTER_AND_WAIT
        elif self.is_demand_fulfilled():
            return EventStatus.CLOSED_DEMAND_FULFILLED
        elif timezone.now() >= self.start_at:
            return EventStatus.CLOSED_UNFULFILLED
        else:
            return EventStatus.OPEN_FIRST_COME_FIRST_SERVE


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = CharFieldWithChoice(RegistrationStatus, default=RegistrationStatus.PENDING)
