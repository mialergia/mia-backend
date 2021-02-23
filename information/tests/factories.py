from factory import django, Faker

from information.models import Notificacion


class NotificacionesFactory(django.DjangoModelFactory):
    texto = Faker('text', max_nb_chars=255)

    class Meta:
        model = Notificacion
