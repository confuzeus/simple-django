from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

User = get_user_model()

fake = Faker()


class AccountsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        user.profile.country = "MU"
        user.profile.save()
        cls.user = user

    def _assert_redirected_to_login(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.split("?")[0], reverse_lazy(settings.LOGIN_URL))
