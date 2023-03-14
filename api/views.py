from rest_framework import generics
from rest_framework.decorators import permission_classes

from api.serializers import SignUpSerializer


@permission_classes([])
class SignUpUserAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
