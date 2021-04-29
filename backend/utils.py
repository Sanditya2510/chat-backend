from uuid import uuid4

from django.core.cache import cache

def get_ws_token(duration, user):
    token = str(uuid4())
    cache.set(token, user, duration)
    return token