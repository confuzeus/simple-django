import pytest
from django.contrib.sites.models import Site
from django.core.management import call_command


@pytest.mark.django_db
def test_init_site(settings, fake):
    site = Site.objects.first()

    settings.PROJECT_NAME = fake.word()
    settings.DOMAIN_NAME = fake.domain_name()
    assert site.name != settings.PROJECT_NAME
    assert site.domain != settings.DOMAIN_NAME

    settings.PORT_NUMBER = 443
    call_command("init_site")

    site.refresh_from_db()
    assert site.name == settings.PROJECT_NAME
    assert site.domain == settings.DOMAIN_NAME

    settings.PORT_NUMBER = 3000
    call_command("init_site")
    site.refresh_from_db()
    assert site.domain == f"{settings.DOMAIN_NAME}:3000"
