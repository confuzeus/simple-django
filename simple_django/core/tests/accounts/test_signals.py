import pytest


@pytest.mark.django_db
def test_user_post_save(fake, django_user_model):
    user = django_user_model.objects.create(
        username=fake.user_name(),
        email=fake.ascii_email())

    assert user.profile is not None
