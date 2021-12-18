from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.core"
    verbose_name = _("Core")

    def ready(self):
        try:
            from . import signals  # noqa F401
        except ImportError:
            pass