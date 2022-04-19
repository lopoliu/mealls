import os

from channels.auth import AuthMiddlewareStack

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from apps.consumers.consumer import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealls.settings.dev')

websocket_urlpatterns = [
    re_path(r"room/(?P<group>\w+)/$", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
