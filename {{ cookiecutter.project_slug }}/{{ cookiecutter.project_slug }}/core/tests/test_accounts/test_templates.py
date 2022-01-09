from unittest.mock import MagicMock

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import SocialApp
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
from django.test import TestCase, RequestFactory
from faker import Faker

User = get_user_model()

fake = Faker()


class AForm(forms.Form):
    val = forms.CharField(required=False)


class AccountsTemplatesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        factory = RequestFactory()
        cls.factory = factory
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user
        request = factory.get("/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        cls.request = request
        site = Site.objects.get_current(request)
        fb = SocialApp.objects.create(
            provider="facebook",
            name="FB",
            client_id="abcd",
            secret="abcd",
        )
        fb.sites.add(site)

        goo = SocialApp.objects.create(
            provider="google", name="G", client_id="abcd", secret="abcd"
        )
        goo.sites.add(site)
        cls.ctx = {"redirect_field_value": "/", "redirect_field_name": "next"}

    def test_account_email_html(self):
        request = self.factory.get("/")
        request.user = self.user
        tmpl = TemplateResponse(request, "account/email.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

        email = EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True, primary=True
        )
        tmpl = TemplateResponse(request, "account/email.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

        email.verified = False
        email.primary = False
        email.save()
        tmpl = TemplateResponse(request, "account/email.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_signup_html(self):
        tmpl = TemplateResponse(self.request, "account/signup.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_login_html(self):
        tmpl = TemplateResponse(self.request, "account/login.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_reset_html(self):
        self.request.user = self.user
        tmpl = TemplateResponse(self.request, "account/password_reset.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_logout_html(self):
        tmpl = TemplateResponse(self.request, "account/logout.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_verified_email_required_html(self):
        tmpl = TemplateResponse(
            self.request, "account/verified_email_required.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_socialaccount_connections_html(self):
        self.request.user = self.user
        form = {"accounts": [MagicMock()]}
        self.ctx["form"] = form
        tmpl = TemplateResponse(
            self.request, "socialaccount/connections.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_reset_from_key_html(self):
        tmpl = TemplateResponse(
            self.request, "account/password_reset_from_key.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

        self.ctx.update({"token_fail": True})
        tmpl = TemplateResponse(
            self.request, "account/password_reset_from_key.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

        form = AForm()
        self.ctx.update({"token_fail": False, "form": form})
        tmpl = TemplateResponse(
            self.request, "account/password_reset_from_key.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_email_confirm_html(self):
        email = EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=False, primary=True
        )
        confirmation = EmailConfirmation.create(
            email_address=email,
        )
        self.ctx.update({"confirmation": confirmation})
        tmpl = TemplateResponse(self.request, "account/email_confirm.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

        tmpl = TemplateResponse(self.request, "account/email_confirm.html")
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_reset_done_html(self):
        self.request.user = self.user
        tmpl = TemplateResponse(
            self.request, "account/password_reset_done.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_socialaccount_authentication_error(self):
        tmpl = TemplateResponse(
            self.request, "socialaccount/authentication_error.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_change(self):
        tmpl = TemplateResponse(self.request, "account/password_change.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_set_html(self):
        tmpl = TemplateResponse(self.request, "account/password_set.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_socialaccount_login_cancelled_html(self):
        tmpl = TemplateResponse(
            self.request, "socialaccount/login_cancelled.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_socialaccount_signup_html(self):
        tmpl = TemplateResponse(self.request, "socialaccount/signup.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_account_inactive_html(self):
        tmpl = TemplateResponse(self.request, "account/account_inactive.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_signup_closed_html(self):
        tmpl = TemplateResponse(self.request, "account/signup_closed.html", self.ctx)
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_password_reset_from_key_done_html(self):
        tmpl = TemplateResponse(
            self.request, "account/password_reset_from_key_done.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_account_verification_sent_html(self):
        tmpl = TemplateResponse(
            self.request, "account/verification_sent.html", self.ctx
        )
        self.assertTrue(tmpl.render().is_rendered)
