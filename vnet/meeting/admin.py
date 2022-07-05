from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'meeting_id', 'host']
    fieldsets = [
        (
            None, {
                'fields': ['title', 'host', 'notes', 'start_time', 'end_time']
            }
        ),
        (
            'MISC', {
                'fields': ['meeting_uuid', 'meeting_id']
            }
        )
    ]
    readonly_fields = ['meeting_uuid', 'meeting_id']
