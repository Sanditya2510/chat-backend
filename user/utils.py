from django.conf import settings
from django.utils import timezone
import datetime
from rest_framework_jwt.settings import api_settings

def jwt_response_payload_handler(token, user=None, request=None):
    """
    This defines the contents of JWT Token.
    Token consists of token, first name, last name, email, username
    :param token: String
    :param user: User object

    Returns:
        [dict] -- [Response on fetching a token]
    """
    return {
        "token": token,
        "first name": user.first_name,
        "last name": user.last_name,
        "email": user.email,
        "username": user.username,
    }

def get_token(user):
    """
    Returns jwt token
    Args:
        user: User Model Object

    Returns:
        res: JWT Token 
    """
    JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
    JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
    JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

    payload = JWT_PAYLOAD_HANDLER(user)
    token = JWT_ENCODE_HANDLER(payload)
    res = JWT_RESPONSE_PAYLOAD_HANDLER(token, user)
    return res