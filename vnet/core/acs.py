from .tasks import create_azure_identity, refresh_user_token


class ACSWork:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.acs_identity:
                # create an identity and token if none exists
                create_azure_identity(request.user.pk)

            else:
                # refresh token if it's 2 hours to expiration
                refresh_user_token(request.user.pk)

        return self.get_response(request)
