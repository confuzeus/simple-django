from allauth.account import forms as allauth_account_forms
from django.contrib.auth import get_user_model

from allcaptcha.mixins import CaptchaFormMixin


class LoginForm(CaptchaFormMixin, allauth_account_forms.LoginForm):
    pass


class ResetPasswordForm(CaptchaFormMixin, allauth_account_forms.ResetPasswordForm):
    pass


class ResetPasswordKeyForm(
    CaptchaFormMixin, allauth_account_forms.ResetPasswordKeyForm
):
    pass


class ChangePasswordForm(CaptchaFormMixin, allauth_account_forms.ChangePasswordForm):
    pass


class SignupForm(CaptchaFormMixin, allauth_account_forms.SignupForm):
    pass
