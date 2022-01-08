from django.conf import settings


def site_data(request):
    return {
        "django_debug": settings.DEBUG,
        "allow_registration": settings.ACCOUNT_ALLOW_REGISTRATION,
    }
