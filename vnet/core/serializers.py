from rest_framework.serializers import ModelSerializer, CharField

from .models import CoreUser


class CoreUserSerializer(ModelSerializer):
    auth_token = CharField(read_only=True, source='get_auth_token')

    def __init__(self, *args, **kwargs):
        no_acs = kwargs.pop('no_acs',  False)
        super(CoreUserSerializer, self).__init__(*args, **kwargs)

        if no_acs:
            self.fields.pop('acs_identity')
            self.fields.pop('acs_token')
            self.fields.pop('auth_token')

    class Meta:
        model = CoreUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'meeting_name', 'profile_image', 'acs_identity', 'acs_token',
            'auth_token'
        )
