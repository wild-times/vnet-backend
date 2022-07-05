import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from meeting.routing import websocket_urlpatterns as meeting_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vnet.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(meeting_websocket_urlpatterns))
})
