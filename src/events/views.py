from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View

from . import logics
from .exceptions import LogicError
from .models import Event


def event_list_view(request, *args, **kwargs):
    return render(
        request,
        'events/event_list_view.html',
        {'debug': Event.objects.all()}
    )


class EventDetailView(View):
    template_name = 'events/event_detail_view.html'

    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        return render(
            request,
            self.template_name, {
                'event': event,
                'debug': [id, args, kwargs, event, ]
            }
        )

    def post(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        try:
            logics.add_registration(request.user, event)
        except LogicError as e:
            return HttpResponseBadRequest(str(e))
        return HttpResponse("Registration succeeded.")
