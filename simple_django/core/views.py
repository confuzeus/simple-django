from django.http import HttpResponse


def healthcheck(request):  # pragma: no cover
    return HttpResponse("OK")
