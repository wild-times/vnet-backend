from uuid import uuid4
from base64 import b64encode
from time import time

from django.db import models
from django.conf import settings


class Meeting(models.Model):
    objects = models.Manager()
    meeting_uuid = models.UUIDField(blank=True, null=True)
    meeting_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, help_text='Name of the meeting')
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField(help_text='More info about the meeting')
    start_time = models.DateTimeField(help_text='Time and date the meeting starts')
    end_time = models.DateTimeField(help_text='Time and date the meeting ends', null=True)

    def __str__(self):
        return f"Meeting: {self.title}"

    def __repr__(self):
        return f"<Meeting: {self.title}>"

    def save(self, *args, **kwargs):
        # add meeting UUID
        if not self.pk:
            self.meeting_uuid = uuid4()

            # add meeting code
            if not self.meeting_id:
                super().save()
                code = f'{self.host.pk}{self.pk}{int(time())}'.encode('ascii')
                self.meeting_id = str(b64encode(code))[2:-1]

        return super().save()
