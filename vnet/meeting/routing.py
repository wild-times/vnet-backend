from django.urls import re_path

from .consumers import VNETSignaling


websocket_urlpatterns = [
    re_path(r'vnet/ps/(?P<code>\d{6})/', VNETSignaling.as_asgi()),
]
