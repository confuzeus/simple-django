from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from src.accounts.models import User


class UserAdmin(AuthUserAdmin):
    pass


admin.site.register(User, UserAdmin)
