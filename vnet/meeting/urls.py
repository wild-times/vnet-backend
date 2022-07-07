from django.urls import path

from .views import meeting_details, user_meetings


app_name = 'meeting'

urlpatterns = [
    # meeting/meetings/
    path('meetings/', user_meetings, name='all-meetings'),

    # meeting/meetings/zsd8z98dn/
    path('meetings/<str:meeting_id>/', meeting_details, name='meeting-details'),
]
