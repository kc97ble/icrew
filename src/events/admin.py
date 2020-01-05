from django.contrib import admin
from django.conf import settings
from django.utils.timezone import localtime

from .models import Event, Reg, WeekConfig, WEEK_OFFSET

class WeekNoFilter(admin.SimpleListFilter):
    title = 'week number'
    parameter_name = 'week_no'

    def lookups(self, request, model_admin):
        return (
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        value = int(self.value())
        return queryset.filter(start_at__week=value-WEEK_OFFSET)

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
    list_filter = [WeekNoFilter, "demand", "locked", "hidden", "is_fcfs", "locking_reason"]

    def week_no(self, event):
        return event.week_no()
    week_no.short_description = "Wk"

    def date(self, event):
        return localtime(event.start_at).date()
    date.admin_order_field = "start_at"

    def start_time(self, event):
        return localtime(event.start_at).time()
    start_time.short_description = "Start"

    def ended_time(self, event):
        return localtime(event.ended_at).time()
    ended_time.short_description = "End"


class RegAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "status"]
    list_editable = ["status"]


class WeekConfigAdmin(admin.ModelAdmin):
    list_display = ["week_no", "reg_start_at", "reg_ended_at"]
    list_editable = ["reg_start_at", "reg_ended_at"]

admin.site.register(Event, EventAdmin)
admin.site.register(Reg, RegAdmin)
admin.site.register(WeekConfig, WeekConfigAdmin)
