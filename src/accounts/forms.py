from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name"]


class UserDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_password(self):
        result = self.user.check_password(self.cleaned_data["password"])
        if result is False:
            raise ValidationError("Wrong password.")
        return self.cleaned_data["password"]
