from django.urls import path

from .views import CoreIndex, user_details, no_login_message, login

app_name = 'core'


urlpatterns = [
    # core/
    path('', CoreIndex.as_view(), name='index'),

    # core/p-login/
    path('p-login/', login, name='api-login'),

    # core/get/user-details/
    path('get/user-details/', user_details, name='user-details'),

    # core/error/
    path('error/', no_login_message, name='no-user'),
]
