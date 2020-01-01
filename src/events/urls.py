from django.urls import path, include
from .views import EventHomeView, EventDetailView, EventWeekView

urlpatterns = [
    path("", EventHomeView.as_view(), name="events-home"),
    path("<int:id>/", EventDetailView.as_view(), name="events-detail"),
    path("weeks/<int:week_no>", EventWeekView.as_view(), name="events-week"),
]
