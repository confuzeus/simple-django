from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from simple_django.accounts.forms import UserForm


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
