from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from api.serializers import SignUpSerializer


@permission_classes([])
class SignUpUserAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer


@api_view(["GET"])
def competitions_view(request):
    # todo
    return Response()
