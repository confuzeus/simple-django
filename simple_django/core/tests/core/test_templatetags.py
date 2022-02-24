from simple_django.core.templatetags.url_tags import active_url, get_qs
from simple_django.core.templatetags.useful_filters import is_number, is_string


def test_active_url(rf):
    request = rf.get("/")
    test_url = "/"
    active = active_url(request, test_url)
    assert active == "active"

    test_url = "/other"
    active = active_url(request, test_url)
    assert active == ""

    request = rf.get("/other")
    active = active_url(request, test_url)
    assert active == "active"

    test_url = "/"
    active = active_url(request, test_url)
    assert active == ""


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

    qs = get_qs(request, "five")
    assert qs == query + "&"


def test_is_number():

    assert is_number(1) is True
    assert is_number("1") is False
    assert is_number(True) is False
    assert is_number(1.0) is True
    assert is_number({}) is False


def test_is_string():

    assert is_string("") is True
    assert is_string(1) is False
    assert is_string(False) is False
    assert is_string({}) is False
    assert is_string(1.0) is False
