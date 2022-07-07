from rest_framework.serializers import ModelSerializer

from .models import CoreUser


class CoreUserSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        no_acs = kwargs.pop('no_acs',  False)
        super(CoreUserSerializer, self).__init__(*args, **kwargs)

        if no_acs:
            self.fields.pop('acs_identity')
            self.fields.pop('acs_token')

    class Meta:
        model = CoreUser
        fields = (
            'username', 'first_name', 'last_name', 'meeting_name', 'profile_image', 'acs_identity', 'acs_token'
        )
