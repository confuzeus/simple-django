from allauth.account import forms as allauth_account_forms
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.core.mixins.form_mixins import HcaptchaFormMixin

User = get_user_model()


class LoginForm(HcaptchaFormMixin, allauth_account_forms.LoginForm):
    pass


class ResetPasswordForm(HcaptchaFormMixin, allauth_account_forms.ResetPasswordForm):
    pass


class ResetPasswordKeyForm(
    HcaptchaFormMixin, allauth_account_forms.ResetPasswordKeyForm
):
    pass


class ChangePasswordForm(HcaptchaFormMixin, allauth_account_forms.ChangePasswordForm):
    pass


class SignupForm(HcaptchaFormMixin, allauth_account_forms.SignupForm):
    pass
