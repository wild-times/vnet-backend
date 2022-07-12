from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.views import status
from rest_framework.decorators import api_view, permission_classes

from .serializers import CoreUserSerializer


class CoreIndex(TemplateView):
    template_name = 'core/index.html'


def no_login_message(request):
    return JsonResponse({'message': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([])
def login(request):
    response = {
        'url': 'user authentication'
    }
    resp_status = status.HTTP_200_OK

    if request.method == 'GET':
        response.update({
            'fields': ['username', 'password'],
            'returns': ['user_data']
        })

    elif request.method == 'POST':
        acs = not request.data.get('acs', True)
        _post_resp = {
            'success': False,
            'error': 'Wrong Credentials'
        }
        resp_status = status.HTTP_400_BAD_REQUEST
        authenticated_user = None

        if request.data.get('password') and request.data.get('username'):
            authenticated_user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )

        if authenticated_user:
            _post_resp.pop('error')
            _post_resp.update({
                'success': True,
                'details': CoreUserSerializer(authenticated_user, no_acs=acs).data
            })
            resp_status = status.HTTP_200_OK

        response.update(_post_resp)

    return JsonResponse(response, status=resp_status)


@login_required(login_url=reverse_lazy('core:no-user'), redirect_field_name=None)
def user_details(request):
    acs = request.GET.get('acs', 0)
    user_det = CoreUserSerializer(request.user, no_acs=True)

    if bool(int(acs)):
        user_det = CoreUserSerializer(request.user)

    return JsonResponse(user_det.data)
