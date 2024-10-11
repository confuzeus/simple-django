from django.http import HttpResponse
from django.shortcuts import render


def healthcheck(request):  # pragma: no cover
    return HttpResponse("OK")


def toast_messages(request):
    return render(request, "common/toast_messages.html")
