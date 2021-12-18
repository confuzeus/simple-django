from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from {{ cookiecutter.project_slug }}.core.utils.captcha import Captcha


class HcaptchaFormMixin:
    def __init__(self, *args, **kwargs):
        super(HcaptchaFormMixin, self).__init__(*args, **kwargs)
        self.fields["captcha_response"] = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        captcha_response = self.cleaned_data.get("captcha_response")
        hcaptcha = Captcha(Captcha.H_CAPTCHA)
        success = hcaptcha.captcha_success(captcha_response)
        if not success:
            raise ValidationError(_("Anti spam verification failed. Please try again."))
        return self.cleaned_data
