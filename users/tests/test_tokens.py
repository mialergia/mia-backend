from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Faker

from users.tests.factories import UserFactory


@override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
class TestUserCreation(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client_test = APIClient()
        self.password = Faker().password
        self.email = UserFactory(password=self.password).email

    def test_if_try_to_refresh_token_then_access_token_is_returned(self):
        refresh_token = self.client_test.post(
            reverse('rest_login'),
            {
                'email': self.email,
                'password': self.password
            }
        ).data['refresh_token']

        response = self.client_test.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(str(response.data['access']))

    def test_if_try_to_refresh_without_token_then_401_is_returned(self):
        response = self.client_test.post(
            reverse('token_refresh'),
            {
                'refresh': '',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
