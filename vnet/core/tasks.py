from azure.communication.identity import CommunicationIdentityClient, CommunicationTokenScope, \
    CommunicationUserIdentifier

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import CoreUser


acs_client = CommunicationIdentityClient.from_connection_string(settings.ACS_CONNECTION_STRING)


def create_azure_identity(user_pk):
    """Create a new azure communication service identity and saves it to user"""
    try:
        user = CoreUser.objects.get(pk=user_pk)
        acs_user, acs_user_token = acs_client.create_user_and_token(scopes=[CommunicationTokenScope.VOIP])
        user.acs_identity = acs_user.properties.get('id')
        user.acs_token = acs_user_token.token
        user.acs_token_expiration = acs_user_token.expires_on
        user.save()
    except ObjectDoesNotExist:
        pass


def refresh_user_token(user_pk):
    """Refresh a user's token and save"""
    try:
        user = CoreUser.objects.get(pk=user_pk)
        mins_to_exp = (user.acs_token_expiration - timezone.now()).seconds / 60

        if (timezone.now() > user.acs_token_expiration) or (mins_to_exp < 120):
            acs_user = CommunicationUserIdentifier(user.acs_identity)
            acs_token = acs_client.get_token(acs_user, [CommunicationTokenScope.VOIP])
            user.acs_token = acs_token.token
            user.acs_token_expiration = acs_token.expires_on
            user.save()

    except ObjectDoesNotExist:
        pass


@receiver(post_save, sender=CoreUser)
def create_user_acs_identity(**kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')

        if not user.acs_identity:
            create_azure_identity(user.pk)


@receiver(post_delete, sender=CoreUser)
def delete_user_acs_identity(**kwargs):
    user = kwargs.get('instance')

    if user.acs_identity:
        acs_client.delete_user(CommunicationUserIdentifier(user.acs_identity))
