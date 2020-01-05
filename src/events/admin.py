from django.contrib import admin

from .models import Event, Reg, WeekConfig

class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "week_no",
        "date",
        "start_time",
        "ended_time",
        "venue",
        "demand",
        "status",
        "locked",
        "locking_reason",
        "hidden",
        "is_fcfs",
    ]
    list_editable = ["locked", "hidden", "is_fcfs", "locking_reason"]
    list_filter = ["demand", "locked", "hidden", "is_fcfs", "locking_reason"]

    def date(self, event):
        return event.start_at.date()

    def start_time(self, event):
        return event.start_at.time()

    def ended_time(self, event):
        return event.ended_at.time()

    date.admin_order_field = "start_at"


class RegAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "status"]
    list_editable = ["status"]


class WeekConfigAdmin(admin.ModelAdmin):
    list_display = ["week_no", "reg_start_at", "reg_ended_at"]
    list_editable = ["reg_start_at", "reg_ended_at"]

admin.site.register(Event, EventAdmin)
admin.site.register(Reg, RegAdmin)
admin.site.register(WeekConfig, WeekConfigAdmin)
