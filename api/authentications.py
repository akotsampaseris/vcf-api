from asyncio import exceptions
import os
from dotenv import load_dotenv

from rest_framework import authentication, exceptions
from rest_framework.response import Response
from rest_framework import status


load_dotenv()

class SecretKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        registered_secret = os.environ.get('AUTH_SECRET_KEY')
        submitted_secret = request.META.get('HTTP_AUTHORIZATION')

        if not submitted_secret:
            raise exceptions.AuthenticationFailed(
                'Missing Authorization header.'
            )
        elif not submitted_secret == registered_secret:
            raise exceptions.AuthenticationFailed(
                'Authorization header contained wrong secret key.'
            )
