from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

import calendar

from events import logics, utils
from events.exceptions import LogicError
from events.models import Event, TimeStatus, EventStatus, RegStatus, Reg
from .constants import *

def decorated_user(user):
    return {
        "username": user.username,
        "displayed_name": user.get_full_name() or user.username,
        **user.__dict__,
    }


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
        **event.__dict__,
        **DECORATION_REG_STATUS[rs],
    }

class EventHomeView(View):
    def get(request, *args, **kwargs):
        return redirect(
            reverse("events-week", kwargs={"week_no": utils.current_week_no()})
        )


class EventDetailView(View):
    template_name = "events/event_detail_view.html"

    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        rs = logics.reg_status(request.user, event)
        return render(
            request,
            self.template_name,
            {"event": decorated_event(event, request.user)},
        )

    def post(self, request, id, *args, **kwargs):
        action = request.POST["action"]
        event = get_object_or_404(Event, id=id)
        try:
            if "register" == action:
                logics.add_reg(request.user, event)
                return HttpResponse("Registration added.")
            elif "unregister" == action:
                logics.remove_reg(request.user, event)
                return HttpResponse("Registration removed.")
            else:
                raise LogicError("Invalid action.")
        except LogicError as e:
            return HttpResponseBadRequest(str(e))


class EventWeekView(View):
    template_name = "events/event_week_view.html"

    def get(self, request, week_no, *args, **kwargs):
        events = [e for e in Event.objects.all() if e.week_no() == week_no]
        days = [
            {
                "day_name": calendar.day_name[dow],
                "date": utils.datetime_from_week_no(week_no, dow),
                "events": [
                    decorated_event(e, request.user)
                    for e in sorted(events, key=lambda e: e.start_at)
                    if e.day_of_week() == dow and not e.hidden
                ],
            }
            for dow in range(7)
        ]
        data = {
            "days": days,
            "active_week_no": week_no,
            "week_no_list": [0, 1, 2, 3, 4, 5],
        }
        return render(request, self.template_name, data)
