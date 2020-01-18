from django.contrib import admin
from events.models import Event, Reg, WeekConfig, Announcement, Tag
from .event_admin import EventAdmin
from .reg_admin import RegAdmin


@admin.register(WeekConfig)
class WeekConfigAdmin(admin.ModelAdmin):
    list_display = ["week_no", "reg_start_at", "reg_ended_at"]
    list_editable = ["reg_start_at", "reg_ended_at"]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "hidden"]
    list_editable = ["text", "hidden"]


admin.site.register(Event, EventAdmin)
admin.site.register(Reg, RegAdmin)
admin.site.register(Tag)
