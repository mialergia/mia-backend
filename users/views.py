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
from alergias.gmail import sendingMessage

from allauth.account.adapter import DefaultAccountAdapter
from .models import User


class CustomRegisterView(RegisterView, DefaultAccountAdapter):
    print(f'/////////// CustomRegisterView 1?/////////////')
    queryset = User.objects.all()
    # def post(self, request):
    #     # activate_url = reverse("account_confirm_key")
    #     # print(activate_url)
    #     print(vars(self))
    #     print(request.data)
    #     # print(self.objects.all())
    #     # print(request.objects.all())
    #     print(f'////////// CustomRegisterView - post //////////////')
    #     print(f'{request.data}')
        
        # try:
        #     user = get_object_or_404(User, email=request.data['email'])
        #     emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()
        # except Exception:
        #     raise ValidationError('Este email no existe.')

        # if emailAddress:
        #     raise ValidationError('Este email ya está verificado.')
        # else:
        # sendingMessage(request.data['email'], 'Email de confirmación', 'Email de confirmación body')
        # return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)

    def send_mail(self, template_prefix, email, context):
        print(f'////////// send_mail //////////////')
        # current_site = get_current_site(request)
        print(F'{self}')
        print(request)
        print(emailconfirmation)
        account_confirm_email = '/api/v1/auth/register/account-confirm-email/'
        context['activate_url'] = (
            settings.BASE_URL + account_confirm_email + context['key']
        )
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
        return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        print(f'////////// send_confirmation_mail //////////////')
        current_site = get_current_site(request)
        print(F'{self}')
        print(request)
        print(emailconfirmation)
        return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)

    # def get_response_data(self, request, emailconfirmation, signup):
    #     print(F'{self}')
    #     print(request)
    #     print(emailconfirmation)
    #     print(f'////////// get_response_data //////////////')
    #     return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)


        # if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
        #     return {"detail": _("Verification Email Sent")}

        # if getattr(settings, 'REST_USE_JWT', False):
        #     data = {
        #         'user': user,
        #         'token': self.token
        #     }
        #     return JWTSerializer(data).data
        # else:
        #     return TokenSerializer(user.auth_token, context={"request": self.request}).data
    



class NewEmailConfirmation(APIView):
    # print(f'////////// NewEmailConfirmation 1 //////////////')
    permission_classes = [AllowAny]

    def post(self, request):
        print(f'////////// NewEmailConfirmation 1 //////////////')
        try:
            user = get_object_or_404(User, email=request.data['email'])
            emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()
        except Exception:
            raise ValidationError('Este email no existe.')

        if emailAddress:
            raise ValidationError('Este email ya está verificado.')
        else:
            send_email_confirmation(request, user=user, signup=True)
            # sendingMessage(request.data['email'], 'Email de confirmación', 'Email de confirmación body')
            return Response({'message': 'Email de confirmación enviado'}, status=status.HTTP_201_CREATED)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
