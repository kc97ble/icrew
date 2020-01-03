from django.contrib import admin

# Register your models here.

from .models import Event, Reg

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'week_no', 'start_at', 'locked', 'hidden', 'is_fcfs', 'status']
    list_editable = ['locked', 'hidden', 'is_fcfs']
    list_filter = ['locked', 'hidden', 'is_fcfs']

    # def reg_status(self, event):
    #     q = Reg.objects.filter(event=event)
    #     return "{} registered".format(q.count())

admin.site.register(Event, EventAdmin)
admin.site.register(Reg)
