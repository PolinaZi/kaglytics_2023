import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from .models import User
from .utils import Util
from api.serializers import SignUpSerializer


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

        token = RefreshToken.for_user(user).access_token
        absurl = 'http://localhost:8000/email-verify?token=' + str(token)
        email_body = 'Hi ' + user.username + '. Use the link below to to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def competitions_view(request):
    # todo
    return Response()


class EmailVerifyView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
