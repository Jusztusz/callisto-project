from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from services.routing import websocket_urlpatterns as serviceRoute
from hardware.routing import websocket_urlpatterns as hardwareRoute
from network.routing import websocket_urlpatterns as networkRoute

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            serviceRoute + hardwareRoute + networkRoute
        )
    ),
})