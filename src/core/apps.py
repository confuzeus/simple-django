from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "src.core"
    verbose_name = _("Core")

    def ready(self):
        try:
            from .signals import accounts  # noqa F401
        except ImportError:
            pass
