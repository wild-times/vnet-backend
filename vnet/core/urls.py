from django.urls import path
from django.contrib.auth import views as auth_views

from .views import CoreIndex, user_details, no_login_message, login, CoreLogin

app_name = 'core'


urlpatterns = [
    # account/
    path('', CoreIndex.as_view(), name='index'),

    # account/p-login/
    path('p-login/', login, name='api-login'),

    # account/get/user-details/
    path('get/user-details/', user_details, name='user-details'),

    # account/error/
    path('error/', no_login_message, name='no-user'),

    # account/sign-in/
    path('sign-in/', CoreLogin.as_view(), name='sign-in'),

    # account/sign-out/
    path('sign-out/', auth_views.LogoutView.as_view(), name='sign-out'),
]
