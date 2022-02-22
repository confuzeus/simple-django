from urllib.parse import urlparse, parse_qs

from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import resolve_url, redirect


def build_redirect_path(
    request: HttpRequest, login_url: str = settings.LOGIN_URL
) -> tuple:  # pragma: no cover
    """
    Return a path to redirect to the the form:
    scheme://domain/path?{redirect_field_name}={return_path}
    """
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(login_url)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if (not login_scheme or login_scheme == current_scheme) and (
        not login_netloc or login_netloc == current_netloc
    ):
        path = request.get_full_path()
    return path, resolved_login_url


def redirect_next_or_default(path: str, default: str) -> HttpResponseRedirect:
    parsed = urlparse(path)

    if len(parsed.query) > 0:

        qs = parse_qs(parsed.query)

        next_path = qs.get("next")

        if next_path is not None:
            return redirect(next_path[0])
    return redirect(default)
