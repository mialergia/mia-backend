from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field


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
