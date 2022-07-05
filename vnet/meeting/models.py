from django.db import models

from django.conf import settings


class Meeting(models.Model):
    objects = models.Manager()
    meeting_uuid = models.UUIDField()
    meeting_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100, help_text='Name of the meeting')
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField(help_text='More info about the meeting')
    start_time = models.DateTimeField(help_text='Time and date the meeting starts')
    end_time = models.DateTimeField(help_text='Time and date the meeting ends', null=True)

    def __str__(self):
        return f'<Meeting titles {self.title}>'
