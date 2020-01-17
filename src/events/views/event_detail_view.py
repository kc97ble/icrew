from django.shortcuts import render, get_object_or_404
from django.views import View
from events import logics
from events.exceptions import LogicError
from events.models import Event
from .utils import decorated_event


class EventDetailView(View):
    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        return render(
            request,
            "events/event_detail/get.html",
            {"event": decorated_event(event, request.user)},
        )

    def post(self, request, id, *args, **kwargs):
        action = request.POST["action"]
        event = get_object_or_404(Event, id=id)
        try:
            if "register" == action:
                logics.add_reg(request.user, event)
                response = {
                    "message": "Registration added",
                    "card_header": {
                        "class": "bg-success text-white font-weight-bold",
                        "icon": "fa fa-check",
                    },
                    "button": {"class": "btn-success"},
                }
                return render(
                    request,
                    "events/event_detail/post.html",
                    {"event": event.__dict__, "response": response},
                )
            elif "unregister" == action:
                logics.remove_reg(request.user, event)
                response = {
                    "message": "Registration removed",
                    "card_header": {
                        "class": "bg-info text-white font-weight-bold",
                        "icon": "fa fa-check",
                    },
                    "button": {"class": "btn-secondary"},
                }
                return render(
                    request,
                    "events/event_detail/post.html",
                    {"event": event.__dict__, "response": response},
                )
            else:
                raise LogicError("Invalid action.")
        except LogicError as e:
            response = {
                "message": str(e),
                "card_header": {
                    "class": "bg-danger text-white font-weight-bold",
                    "icon": "fa fa-times",
                },
                "button": {"class": "btn-secondary"},
            }
            return render(
                request,
                "events/event_detail/post.html",
                {"event": event.__dict__, "response": response},
            )
