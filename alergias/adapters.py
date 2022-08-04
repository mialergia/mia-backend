from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from alergias.gmail import send_email_confirmation


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
        current_site = get_current_site(request)
        account_confirm_email = '/api/v1/auth/register/account-confirm-email/'
        context['activate_url'] = (
            settings.BASE_URL + account_confirm_email + context['key']
        )
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    # sing-up
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        send_email_confirmation(emailconfirmation.email_address.email, activate_url)
