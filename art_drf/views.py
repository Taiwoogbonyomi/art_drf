from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def root_route(request):
    """
    A root endpoint providing a welcome message for the API.
    """
    return Response(
        {"message": "Welcome to my Art drf API!"},
        status=status.HTTP_200_OK
    )
