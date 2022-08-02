from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse
import random

from symptoms.tests.factories import SymptomFactory
from users.tests.factories import UserFactory
from symptoms.models import Sintoma, CategoriaSintoma

fake = Faker()


class TestSymptoms(TestCase):
    fixtures = ['sintomas_categorias.json']

    @classmethod
    def setUp(self):
        self.symptom_url = reverse('sintoma-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        self.categorias = CategoriaSintoma.objects.all()

    def test_create_symptom(self):
        nombre = fake.word()
        descripcion = fake.latlng()
        categoria = random.choice(self.categorias).id

        response = self.client_test.post(
            self.symptom_url,
            {
                'nombre': nombre,
                'descripcion': descripcion,
                'categoria': categoria,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_symptom = Sintoma.objects.first()
        response_symptom = response.data

        self.assertEqual(response_symptom['id'], db_symptom.id)
        self.assertEqual(response_symptom['nombre'], db_symptom.nombre)

    def test_get_symptoms(self):
        SymptomFactory.create_batch(10)
        response = self.client_test.get(self.symptom_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for symptom in response.data:
            db_symptoms = Sintoma.objects.get(id=symptom['id'])
            self.assertEqual(symptom['nombre'], db_symptoms.nombre)
            self.assertEqual(symptom['descripcion'], db_symptoms.descripcion)

    def test_delete_symptom(self):
        SymptomFactory()
        symptom_id = Sintoma.objects.first().id
        response = self.client_test.delete(f'{self.symptom_url}{symptom_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Sintoma.objects.first())
