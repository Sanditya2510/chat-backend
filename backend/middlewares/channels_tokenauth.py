from urllib.parse import parse_qs

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from backend.exceptions import TokenExpired

def get_user(token):
    """
    get_user from token
    """
    user = cache.get(token)

    if user is None:
        raise TokenExpired
    
    return user

class TokenAuthMiddleware:
    """
    Middleware which populates scope["user"] from a simple JWT.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        scope["user"] = get_user(token)

        return await self.inner(scope, receive, send)