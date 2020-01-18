from django.contrib import admin
from events.models import WEEK_OFFSET


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
        return queryset.filter(event__start_at__week=value - WEEK_OFFSET)


class RegAdmin(admin.ModelAdmin):
    list_display = ["id", "week_no", "user", "event", "demand", "status"]
    list_editable = ["status"]
    list_filter = [WeekNoFilter]

    week_no = lambda self, reg: reg.event.week_no()  # noqa
    week_no.short_description = "Wk"
    demand = lambda self, reg: reg.event.demand  # noqa
    demand.short_description = "Demand"
