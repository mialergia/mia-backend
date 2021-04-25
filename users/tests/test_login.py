from django.test import TestCase, Client, override_settings
from rest_framework import status
from faker import Faker
from django.urls import reverse

from users.tests.factories import UserFactory
from users.models import User
import alergias.strings as strings

LOGIN_URL = reverse('rest_login')


@override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
class TestUserLogin(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client_test = Client()

    def test_if_user_login_correctly(self):
        password = Faker().password
        user = UserFactory(password=password)

        response = self.client_test.post(
            LOGIN_URL,
            {
                'email': user.email,
                'password': password
            }
        )

        response_db = User.objects.first()
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(str(response_data['access_token']))
        self.assertIsNotNone(str(response_data['refresh_token']))
        self.assertEqual(response_data['user']['email'], response_db.email)

    def test_if_user_doesnt_exist_then_should_raise_an_error(self):
        password = Faker().password
        email = Faker().email

        response = self.client_test.post(
            LOGIN_URL,
            {
                'email': email,
                'password': password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['errors'][0]['message']),
            strings.valid_email,
        )
