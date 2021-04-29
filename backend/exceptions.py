from rest_framework.exceptions import APIException
from rest_framework import status

class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Expired" 