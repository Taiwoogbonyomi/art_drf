from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .settings import(
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE, JWT_AUTH_SECURE
)


@api_view(['GET'])
def root_route(request):
    """
    A root endpoint providing a welcome message for the API.
    """
    return Response(
        {"message": "Welcome to my Art drf API!"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
# Fix for Django Rest Framework logout bug from Code Institute
# DRF walkthrough
def logout_route(request):
    print('Doing logout')
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


