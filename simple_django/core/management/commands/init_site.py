from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Updating default Django site.")
        site = Site.objects.first()
        site.name = settings.PROJECT_NAME
        site_domain = settings.DOMAIN_NAME

        if settings.PORT_NUMBER > 443:
            site_domain += f":{settings.PORT_NUMBER}"

        site.domain = site_domain
        site.save()
        self.stdout.write(self.style.SUCCESS("Success."))
