from django.urls import path

from .views import CoreIndex

app_name = 'core'


urlpatterns = [
    path('', CoreIndex.as_view())
]
