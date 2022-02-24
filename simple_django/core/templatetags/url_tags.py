import re
from typing import Optional

from django import template
from django.http import HttpRequest, QueryDict
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.filter()
def active_url(request: HttpRequest, url: str) -> str:
    """Output the active css class if the current url matches the passed url."""
    if url == "/":
        if request.path == "/":
            return "active"
        else:
            return ""

    try:
        pattern = f"^{reverse(url)}$"
    except NoReverseMatch:
        pattern = url

    return "active" if re.search(pattern, request.path) else ""


@register.simple_tag()
def get_qs(request: HttpRequest, exclude: Optional[str] = None) -> str:
    """Return existing querystring, optionally excluding a specific one."""
    query_dict: QueryDict = request.GET.copy()

    if exclude:

        if exclude in query_dict:
            del query_dict[exclude]

    if len(query_dict.keys()) > 0:
        qs: str = query_dict.urlencode() + "&"
    else:
        qs = ""
    return qs
