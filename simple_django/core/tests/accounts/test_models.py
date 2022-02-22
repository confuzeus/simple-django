def test_user_profile_str(user):
    assert str(user.profile) == f"{user.email}'s profile."
