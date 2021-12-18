import unittest.mock
from unittest.mock import MagicMock
from django.test import TestCase

from {{ cookiecutter.project_slug }}.core.utils import captcha as captcha_util
from {{ cookiecutter.project_slug }}.core.utils.urls import redirect_next_or_default



class UtilsTests(TestCase):
    def test_captcha(self):

        h_captcha = captcha_util.Captcha(captcha_util.Captcha.H_CAPTCHA)
        self.assertEqual(h_captcha.provider_url, captcha_util.Captcha.H_CAPTCHA_URL)

        with self.assertRaises(NotImplementedError):
            captcha_util.Captcha(captcha_util.Captcha.RECAPTCHA)

        with unittest.mock.patch.object(captcha_util, "requests") as mock:
            response = MagicMock()
            mock.post.return_value = response

            response.status_code = 200
            response.json.return_value = {"success": True}

            self.assertTrue(h_captcha.captcha_success("abcd"))

            mock.post.side_effect = Exception()
            self.assertFalse(h_captcha.captcha_success("abcd"))

            mock.post.side_effect = None

            response.json.side_effect = Exception()
            self.assertFalse(h_captcha.captcha_success("abcd"))

            response.json.side_effect = None

            response.status_code = 400
            self.assertFalse(h_captcha.captcha_success("abcd"))

    def test_urls(self):
        response = redirect_next_or_default(path="/home/", default="/abcd/")
        self.assertEqual(response.url, "/abcd/")

        response = redirect_next_or_default(
            path="/home/?next=/place/", default="/abcd/"
        )
        self.assertEqual(response.url, "/place/")

        response = redirect_next_or_default(path="/home/?one=/place/", default="/abcd/")
        self.assertEqual(response.url, "/abcd/")
