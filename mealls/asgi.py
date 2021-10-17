import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealls.settings.dev')
django.setup()

from django.core.wsgi import get_wsgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing


application = ProtocolTypeRouter({
    # 'http': get_wsgi_application(),
    'websocket': URLRouter(routing.websocket_urlpatterns),
})
