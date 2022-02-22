from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

from simple_django.core.utils.urls import build_redirect_path


def group_required(
    view_id: str, login_url=settings.LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME
):
    """
    Restrict access to users in certain groups.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            path, resolved_login_url = build_redirect_path(request, login_url=login_url)

            if request.user.is_authenticated:

                user_membership_group_name = settings.MEMBERSHIP_GROUPS[
                    request.user.membership_code
                ]["group_name"]

                allowed_groups = settings.VIEW_PERMISSION_GROUPS[view_id]

                if not (user_membership_group_name in allowed_groups):
                    path, resolved_login_url = build_redirect_path(
                        request, login_url=settings.UPGRADE_URL
                    )
                    return redirect_to_login(
                        path, resolved_login_url, redirect_field_name
                    )

                return view_func(request, *args, **kwargs)

            return redirect_to_login(path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator
