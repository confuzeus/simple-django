import unittest.mock
from django.test import TestCase
from django import forms

from {{ cookiecutter.project_slug }}.core.mixins import form_mixins


class HCaptchaForm(form_mixins.HcaptchaFormMixin, forms.Form):
    pass


class MixinsTests(TestCase):
    def test_hcaptcha_form_mixin(self):
        # Must be invalid if no captcha_response passed
        form = HCaptchaForm()
        self.assertFalse(form.is_valid())

        # Should be valid only if API returns True
        with unittest.mock.patch.object(form_mixins.Captcha, "captcha_success") as mock:
            mock.return_value = True
            form = HCaptchaForm({"captcha_response": "test"})
            self.assertTrue(form.is_valid())

            mock.return_value = False
            form = HCaptchaForm({"captcha_response": "test"})
            self.assertFalse(form.is_valid())
