from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from simple_django.accounts.forms import UserDeleteForm, UserForm


@login_required
def update_user(request):
    form = None
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
        else:
            messages.error(request, "Unable to update your profile.")
    if form is None:
        form = UserForm(instance=request.user)
    return TemplateResponse(request, "accounts/update_user.html", {"form": form})


@login_required
def delete_user(request):
    form = None
    if request.method == "POST":
        form = UserDeleteForm(request.POST, user=request.user)

        if form.is_valid():
            user = get_user_model().objects.get(pk=request.user.id)
            user.delete()
            logout(request)
            messages.info(request, "Your account has been deleted!")
            return redirect("/")
    if form is None:
        form = UserDeleteForm(user=request.user)
    return TemplateResponse(
        request, "accounts/confirm_delete_user.html", {"form": form}
    )
