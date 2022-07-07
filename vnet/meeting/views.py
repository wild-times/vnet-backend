from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import status

from .serializers import MeetingSerializer
from .models import Meeting


# meeting for a user
@login_required(redirect_field_name=None, login_url=reverse_lazy('core:no-user'))
def user_meetings(request):
    meetings = Meeting.objects.filter(host__pk=request.user.pk)
    ser_meetings = MeetingSerializer(meetings, many=True)
    return JsonResponse({'meetings': ser_meetings.data})


# specific meeting
@login_required(redirect_field_name=None, login_url=reverse_lazy('core:no-user'))
def meeting_details(request, meeting_id):
    try:
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        content = MeetingSerializer(meeting).data
        st = status.HTTP_200_OK
    except ObjectDoesNotExist:
        content = {
            'message': 'Meeting not found'
        }
        st = status.HTTP_404_NOT_FOUND

    return JsonResponse(content, status=st)
