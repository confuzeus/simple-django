from django.test import TestCase

from simple_django.core.utils.urls import redirect_next_or_default


class TestUtils(TestCase):
    def test_urls(self):
        response = redirect_next_or_default(path="/home/", default="/abcd/")
        self.assertEqual(response.url, "/abcd/")

        response = redirect_next_or_default(
            path="/home/?next=/place/", default="/abcd/"
        )
        self.assertEqual(response.url, "/place/")

        response = redirect_next_or_default(path="/home/?one=/place/", default="/abcd/")
        self.assertEqual(response.url, "/abcd/")
