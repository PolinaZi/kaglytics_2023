from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view

from api.serializers import SignUpSerializer
from .kaggle_api import api


@permission_classes([])
class SignUpUserAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

