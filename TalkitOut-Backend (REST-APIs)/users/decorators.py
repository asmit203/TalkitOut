# decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.profile.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
