from django.http import HttpResponseForbidden

def ownership_or_required(fn):
    """
    Decorator that enforces that the user either has the permission
    'can_edit_all' to bypass ownership of the particular user model.

    :param fn: view function
    :return function
    """
    def wrap(request, pk, *args, **kwargs):
        """
        Wrapper for the view function.

        :param request: 'Request' object
        :param pk: Primary key for 'User' model
        :param args: Variable arguments list
        :param kwargs: Keywords argument dictionary
        :return 'Response' object
        """
        user = request.user
        if user is not None:
            if user.has_permission('can_edit_all') or pk == user.pk:
                return fn(request, pk, *args, **kwargs)
        return HttpResponseForbidden()

    return wrap
