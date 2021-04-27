from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token):
    """
    get_user from token
    """
    try:
        token_data = UntypedToken(token)
        return get_user_model().objects.get(id=token_data["user_id"])
    except (InvalidToken, TokenError, get_user_model().DoesNotExist):
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Middleware which populates scope["user"] from a simple JWT.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        scope["user"] = await get_user(token)

        return await self.inner(scope, receive, send)