from rest_framework.permissions import AllowAny
from rest_framework import generics

from api.serializers import SignUpSerializer


class SignUpUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
