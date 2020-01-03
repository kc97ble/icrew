from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

import calendar

from . import logics, utils
from .exceptions import LogicError
from .models import Event, TimeStatus, EventStatus, RegStatus

TIME_STATUS_CLASS = {
    TimeStatus.ON_TIME.value: "badge badge-light",
    TimeStatus.DELAYED.value: "badge badge-warning",
    TimeStatus.CANCELED.value: "badge badge-danger",
}

STATUS_CLASS = {
    EventStatus.CLOSED_NONE.value: "badge badge-secondary",
    EventStatus.CLOSED_UNOPENED.value: "badge badge-secondary",
    EventStatus.CLOSED_EVENT_CANCELLED.value: "badge badge-danger",
    EventStatus.CLOSED_REG_CLOSED.value: "badge badge-secondary",
    EventStatus.OPEN_REG_AND_WAIT.value: "badge badge-info",
    EventStatus.OPEN_FCFS.value: "badge badge-warning",
    EventStatus.CLOSED_UNFULFILLED.value: "badge badge-secondary",
    EventStatus.CLOSED_DEMAND_FULFILLED.value: "badge badge-secondary",
}

REG_STATUS_CLASS = {
    RegStatus.NONE.value: "badge badge-light",
    RegStatus.PENDING.value: "badge badge-info",
    RegStatus.ACCEPTED.value: "badge badge-success",
    RegStatus.REJECTED.value: "badge badge-danger",
}


def decorated_event(event, user):
    es = event.status()
    rs = logics.reg_status(user, event)
    return {
        "time_status_label": TimeStatus[event.time_status].label,
        "time_status_class": TIME_STATUS_CLASS[event.time_status],
        "status_label": EventStatus[es].label,
        "status_class": STATUS_CLASS[es],
        "reg_status_label": RegStatus[rs].label,
        "reg_status_class": REG_STATUS_CLASS[rs],
        "has_registered": rs != RegStatus.NONE,
        **event.__dict__,
    }


def decorated_reg(rs, event):  # deprecated
    is_event_open = event.status() in [
        EventStatus.OPEN_REG_AND_WAIT,
        EventStatus.OPEN_FCFS,
    ]
    return {
        "reg_status_label": RegStatus[rs].label,
        "reg_status_class": REG_STATUS_CLASS[rs],
        "has_registered": rs != RegStatus.NONE,
        "can_register": rs == RegStatus.NONE and is_event_open,
        "can_unregister": rs == RegStatus.PENDING,
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
            {
                "event": decorated_event(event, request.user),
                "reg": decorated_reg(rs, event),
            },
        )

    def post(self, request, id, *args, **kwargs):
        action = request.POST["action"]
        event = get_object_or_404(Event, id=id)
        print(action, event, request.user)
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
                    for e in events
                    if e.day_of_week() == dow
                ],
            }
            for dow in range(7)
        ]
        data = {
            "days": days,
        }
        return render(request, self.template_name, data)
