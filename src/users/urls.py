from django.urls import path, include
from .views import users_view, signup_view

urlpatterns = [
    path('', users_view),
    path('signup/', signup_view),
]
