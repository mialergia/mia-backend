from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from faker.providers import lorem, misc
import random
from django.urls import reverse

from users.tests.factories import UserFactory
from pollens.tests.factories import PolenFactory
from information.tests.factories import NotificacionesFactory
from users.models import User
import alergias.strings as strings

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
        self.pollen = PolenFactory.create_batch(10)
        self.nombre = Faker().name()
        self.sexo = random.choice(['M', 'F'])
        self.departamento = fake.word()
        self.fecha_nacimiento = fake.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=90)
        self.barrio = fake.word()
        self.onesignal_player_id = fake.word()
        self.alergias = random.sample(self.pollen, 4)
        self.notificaciones = random.sample(NotificacionesFactory.create_batch(10), 5)

    def test_if_user_is_authenticated_then_update_his_data_correctly(self):
        response = self.client_test.put(
            self.update_user_url,
            {
                'nombre': self.nombre,
                'sexo': self.sexo,
                'departamento': self.departamento,
                'fecha_nacimiento': self.fecha_nacimiento,
                'barrio': self.barrio,
                'onesignal_player_id': self.onesignal_player_id,
                'alergias': [alergia.id for alergia in self.alergias],
                'notificaciones': [notificacion.id for notificacion in self.notificaciones],
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
        self.assertEqual(response_data['barrio'], response_db.barrio)
        self.assertEqual(response_data['onesignal_player_id'], response_db.onesignal_player_id)

        alergias_response = response_data['alergias']
        alergias_db = response_db.alergias.all()

        for alergia_id in alergias_response:
            self.assertIsNotNone(alergias_db.get(id=alergia_id))

        notificaciones_response = response_data['notificaciones']
        notificaciones_db = response_db.notificaciones.all()

        for notificacion_id in notificaciones_response:
            self.assertIsNotNone(notificaciones_db.get(id=notificacion_id))

    def test_if_user_tries_to_update_their_data_without_name_then_error_is_shown(self):
        response = self.client_test.put(
            self.update_user_url,
            {
                'sexo': self.sexo,
                'departamento': self.departamento,
                'fecha_nacimiento': self.fecha_nacimiento,
                'barrio': self.barrio,
                'onesignal_player_id': self.onesignal_player_id,
                'alergias': [alergia.id for alergia in self.alergias],
                'notificaciones': [notificacion.id for notificacion in self.notificaciones],
            }
        )

        self.assertEqual(str(response.data['errors'][0]['message']), strings.empty_field)
        self.assertEqual(str(response.data['errors'][0]['field']), 'nombre')

    def test_if_user_tries_to_update_their_data_without_department_then_error_is_shown(self):
        response = self.client_test.put(
            self.update_user_url,
            {
                'nombre': self.nombre,
                'sexo': self.sexo,
                'fecha_nacimiento': self.fecha_nacimiento,
                'barrio': self.barrio,
                'onesignal_player_id': self.onesignal_player_id,
                'alergias': [alergia.id for alergia in self.alergias],
                'notificaciones': [notificacion.id for notificacion in self.notificaciones],
            }
        )

        self.assertEqual(str(response.data['errors'][0]['message']), strings.empty_field)
        self.assertEqual(str(response.data['errors'][0]['field']), 'departamento')

    def test_if_user_tries_to_update_their_data_with_montevideo_department_without_neighboor_then_error_is_shown(self):
        response = self.client_test.put(
            self.update_user_url,
            {
                'nombre': self.nombre,
                'sexo': self.sexo,
                'departamento': 'Montevideo',
                'fecha_nacimiento': self.fecha_nacimiento,
                'onesignal_player_id': self.onesignal_player_id,
                'alergias': [alergia.id for alergia in self.alergias],
                'notificaciones': [notificacion.id for notificacion in self.notificaciones],
            }
        )

        self.assertEqual(str(response.data['errors'][0]['message']), strings.valid_neighboor)

    def test_if_user_tries_to_update_their_data_with_invalid_notification_id_then_error_is_shown(self):
        response = self.client_test.put(
            self.update_user_url,
            {
                'nombre': self.nombre,
                'sexo': self.sexo,
                'departamento': self.departamento,
                'fecha_nacimiento': self.fecha_nacimiento,
                'barrio': self.barrio,
                'onesignal_player_id': self.onesignal_player_id,
                'alergias': [alergia.id for alergia in self.alergias],
                'notificaciones': [15],
            }
        )

        self.assertEqual(
            str(response.data['errors'][0]['message']),
            'Clave primaria "15" inválida - objeto no existe.'
        )
