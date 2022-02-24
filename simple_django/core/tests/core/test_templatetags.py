from simple_django.core.templatetags.url_tags import active_url, get_qs


def test_active_url(rf):
    request = rf.get("/")
    current_url = "/"
    active = active_url(request, current_url)
    assert active == "active"

    current_url = "/other"
    active = active_url(request, current_url)
    assert active == ""

    request = rf.get("/other")
    active = active_url(request, current_url)
    assert active == "active"

def test_get_qs(rf):
    request = rf.get("/")
    qs = get_qs(request)
    assert qs == ""

    query = "one=two&three=four"
    request = rf.get(f"/path?{query}")
    qs = get_qs(request)
    assert qs == query + "&"

    qs = get_qs(request, "one")
    assert qs == "three=four&"
