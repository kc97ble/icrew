from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from events import utils

class EventHomeView(View):
    def get(request, *args, **kwargs):
        return redirect(
            reverse("events-week", kwargs={"week_no": utils.current_week_no()})
        )
