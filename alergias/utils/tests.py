from faker import Faker
from django.contrib.gis.geos import Point
from faker.providers import geo
from rest_framework import status
import random

from users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(geo)


def get_random_coordinate():
    coordinates = fake.latlng()
    return Point(float(coordinates[1]), float(coordinates[0]))


def get_random_choices(choices, amount):
    random_choices = []

    i = 0
    while (i < amount and i < len(choices)):
        i += 1
        rest_of_choices = [choice for choice in choices if choice not in random_choices]
        random_choice = random.choice(rest_of_choices)
        random_choices.append(random_choice)

    return random_choices


def test_unauthorized_call(self, call_endpoint, *args):
    self.client_test.logout()
    response = call_endpoint()
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    if args:
        user2 = UserFactory()
        self.client_test.force_authenticate(user2)
        response = call_endpoint()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)
