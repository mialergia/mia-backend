import factory
from factory import django, Faker

from users.tests.factories import UserFactory
from symptoms.models import (
    CategoriaSintoma,
    Sintoma,
    Historial,
    TipoRespuesta,
    Pregunta,
    EntradaDiario,
    ValorRespuesta
)
from alergias.utils.tests import get_random_coordinate, get_random_choices


class SymptomCategoryFactory(django.DjangoModelFactory):
    identificador = factory.Sequence(lambda n: "categoria_sintoma_id_%d" % n)
    pregunta = Faker('text', max_nb_chars=255)

    class Meta:
        model = CategoriaSintoma


class SymptomFactory(django.DjangoModelFactory):
    nombre = Faker('word')
    descripcion = Faker('text', max_nb_chars=255)
    categoria = factory.SubFactory(SymptomCategoryFactory)

    class Meta:
        model = Sintoma


class HistoryFactory(django.DjangoModelFactory):
    usuario = factory.SubFactory(UserFactory)

    @factory.post_generation
    def symptoms(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for symptom in extracted:
                self.sintomas.add(symptom)

    class Meta:
        model = Historial


class QuestionFactory(django.DjangoModelFactory):
    pregunta = factory.Iterator(Pregunta.objects.all())
    tipo_respuesta = factory.Iterator(TipoRespuesta.objects.all())

    class Meta:
        model = Pregunta


class DiaryEntryFactory(django.DjangoModelFactory):
    usuario = factory.SubFactory(UserFactory)
    fecha = Faker('date')
    coordenadas = get_random_coordinate()
    comentario = Faker('text', max_nb_chars=255)

    class Meta:
        model = EntradaDiario


class AnswerValueFactory(django.DjangoModelFactory):
    entrada_diario = factory.SubFactory(DiaryEntryFactory)
    pregunta = factory.SubFactory(QuestionFactory)
    respuesta = factory.LazyAttribute(
        lambda a: get_random_choices(a.pregunta.tipo_respuesta.opciones, 1)[0],
    )

    class Meta:
        model = ValorRespuesta


class DiaryEntryWithAnswerValueFactory(DiaryEntryFactory):
    answer1 = factory.RelatedFactory(
        AnswerValueFactory,
        factory_related_name='entrada_diario',
    )
    answer2 = factory.RelatedFactory(
        AnswerValueFactory,
        factory_related_name='entrada_diario',
    )
