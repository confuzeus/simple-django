from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django_htmx.http import reswap, trigger_client_event


def healthcheck(request):  # pragma: no cover
    return HttpResponse("OK")


def toast_messages(request):
    storage = messages.get_messages(request)
    if len(storage) == 0:
        response = HttpResponse()
        return reswap(response, "none")

    response = render(request, "common/toast_messages.html")
    return trigger_client_event(response, "initToasts")
