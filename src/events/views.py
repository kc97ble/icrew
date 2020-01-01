from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

import calendar

from . import logics, utils
from .exceptions import LogicError
from .models import Event


class EventHomeView(View):
    def get(request, *args, **kwargs):
        return redirect(
            reverse("events-week", kwargs={"week_no": utils.current_week_no()})
        )


class EventDetailView(View):
    template_name = "events/event_detail_view.html"

    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        return render(
            request,
            self.template_name,
            {"event": event, "debug": [id, args, kwargs, event,]},
        )

    def post(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        try:
            logics.add_registration(request.user, event)
        except LogicError as e:
            return HttpResponseBadRequest(str(e))
        return HttpResponse("Registration succeeded.")


class EventWeekView(View):
    template_name = "events/event_week_view.html"

    def get(self, request, week_no, *args, **kwargs):
        events = [e for e in Event.objects.all() if e.week_no() == week_no]
        days = [
            {
                "day_name": calendar.day_name[day_of_week],
                "date": utils.datetime_from_week_no(week_no, day_of_week),
                "events": [e for e in events if e.day_of_week() == day_of_week],
            }
            for day_of_week in range(7)
        ]
        data = {
            "days": days,
        }
        return render(request, self.template_name, data)
