"""
ASGI config for talkitout project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import chat.routing
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from whiteboardcollab.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "talkitout.settings")

application = get_asgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "talkitout.settings")


# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()
import whiteboardcollab.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns + chat.routing.websocket_urlpatterns)
            )
        ),
    }
)
# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
#     }
# )
