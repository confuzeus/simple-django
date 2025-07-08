import factory

from src.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")

    @factory.post_generation
    def password(obj: User, create: bool, extracted: str, **kwargs):
        password_plaintext = (
            extracted
            if extracted
            else factory.Faker("password").evaluate(
                None, None, extra={"locale": "en_US"}
            )
        )

        obj.set_password(password_plaintext)
