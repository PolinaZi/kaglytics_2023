from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from api.serializers import SignUpSerializer, CompetitionSerializer
from .services import get_active_competitions


@permission_classes([])
class SignUpUserAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer


@api_view(["GET"])
def competitions_view(request):
    competitions = get_active_competitions()
    serializer = CompetitionSerializer(competitions, many=True)
    return Response(serializer.data)
