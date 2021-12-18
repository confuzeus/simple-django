from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")

    def test_user_profile(self):
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        self.assertFalse(user.profile.is_complete)
