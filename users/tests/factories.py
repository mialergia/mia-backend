from factory import django, Faker, post_generation
from typing import Any, Sequence

from users.models import User


class UserFactory(django.DjangoModelFactory):
    email = Faker('email')

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                'password'
            ).generate(extra_kwargs={})
        )

        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ['email']
