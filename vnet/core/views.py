from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.views import status

from .serializers import CoreUserSerializer


class CoreIndex(TemplateView):
    template_name = 'core/index.html'


def no_login_message(request):
    return JsonResponse({'message': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)


@login_required(login_url=reverse_lazy('core:no-user'), redirect_field_name=None)
def user_details(request):
    acs = request.GET.get('acs', 0)
    user_det = CoreUserSerializer(request.user, no_acs=True)

    if bool(int(acs)):
        user_det = CoreUserSerializer(request.user)

    return JsonResponse(user_det.data)
