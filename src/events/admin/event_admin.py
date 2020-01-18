from django.contrib import admin
from django.utils.timezone import localtime
from events.models import Event, WEEK_OFFSET


class EventTagInline(admin.TabularInline):
    model = Event.custom_tags.through


class WeekNoFilter(admin.SimpleListFilter):
    title = "week number"
    parameter_name = "week_no"

    def lookups(self, request, model_admin):
        return (
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        value = int(self.value())
        return queryset.filter(start_at__week=value - WEEK_OFFSET)


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "week_no",
        "day_of_week",
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
    list_filter = [
        WeekNoFilter,
        "demand",
        "locked",
        "hidden",
        "is_fcfs",
        "locking_reason",
    ]
    inlines = [EventTagInline]
    exclude = ["custom_tags"]

    week_no = lambda self, event: event.week_no()  # noqa
    week_no.short_description = "Wk"
    day_of_week = lambda self, event: event.day_of_week()  # noqa
    day_of_week.short_description = "Wd"
    date = lambda self, event: localtime(event.start_at).date()  # noqa
    date.admin_order_field = "start_at"
    start_time = lambda self, event: localtime(event.start_at).time()  # noqa
    start_time.short_description = "Start"
    ended_time = lambda self, event: localtime(event.ended_at).time()  # noqa
    ended_time.short_description = "End"
