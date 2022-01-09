from django.test import TestCase, RequestFactory
from django.conf import settings

from {{ cookiecutter.project_slug }}.core import context_processors


class ContextProcessorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    def test_context_processors(self):
        request = self.factory.get("/")

        ctx = context_processors.site_data(request)

        # Django debug
        # ------------

        django_debug = ctx.get("django_debug")

        # Must be not None
        self.assertIsNotNone(django_debug)

        # Must be same as in settings
        self.assertEqual(django_debug, settings.DEBUG)

        # Site key
        # --------

        captcha_site_key = ctx.get("captcha_site_key")

        # Must be none None
        self.assertIsNotNone(captcha_site_key)

        # Must be same as in settings
        self.assertEqual(captcha_site_key, settings.CAPTCHA_SITE_KEY)
