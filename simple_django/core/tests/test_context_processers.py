from django.test import RequestFactory, SimpleTestCase

from simple_django.core.context_processors import site_data


class ContextProcessorsTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(ContextProcessorsTests, cls).setUpClass()
        cls.rf = RequestFactory()

    def test_site_data(self):
        request = self.rf.get("/")

        ctx = site_data(request)
        self.assertIn("django_debug", ctx.keys())

        with self.settings(DEBUG=True):
            ctx = site_data(request)
            self.assertTrue(ctx["django_debug"])

        with self.settings(DEBUG=False):
            ctx = site_data(request)
            self.assertFalse(ctx["django_debug"])
