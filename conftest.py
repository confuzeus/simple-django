import pytest
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.http import HttpRequest
from faker import Faker

User = get_user_model()

@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def site(db) -> Site:
    site = Site.objects.first()

    if not site:
        site = Site.objects.create(name=fake.word(), domain=fake.domain_name())

    return


@pytest.fixture
def admin_request(admin_user, rf) -> HttpRequest:
    request = rf.get("/")
    request.user = admin_user
    return


@pytest.fixture
def user(db, fake, django_user_model) -> User:
    return django_user_model.objects.create(username=fake.user_name(), email=fake.ascii_email())
