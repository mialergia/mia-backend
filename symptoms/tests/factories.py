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
from alergias.utils import get_random_coordinate


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
    sintomas = factory.SubFactory(SymptomFactory)

    class Meta:
        model = Historial


class AnswerTypeFactory(django.DjangoModelFactory):
    identificador = factory.Sequence(lambda n: "categoria_tipo_respuesta_id_%d" % n)
    opciones = [Faker('text', max_nb_chars=25), Faker('text', max_nb_chars=25), Faker('text', max_nb_chars=25)]

    class Meta:
        model = TipoRespuesta


class QuestionFactory(django.DjangoModelFactory):
    pregunta = Faker('text', max_nb_chars=255)
    tipo_respuesta = factory.SubFactory(AnswerTypeFactory)

    class Meta:
        model = Pregunta


class DiaryEntryFactory(django.DjangoModelFactory):
    usuario = factory.SubFactory(UserFactory)
    fecha = Faker('date')
    coordenadas = get_random_coordinate()
    preguntas = factory.SubFactory(QuestionFactory)
    comentario = Faker('text', max_nb_chars=255)

    class Meta:
        model = EntradaDiario


class AnswerValueFactory(django.DjangoModelFactory):
    entrada_diario = factory.SubFactory(DiaryEntryFactory)
    pregunta = factory.SubFactory(QuestionFactory)
    respuesta = Faker('text', max_nb_chars=25)

    class Meta:
        model = ValorRespuesta
