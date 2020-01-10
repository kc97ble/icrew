from django.urls import path
from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required
from .views import ConsistencyTestView


def home_view(request):
    return render(request, "staff/home.html", {})


urlpatterns = [
    path("", home_view, name="staff-home"),
    path(
        "consistency-test",
        staff_member_required(ConsistencyTestView.as_view()),
        name="staff-consistency_test",
    ),
]
