from django.urls import path

from simple_django.core import views

app_name = "core"

urlpatterns = [path("toasts/", views.toast_messages, name="toast-messages")]
