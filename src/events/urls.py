from django.urls import path, include
from .views import event_list_view, EventDetailView, EventWeekView

urlpatterns = [
    path('', event_list_view),
    path('<int:id>/', EventDetailView.as_view()),
    path('weeks/<int:week_no>', EventWeekView.as_view())
]
