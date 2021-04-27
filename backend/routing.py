from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from backend.middlewares.channels_tokenauth import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})