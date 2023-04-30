import os

from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from pprint import pprint

from api.serializers import SignUpSerializer, EmailVerifySerializer, SignInSerializer, CompetitionSerializer, \
    CompetitionDtoSerializer
from .models import User, VerifyCode
from .services import api_competitions_to_df, active_competitions_to_dto_list, get_active_competitions
from .utils import Util, generate_code


@permission_classes([])
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        code = generate_code()
        verify_code = VerifyCode(code=code, user=user)
        verify_code.save()

        absurl = f"{os.environ.get('FRONT_URL')}/email-verify?code=" + str(code)
        email_body = 'Hi ' + user.username + '. Use the link below to to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def competitions_view(request):
    api_active_competitions = get_active_competitions()
    active_competitions_df = api_competitions_to_df(api_active_competitions)
    active_competitions = active_competitions_to_dto_list(active_competitions_df)
    for c in active_competitions:
        pprint(vars(c))
    serializer = CompetitionDtoSerializer(active_competitions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([])
class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer

    def post(self, request):
        code = request.data['code']

        try:
            verify_code = VerifyCode.objects.get(code=code)
            user = User.objects.get(id=verify_code.user_id)

            if not user.is_verified:
                user.is_verified = True
                user.save()

            verify_code.delete()

            return Response(user.tokens(), status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'An error has occurred. Please follow the link again'},
                            status=status.HTTP_404_NOT_FOUND)


@permission_classes([])
class SignInView(TokenObtainPairView):
    serializer_class = SignInSerializer
