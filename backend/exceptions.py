from rest_framework.exceptions import APIException
from rest_framework import status

class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Expired" 

class NotAuthorizedError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = None

    def __init__(self, msg):
        self.detail = msg

class DoesntExistError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = None

    def __init__(self, msg):
        self.detail = msg
