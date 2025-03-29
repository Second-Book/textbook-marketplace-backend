import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "textbook_marketplace.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter([
                path("ws/chat/", ChatConsumer.as_asgi()),
            ])
        )
    }
)
