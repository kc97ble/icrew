from datetime import timedelta
from django.utils import timezone
from events import logics
from events.models import TimeStatus, EventStatus, RegStatus, Reg
from .constants import (
    TIME_STATUS_CLASS,
    STATUS_CLASS,
    DECORATION_REG_STATUS,
    DECORATION_TAG_LEVEL,
)

RECENTLY_CHANGED_INTERVAL = timedelta(days=1)


def decorated_user(user):
    return {
        "username": user.username,
        "displayed_name": user.get_full_name() or user.username,
        **user.__dict__,
    }


def decorated_tag(tag):
    return {**tag.__dict__, **DECORATION_TAG_LEVEL.get(tag.level, {})}


def decorated_event(event, user):
    event_status = event.status()
    rs = logics.reg_status(user, event)
    is_event_open = event_status in [
        EventStatus.OPEN_REG_AND_WAIT,
        EventStatus.OPEN_FCFS,
    ]
    can_register = user.is_authenticated and rs == RegStatus.NONE and is_event_open
    can_unregister = user.is_authenticated and rs == RegStatus.PENDING
    accepted_users = [
        decorated_user(r.user)
        for r in Reg.objects.filter(event=event, status=RegStatus.ACCEPTED).all()
    ]
    reg_count = Reg.objects.filter(event=event).count()
    is_user_accepted = user.is_authenticated and (
        Reg.objects.filter(user=user, event=event, status=RegStatus.ACCEPTED).count()
        > 0
    )
    custom_tags = [decorated_tag(tag) for tag in event.custom_tags.all()]
    is_recently_changed = (
        timezone.now() - event.modified_at
    ) < RECENTLY_CHANGED_INTERVAL

    return {
        "time_status_label": TimeStatus[event.time_status].label,
        "time_status_class": TIME_STATUS_CLASS[event.time_status],
        "status_label": EventStatus[event_status].label,
        "status_class": STATUS_CLASS[event_status],
        "has_registered": rs != RegStatus.NONE,
        "can_register": can_register,
        "can_unregister": can_unregister,
        "accepted_users": accepted_users,
        "reg_count": reg_count,
        "is_user_accepted": is_user_accepted,
        "custom_tags": custom_tags,
        "is_recently_changed": is_recently_changed,
        **event.__dict__,
        **DECORATION_REG_STATUS.get(rs, {}),
    }
