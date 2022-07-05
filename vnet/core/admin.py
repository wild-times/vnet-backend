from django.contrib import admin

from .models import CoreUser


@admin.register(CoreUser)
class CoreUserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'meeting_name',]
    fieldsets = [
        (
            None, {
                'fields': ['username', 'first_name', 'last_name', 'profile_image']
            }
        ),
        (
            'ACS', {
                'fields': ['meeting_name', 'acs_identity', 'acs_token']
            }
        ),
        (
            'Permissions', {
                'fields': ['is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions']
            }
        ),
        (
            'Important Dates', {
                'fields': ['date_joined', 'last_login']
            }
        )
    ]
