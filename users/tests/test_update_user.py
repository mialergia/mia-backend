from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from faker.providers import lorem, misc
import random
from django.urls import reverse

from users.tests.factories import UserFactory
from users.models import User

DATE_FORMAT = '%d-%m-%Y'

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(misc)


class TestUserLogin(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client_test = APIClient()
        self.user = UserFactory()
        self.client_test.force_authenticate(self.user)
        self.update_user_url = reverse('rest_user_details')

    def test_if_user_is_authenticated_then_update_his_data_correctly(self):
        nombre = Faker().name()
        sexo = random.choice(['M', 'F'])
        departamento = fake.word()
        fecha_nacimiento = fake.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=90)

        response = self.client_test.put(
            self.update_user_url,
            {
                'nombre': nombre,
                'sexo': sexo,
                'departamento': departamento,
                'fecha_nacimiento': fecha_nacimiento,
            }
        )

        response_db = User.objects.first()
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], response_db.id)
        self.assertEqual(response_data['email'], response_db.email)
        self.assertEqual(response_data['nombre'], response_db.nombre)
        self.assertEqual(response_data['sexo'], response_db.sexo)
        self.assertEqual(response_data['departamento'], response_db.departamento)
        self.assertEqual(response_data['fecha_nacimiento'], str(response_db.fecha_nacimiento))
