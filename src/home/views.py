from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "home/home_view.html", {})


def chat_room_view(request, *args, **kwargs):
    return render(request, "home/chat_room_view.html", {})
