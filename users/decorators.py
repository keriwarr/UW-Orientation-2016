from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def active_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not (request.user and request.user.is_authenticated() and request.user.is_active):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def require_positions(positions=None):
    if positions is None:
        positions = []
    def _func_wrapper(view_func):
        def _wrapped_view_func(request, *args, **kwargs):
            if not (request.user and request.user.is_authenticated() and request.user.position in positions):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view_func
    return _func_wrapper
