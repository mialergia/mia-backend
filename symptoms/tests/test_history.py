from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse

from symptoms.tests.factories import HistoryFactory
from users.tests.factories import UserFactory
from symptoms.models import Sintoma, Historial
from alergias.utils import get_random_choices
from symptoms.serializers import HistorialSerializer

fake = Faker()


class TestHistory(TestCase):
    fixtures = ['sintomas_categorias.json', 'sintomas']

    @classmethod
    def setUp(self):
        self.history_url = reverse('historial-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        symptoms_id = [symptom.id for symptom in Sintoma.objects.all()]
        self.symptoms_selected = get_random_choices(symptoms_id, 5)

    def test_create_history(self):
        response = self.client_test.post(
            self.history_url,
            {
                'sintomas': self.symptoms_selected,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_history = HistorialSerializer(Historial.objects.first()).data
        response_history = response.data

        self.assertEqual(response_history, db_history)

    def test_create_history_with_empty_symptoms(self):
        response = self.client_test.post(
            self.history_url
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_history = HistorialSerializer(Historial.objects.first()).data
        response_history = response.data

        self.assertEqual(response_history, db_history)

    def test_get_history(self):
        HistoryFactory.create_batch(10, symptoms=self.symptoms_selected, usuario=self.user)
        response = self.client_test.get(self.history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_history = HistorialSerializer(Historial.objects.all(), many=True).data
        response_history = response.data

        self.assertEqual(response_history, db_history)

    def test_delete_symptom(self):
        HistoryFactory(symptoms=self.symptoms_selected, usuario=self.user)
        history_id = Historial.objects.first().id

        response = self.client_test.delete(f'{self.history_url}{history_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Historial.objects.first())
