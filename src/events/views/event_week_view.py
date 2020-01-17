from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import View

import calendar

from events import logics, utils
from events.exceptions import LogicError
from events.models import Event
from .utils import decorated_event


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
