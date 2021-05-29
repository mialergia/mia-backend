import factory
import random
from factory import django, Faker

from pollens.models import Polen, ReporteConcentracion, NivelesPolen
from alergias.utils.tests import get_random_choices


class ConcentrationReportFactory(django.DjangoModelFactory):
    tiempo_extra = Faker('random_int')
    tiempo_total = Faker('random_int')
    porcentaje_muestreado = random.random()

    class Meta:
        model = ReporteConcentracion


class PollenLevel(django.DjangoModelFactory):
    reporte = factory.SubFactory(ConcentrationReportFactory)
    polen = get_random_choices(Polen.objects.all(), 1)[0]
    nivel = random.uniform(0, 100)

    class Meta:
        model = NivelesPolen


class ConcentrationReportWithPollenLevelFactory(ConcentrationReportFactory):
    pollen1 = factory.RelatedFactory(
        PollenLevel,
        factory_related_name='reporte',
    )
    pollen2 = factory.RelatedFactory(
        PollenLevel,
        factory_related_name='reporte',
    )
