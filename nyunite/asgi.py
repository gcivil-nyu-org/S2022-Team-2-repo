import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nyunite.settings")
django_asgi_app = get_asgi_application()

application = None


if __name__ == "__main__":
    from django_private_chat2 import urls

    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns)),
        }
    )
