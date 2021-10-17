from django.urls import path, re_path
from consumers.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"room/(?P<group>\w+)/$", ChatConsumer.as_asgi()),
]