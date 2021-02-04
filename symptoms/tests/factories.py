from factory import django, Faker

from symptoms.models import Sintoma


class SymptomFactory(django.DjangoModelFactory):
    nombre = Faker('word')
    descripcion = Faker('word')

    class Meta:
        model = Sintoma
