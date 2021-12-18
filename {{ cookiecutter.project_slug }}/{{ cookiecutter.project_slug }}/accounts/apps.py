from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.accounts"
    verbose_name = _("Accounts")

    def ready(self):
        try:
            from . import signals  # noqa F401
        except ImportError:
            pass
