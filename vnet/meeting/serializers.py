from rest_framework.serializers import ModelSerializer, UUIDField, CharField, URLField

from .models import Meeting
from core.serializers import CoreUserSerializer


class MeetingSerializer(ModelSerializer):
    host = CoreUserSerializer(no_acs=True, read_only=True)
    meeting_uuid = UUIDField(read_only=True)
    meeting_id = CharField(read_only=True, max_length=1000)
    meeting_url = URLField(source='get_meeting_url', read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'title', 'notes', 'start_time', 'end_time', 'meeting_uuid', 'meeting_id', 'host', 'meeting_url'
        )
