from django.urls import path

from .views import meeting_details, user_meetings, create_meeting


app_name = 'meeting'

urlpatterns = [
    # meeting/meetings/
    path('meetings/', user_meetings, name='all-meetings'),

    # meeting/meetings/zsd8z98dn/
    path('meetings/<str:meeting_id>/', meeting_details, name='meeting-details'),

    # meeting/new/
    path('new/', create_meeting, name='new-meeting'),
]
