from django.test import TestCase
from rest_framework import status
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse

from symptoms.tests.factories import SymptomCategoryFactory
from users.tests.factories import UserFactory
from symptoms.models import CategoriaSintoma
from symptoms.serializers import CategoriaSintomaSerializer

fake = Faker()


class TestSymptomCategory(TestCase):

    @classmethod
    def setUp(self):
        self.symptom_category_url = reverse('categoriasintoma-list')
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)

    def test_create_sympotom_category(self):
        id = fake.word()
        question = fake.text(max_nb_chars=255)

        response = self.client_test.post(
            self.symptom_category_url,
            {
                'identificador': id,
                'pregunta': question,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        db_symptom_category = CategoriaSintomaSerializer(CategoriaSintoma.objects.first()).data
        response_symptom_category = response.data
        self.assertEqual(response_symptom_category, db_symptom_category)

    def test_get_sympotom_category(self):
        SymptomCategoryFactory.create_batch(10)
        response = self.client_test.get(self.symptom_category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_symptom_category = CategoriaSintomaSerializer(CategoriaSintoma.objects.all(), many=True).data
        response_symptom_category = response.data
        self.assertEqual(response_symptom_category, db_symptom_category)

    def test_delete_sympotom_category(self):
        SymptomCategoryFactory()
        symptom_category_id = CategoriaSintoma.objects.first().id
        response = self.client_test.delete(f'{self.symptom_category_url}{symptom_category_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(CategoriaSintoma.objects.first())
