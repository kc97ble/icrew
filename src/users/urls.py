from django.urls import path, include
from .views import signup_view, change_password

urlpatterns = [
    path("signup/", signup_view),
    path("change_password/", change_password, name="change_password"),
]
