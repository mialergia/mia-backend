from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from information.models import Notificacion


class User(AbstractUser):
    OPCIONES_SEXO = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    nombre = models.CharField(max_length=50, null=True, default=None, blank=True)
    fecha_nacimiento = models.DateField(null=True, default=None, blank=True)
    departamento = models.CharField(max_length=50, null=True, default=None, blank=True)
    barrio = models.CharField(max_length=50, null=True, default=None, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=OPCIONES_SEXO,
        null=True,
        default=None,
        blank=True,
    )
    necesita_onboarding = models.BooleanField(default=True)
    alergias = models.ManyToManyField('pollens.Polen', blank=True)
    onesignal_player_id = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    notificaciones = models.ManyToManyField(Notificacion, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
