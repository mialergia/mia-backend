from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse
import json
from datetime import timedelta, datetime

from symptoms.tests.factories import DiaryEntryWithAnswerValueFactory
from users.tests.factories import UserFactory
from symptoms.models import Pregunta, EntradaDiario
from alergias.utils.tests import get_random_choices, test_unauthorized_call
from symptoms.serializers import EntradaDiarioSerializer
from alergias import strings
from alergias.utils.general import CRITICAL_ANSWERS

fake = Faker()


class TestDiaryEntry(TestCase):
    fixtures = ['tipo_respuestas', 'preguntas']

    @classmethod
    def setUp(self):
        self.diary_entry_url = reverse('entradadiario-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        self.questions = [
            {
                'pregunta': question.id,
                'respuesta': get_random_choices(question.tipo_respuesta.opciones, 1)[0],
            }
            for question in Pregunta.objects.all()
        ]

    def test_create_diary_entry(self):
        date = fake.date()
        coordinates = fake.latlng()
        coordinates = {
            'longitud': float(coordinates[0]),
            'latitud': float(coordinates[1])
        }
        comment = fake.text(max_nb_chars=255)

        def call_endpoint():
            return self.client_test.post(
                self.diary_entry_url,
                {
                    'fecha': date,
                    'coordenadas': coordinates,
                    'comentario': comment,
                    'respuestas': self.questions,
                },
                format='json',
            )

        response = call_endpoint()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)

        test_unauthorized_call(self, call_endpoint)

    def test_if_create_diary_entry_with_one_critical_answer_then_low_alert_should_be_shown(self):
        date = fake.date()

        response = self.client_test.post(
            self.diary_entry_url,
            {
                'fecha': date,
                'respuestas': [{'pregunta': 1, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)
        self.assertEqual(response.data.get('alerta'), strings.low_critical_alert)

    def test_if_create_diary_entry_with_two_critical_answer_then_low_alert_should_be_shown(self):
        date = fake.date()

        response = self.client_test.post(
            self.diary_entry_url,
            {
                'fecha': date,
                'respuestas': [
                    {'pregunta': 1, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 2, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)
        self.assertEqual(response.data.get('alerta'), strings.low_critical_alert)

    def test_if_create_diary_entry_with_three_critical_answer_then_medium_alert_should_be_shown(self):
        date = fake.date()

        response = self.client_test.post(
            self.diary_entry_url,
            {
                'fecha': date,
                'respuestas': [
                    {'pregunta': 1, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 2, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 3, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)
        self.assertEqual(response.data.get('alerta'), strings.medium_critical_alert)

    def test_if_create_diary_entry_with_four_critical_answer_then_medium_alert_should_be_shown(self):
        date = fake.date()

        response = self.client_test.post(
            self.diary_entry_url,
            {
                'fecha': date,
                'respuestas': [
                    {'pregunta': 1, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 2, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 3, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    {'pregunta': 4, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)
        self.assertEqual(response.data.get('alerta'), strings.medium_critical_alert)

    def test_if_create_diary_entry_high_alert(self):
        # test if create diary entry with more than four critical answers on last week
        # then high alert should be shown

        def post_critical_day(previous_days):
            date = str((datetime.today() - timedelta(days=previous_days)).date())

            response = self.client_test.post(
                self.diary_entry_url,
                {
                    'fecha': date,
                    'respuestas': [
                        {'pregunta': 1, 'respuesta': get_random_choices(CRITICAL_ANSWERS, 1)[0]},
                    ],
                },
                format='json',
            )

            return response

        post_critical_day(7)
        post_critical_day(6)
        post_critical_day(5)
        post_critical_day(4)
        response = post_critical_day(3)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.last()).data
        response_diary_entry = response.data.get('entradas')
        self.assertEqual(response_diary_entry, db_diary_entry)
        self.assertEqual(response.data.get('alerta'), strings.high_critical_alert)

    def test_get_diary_entries(self):
        DiaryEntryWithAnswerValueFactory(usuario=self.user)

        def call_endpoit():
            return self.client_test.get(self.diary_entry_url)

        response = call_endpoit()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_diary_entry = EntradaDiarioSerializer(EntradaDiario.objects.first()).data
        response_diary_entry = response.data
        self.assertEqual(json.dumps(response_diary_entry[0]), json.dumps(db_diary_entry))

        test_unauthorized_call(self, call_endpoit, True)

    def test_delete_diary_entry(self):
        DiaryEntryWithAnswerValueFactory(usuario=self.user)
        diary_entry_id = EntradaDiario.objects.first().id

        def call_endpoit():
            return self.client_test.delete(f'{self.diary_entry_url}{diary_entry_id}/')

        response = call_endpoit()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(EntradaDiario.objects.first())

        test_unauthorized_call(self, call_endpoit)
