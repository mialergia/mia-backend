import factory
import random
from factory import django, Faker

from pollens.models import GrupoPolinico, Polen


class GrupoPolinicoFactory(django.DjangoModelFactory):
    id = factory.Sequence(lambda n: "gp_id_%d" % n)
    nombre = Faker('word')
    unidad_medida = Faker('text', max_nb_chars=12)
    nivel_alto = Faker('random_int')
    nivel_medio = Faker('random_int')
    nivel_alto_sumatoria = Faker('random_int')
    nivel_medio_sumatoria = Faker('random_int')

    class Meta:
        model = GrupoPolinico


class PolenFactory(django.DjangoModelFactory):
    tipo = Faker('word')
    nombre_cientifico = Faker('word')
    nombre_comun = Faker('word')
    familia = Faker('word')
    picks_presente = bool(random.getrandbits(1))
    grupo_polinico = factory.SubFactory(GrupoPolinicoFactory)
    alergenicidad = Faker('word')
    nivel_alto = Faker('random_int')
    nivel_medio = Faker('random_int')
    nombre_alergia = Faker('word')

    class Meta:
        model = Polen
