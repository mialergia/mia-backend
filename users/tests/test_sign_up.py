from django.test import TestCase, Client
from rest_framework import status

from users.models import User
from users.tests.factories import UserFactory
import alergias.strings as strings


class TestUserCreation(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client_test = Client()

    def _create_account_request(self, new_email, pass1, pass2):
        return self.client_test.post(
            '/api/v1/users/sign-up/',
            {
                'email': new_email,
                'password1': pass1,
                'password2': pass2,
            }
        )

    def test_if_email_and_passwords_are_correct_then_must_create_correctly(self):
        user = UserFactory.build()

        response = self._create_account_request(
            user.email,
            user.password,
            user.password,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(len(mail.outbox), 1)  # Test that one message was sent
        # self.assertEqual(mail.outbox[0].to, [user.email])

    def test_if_email_already_exists_then_can_not_be_created(self):
        user = UserFactory.build()
        User.objects.create(email=user.email)

        response = self._create_account_request(
            user.email,
            user.password,
            user.password,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            str(response.data['errors'][0]['message']),
            strings.email_already_created,
        )

    def test_if_the_passwords_do_not_match_then_can_not_be_created(self):
        user = UserFactory.build()

        response = self._create_account_request(
            user.email,
            user.password,
            f"{user.password}error",
        )

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(response.data['errors'][0]['message']),
            strings.passwords_should_match,
        )
