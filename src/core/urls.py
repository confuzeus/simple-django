from django.urls import path

from src.core import views

app_name = "core"

urlpatterns = [path("toasts/", views.toast_messages, name="toast-messages")]
