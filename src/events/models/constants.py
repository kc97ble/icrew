from django.db import models

WEEK_OFFSET = -2


class TimeStatus(models.TextChoices):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    CANCELED = "CANCELED"


class RegStatus(models.TextChoices):
    NONE = "NONE", "Unregistered"
    PENDING = "PENDING", "Registration pending"
    ACCEPTED = "ACCEPTED", "Registration accepted"
    REJECTED = "REJECTED", "Registration rejected"


class LockingReason(models.TextChoices):
    NONE = "NONE"
    UNOPENED = "UNOPENED"
    EVENT_CANCELED = "EVENT_CANCELED"
    REG_CLOSED = "REG_CLOSED", "Registration closed"


class EventStatus(models.TextChoices):
    CLOSED_NONE = "CLOSED_NONE", "Closed"
    CLOSED_UNOPENED = "CLOSED_UNOPENED", "Closed - Unopened"
    CLOSED_EVENT_CANCELLED = "CLOSED_EVENT_CANCELLED", "Closed - Event cancelled"
    CLOSED_REG_CLOSED = "CLOSED_REG_CLOSED", "Closed - Registration closed"
    OPEN_REG_AND_WAIT = "OPEN_REG_AND_WAIT", "Open - Register and wait"
    OPEN_FCFS = "OPEN_FCFS", "Open - First come first serve"
    CLOSED_UNFULFILLED = "CLOSED_UNFULFILLED", "Closed - Unfulfilled"
    CLOSED_DEMAND_FULFILLED = "CLOSED_DEMAND_FULFILLED", "Closed - Demand fulfilled"


class MessageLevel(models.TextChoices):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"
