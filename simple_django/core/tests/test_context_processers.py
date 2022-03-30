from simple_django.core.context_processors import site_data


def test_site_data(rf, settings):
    request = rf.get("/")

    ctx = site_data(request)
    assert "django_debug" in ctx.keys()

    assert ctx["django_debug"] is settings.DEBUG
