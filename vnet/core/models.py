from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


class CoreUser(AbstractUser):
    meeting_name = models.CharField(max_length=100, blank=True, null=True)
    acs_identity = models.CharField(max_length=1000, blank=True, null=True)
    acs_token = models.CharField(max_length=2000, blank=True, null=True)
    acs_token_expiration = models.DateTimeField(blank=True, null=True)
    objects = UserManager()
    profile_image = models.ImageField(
        upload_to='profiles/images/pc/', default='profile/images/def/pc.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'CoreUser: {self.username}'

    def __repr__(self):
        return f'<CoreUser: {self.username}>'

    def get_auth_token(self):
        try:
            token = Token.objects.get(user__pk=self.pk).key
        except ObjectDoesNotExist:
            token = ''
        return token

    def save(self, *args, **kwargs):
        super().save()
        try:
            Token.objects.get(user__pk=self.pk)
        except ObjectDoesNotExist:
            Token.objects.create(user=self)
        return self
