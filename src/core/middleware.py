from django.contrib import messages
from django_htmx.http import trigger_client_event


def toaster_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        storage = messages.get_messages(request)
        if len(storage) > 0:
            response = trigger_client_event(response, "toasts:fetch", after="settle")

        return response

    return middleware
