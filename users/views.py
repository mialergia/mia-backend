from rest_framework.views import APIView
from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from allauth.account.admin import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import User


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()


class NewEmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = get_object_or_404(User, email=request.data['email'])
            emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()
        except Exception:
            raise ValidationError('Este email no existe.')

        if emailAddress:
            raise ValidationError('Este email ya está verificado.')
        else:
            send_email_confirmation(request, user=user, signup=True)
            return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
