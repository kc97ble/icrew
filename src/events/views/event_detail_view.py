from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import View

import calendar

from events import logics, utils
from events.exceptions import LogicError
from events.models import Event
from .utils import decorated_event


class EventDetailView(View):
    template_name = "events/event_detail_view.html"

    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
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
