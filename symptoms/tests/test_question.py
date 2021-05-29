from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse

from symptoms.tests.factories import QuestionFactory
from users.tests.factories import UserFactory
from symptoms.models import TipoRespuesta, Pregunta
from alergias.utils.tests import get_random_choices, test_unauthorized_call
from symptoms.serializers import PreguntaSerializer

fake = Faker()


class TestQuestion(TestCase):
    fixtures = ['tipo_respuestas']

    @classmethod
    def setUp(self):
        self.question_url = reverse('pregunta-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        answer_type_id = [answer_type.id for answer_type in TipoRespuesta.objects.all()]
        self.answer_type = get_random_choices(answer_type_id, 1)

    def test_create_question(self):
        question = fake.text(max_nb_chars=255)

        def call_endpoint():
            return self.client_test.post(
                self.question_url,
                {
                    'pregunta': question,
                    'tipo_respuesta': self.answer_type,
                }
            )

        response = call_endpoint()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_question = PreguntaSerializer(Pregunta.objects.first()).data
        response_db_question = response.data
        self.assertEqual(response_db_question, db_question)

        test_unauthorized_call(self, call_endpoint)

    def test_get_questions(self):
        QuestionFactory.create_batch(10)

        def call_endpoint():
            return self.client_test.get(self.question_url)

        response = call_endpoint()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_question = PreguntaSerializer(Pregunta.objects.all(), many=True).data
        response_question = response.data
        self.assertEqual(response_question, db_question)

        test_unauthorized_call(self, call_endpoint)

    def test_delete_symptom(self):
        QuestionFactory()
        question_id = Pregunta.objects.first().id

        def call_endpoint():
            return self.client_test.delete(f'{self.question_url}{question_id}/')

        response = call_endpoint()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Pregunta.objects.first())

        test_unauthorized_call(self, call_endpoint)
