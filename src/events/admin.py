from django.contrib import admin

# Register your models here.

from .models import Event, Registration

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'week_no', 'start_at', 'locked', 'hidden', 'is_fcfs', 'status']
    list_editable = ['locked', 'hidden', 'is_fcfs']
    list_filter = ['locked', 'hidden', 'is_fcfs']

    # def registration_status(self, event):
    #     q = Registration.objects.filter(event=event)
    #     return "{} registered".format(q.count())

admin.site.register(Event, EventAdmin)
admin.site.register(Registration)
