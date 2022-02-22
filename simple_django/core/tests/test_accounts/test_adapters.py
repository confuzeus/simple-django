from unittest.mock import Mock

from django.conf import settings
from django.test import RequestFactory, TestCase

from simple_django.core import accounts_adapters as adapters


class AdaptersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    def test_account_adapter(self):

        request = self.factory.get("/")

        adapter = adapters.AccountAdapter()

        signup_open = adapter.is_open_for_signup(request)

        self.assertEqual(signup_open, settings.ACCOUNT_ALLOW_REGISTRATION)

    def test_social_account_adapter(self):
        request = self.factory.get("/")

        adapter = adapters.SocialAccountAdapter()

        signup_open = adapter.is_open_for_signup(request, Mock())

        self.assertEqual(signup_open, settings.ACCOUNT_ALLOW_REGISTRATION)
