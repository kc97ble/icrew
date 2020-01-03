from django.utils import timezone
from django.contrib.auth.models import User

from .exceptions import LogicError
from .models import Event, Reg, EventStatus, RegStatus


def reg_status(user, event):
    if user.is_anonymous:
        return RegStatus.NONE
    r = Reg.objects.filter(user=user, event=event).first()
    return r.status if r is not None else RegStatus.NONE


def add_reg(user, event):
    if user.is_anonymous:
        raise LogicError("You have to login first.")
    if reg_status(user, event) != RegStatus.NONE:
        raise LogicError("You have registered for this event already.")

    event_status = event.status()
    if event_status == EventStatus.OPEN_REG_AND_WAIT:
        Reg.objects.create(user=user, event=event, status=RegStatus.PENDING.value)
    elif event_status == EventStatus.OPEN_FCFS:
        Reg.objects.create(user=user, event=event, status=RegStatus.ACCEPTED.value)
    else:
        raise LogicError("The registration for this event is not open.")


def remove_reg(user, event):
    rs = reg_status(user, event)
    if rs is None:
        raise LogicError("You have not registered for this event.")
    if rs != RegStatus.PENDING.value:
        raise LogicError(
            "You can only unregister when your registration status is PENDING."
        )
    Reg.objects.filter(user=user, event=event).delete()
