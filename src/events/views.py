from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .forms import EventForm


def event_list_view(request, *args, **kwargs):
    return render(
        request,
        'events/event_list_view.html',
        {'debug': Event.objects.all()}
    )


def event_detail_view(request, id, *args, **kwargs):
    return render(
        request,
        'events/event_detail_view.html',
        {'debug': [id, args, kwargs, Event.objects.get(id=id)]}
    )


def event_create_view(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EventForm()

    return render(
        request,
        'events/event_create_view.html',
        {'form': form}
    )
