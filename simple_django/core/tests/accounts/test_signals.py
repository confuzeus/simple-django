def test_user_post_save(db, fake, user_model):
    user = user_model.objects.create(
        username=fake.user_name(),
        email=fake.ascii_email())

    assert user.profile is not None
