from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CoreUser(AbstractUser):
    meeting_name = models.CharField(max_length=100, blank=True, null=True)
    acs_identity = models.CharField(max_length=1000, blank=True, null=True)
    acs_token = models.CharField(max_length=2000, blank=True, null=True)
    objects = UserManager()
    profile_image = models.ImageField(
        upload_to='profiles/images/pc/', default='profile/images/def/pc.jpg',
        blank=True,
        null=True
    )
