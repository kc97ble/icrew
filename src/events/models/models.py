from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import localtime

from .constants import (
    LockingReason,
    TimeStatus,
    MessageLevel,
    WEEK_OFFSET,
    RegStatus,
    EventStatus,
)


def CharFieldWithChoice(Choices, default=None):
    return models.CharField(max_length=255, choices=Choices.choices, default=default)


class Tag(models.Model):
    label = models.CharField(max_length=255)
    level = CharFieldWithChoice(MessageLevel, default=MessageLevel.INFO)

    def __str__(self):
        return "[{}] {}".format(self.level, self.label)


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
    custom_tags = models.ManyToManyField(Tag)
    is_inconsistent = models.BooleanField(null=False, default=False)

    def __str__(self):
        return "E{} - {}".format(self.id, self.title)

    def week_no(self):
        return localtime(self.start_at).isocalendar()[1] + WEEK_OFFSET

    def day_of_week(self):
        return localtime(self.start_at).weekday()

    def is_demand_fulfilled(self):
        num_reg_accepted = Reg.objects.filter(
            event=self, status=RegStatus.ACCEPTED
        ).count()
        return num_reg_accepted >= self.demand

    def get_week_config(self):
        return WeekConfig.objects.filter(week_no=self.week_no()).first()

    def status(self):
        if self.locked:
            if self.locking_reason == LockingReason.NONE:
                return EventStatus.CLOSED_NONE.value
            if self.locking_reason == LockingReason.UNOPENED:
                return EventStatus.CLOSED_UNOPENED.value
            if self.locking_reason == LockingReason.EVENT_CANCELED:
                return EventStatus.CLOSED_EVENT_CANCELLED.value
            if self.locking_reason == LockingReason.REG_CLOSED:
                return EventStatus.CLOSED_REG_CLOSED.value
            raise Exception("Unknown locking_reason")

        now = timezone.now()
        wc = self.get_week_config()
        if wc and wc.reg_start_at and now < wc.reg_start_at:
            return EventStatus.CLOSED_UNOPENED.value

        if not self.is_fcfs:
            if wc and wc.reg_ended_at and now > wc.reg_ended_at:
                return EventStatus.CLOSED_REG_CLOSED.value
            else:
                return EventStatus.OPEN_REG_AND_WAIT.value

        if self.is_demand_fulfilled():
            return EventStatus.CLOSED_DEMAND_FULFILLED.value
        if now >= self.start_at:
            return EventStatus.CLOSED_UNFULFILLED.value
        return EventStatus.OPEN_FCFS.value


class Reg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = CharFieldWithChoice(RegStatus, default=RegStatus.PENDING)

    def __str__(self):
        return "{} - {} - {}".format(self.event.title, self.user.username, self.status)


class WeekConfig(models.Model):
    week_no = models.IntegerField(primary_key=True)
    reg_start_at = models.DateTimeField(null=True, blank=True)
    reg_ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.week_no, self.reg_start_at, self.reg_ended_at)


class Announcement(models.Model):
    text = models.TextField()
    hidden = models.BooleanField(default=False)
