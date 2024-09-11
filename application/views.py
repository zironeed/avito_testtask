from rest_framework import status
from rest_framework.response import Response


def ping():
    return Response({'message': 'ok'}, status=status.HTTP_200_OK)
