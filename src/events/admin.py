from django.contrib import admin

# Register your models here.

from .models import Event, Reg, WeekConfig


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "week_no",
        "start_at",
        "locked",
        "hidden",
        "is_fcfs",
        "status",
    ]
    list_editable = ["locked", "hidden", "is_fcfs"]
    list_filter = ["locked", "hidden", "is_fcfs"]


class RegAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "status"]
    list_editable = ["status"]


class WeekConfigAdmin(admin.ModelAdmin):
    list_display = ["week_no", "reg_start_at", "reg_ended_at"]
    list_editable = ["reg_start_at", "reg_ended_at"]

admin.site.register(Event, EventAdmin)
admin.site.register(Reg, RegAdmin)
admin.site.register(WeekConfig, WeekConfigAdmin)
