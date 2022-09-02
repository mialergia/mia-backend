from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from alergias.gmail import send_email_confirmation, send_email_reset_password, send_message, get_service
from users.models import User
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.urls import reverse

class UserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        name = data.get('name')
        gender = data.get('gender')
        address = data.get('address')
        date_of_birth = data.get('date_of_birth')
        onesignal_player_id = data.get('onesignal_player_id')

        if name:
            user_field(user, 'name', name)
        if gender:
            user_field(user, 'gender', gender)
        if address:
            user_field(user, 'address', address)
        if date_of_birth:
            user_field(user, 'date_of_birth', date_of_birth)
        if onesignal_player_id:
            user_field(user, 'onesignal_player_id', onesignal_player_id)

        return super().save_user(request, user, form, commit=commit)
    
    # forgot password
    def send_mail(self, template_prefix, email, context):
        # urlsafe_base64_encode(force_bytes(user.pk)),
        # import pdb; pdb.set_trace()
        # msg = self.render_mail(template_prefix, email, context)
        # import pdb; pdb.set_trace()
        # send_message(msg)

        token_generator = EmailAwarePasswordResetTokenGenerator()
        user = User.objects.get(email=email)
        temp_key = token_generator.make_token(user)
        path = reverse("account_reset_password_from_key", kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key))
        # import pdb; pdb.set_trace()
        
        send_email_reset_password(email, path)

    # sing-up
    def send_confirmation_mail(self, request, emailconfirmation):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        send_email_confirmation(emailconfirmation.email_address.email, activate_url)
