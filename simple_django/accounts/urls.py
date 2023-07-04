from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("update-user/", views.update_user, name="update-user"),
    path("delete-user/", views.delete_user, name="delete-user"),
]
