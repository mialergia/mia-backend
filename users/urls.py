from django.urls import path, include
from users.views import CustomRegisterView, NewEmailConfirmation
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

urlpatterns = [
    path(
        'account-confirm-email/<str:key>/',
        ConfirmEmailView.as_view(),
        name='account_confirm_email'
    ),
    path('sign-up/', CustomRegisterView.as_view()),
    path(
        'account-confirm-email',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    path('^', include('django.contrib.auth.urls')),
    path(
        'resend-verification-email/',
        NewEmailConfirmation.as_view(),
        name='resend-email-confirmation',
    ),
]
