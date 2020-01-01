from django.contrib import admin

# Register your models here.

from .models import Event, Registration

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'week', 'week_no', 'start_at', 'readonly', 'hidden', 'is_fcfs', 'registration_status']
    list_editable = ['readonly', 'hidden', 'is_fcfs']
    list_filter = ['week', 'readonly', 'hidden', 'is_fcfs']

    def registration_status(self, event):
        q = Registration.objects.filter(event=event)
        return "{} registered".format(q.count())

admin.site.register(Event, EventAdmin)
admin.site.register(Registration)
