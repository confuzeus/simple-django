from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Updating default Django site.")
        site = Site.objects.first()
        site.name = settings.PROJECT_NAME
        site.domain = f"{settings.DOMAIN_NAME}:{settings.PORT_NUMBER}"
        site.save()
        self.stdout.write(self.style.SUCCESS("Success."))
