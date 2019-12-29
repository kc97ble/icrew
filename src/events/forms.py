from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'time_status',
            'event_start_at',
            'event_ended_at',
            'register_start_at',
            'result_release_at',
            'register_ended_at',
        ]
