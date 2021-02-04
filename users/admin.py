from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'nombre', 'sexo', 'fecha_nacimiento', 'departamento', 'barrio', 'onesignal_player_id']
    list_filter = ('sexo',)
    fieldsets = (
        (
            None,
            {
                'fields':
                (
                    'nombre',
                    'sexo',
                    'fecha_nacimiento',
                    'departamento',
                    'barrio'
                    'historial_sintomas',
                    'email',
                    'password'
                )
            }
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nombre',
                'sexo',
                'fecha_nacimiento',
                'departamento',
                'barrio',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            )
        }),
    )
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Token)
admin.site.unregister(auth.models.Group)
admin.site.unregister(Site)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
