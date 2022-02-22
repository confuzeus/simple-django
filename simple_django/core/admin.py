from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from simple_django.core.models import User, UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.register(User, UserAdmin)
