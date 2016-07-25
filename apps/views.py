import django.contrib.auth.decorators as auth_decorators
import django.views.decorators.http as http_decorators
import decorators as custom_decorators

@http_decorators.require_http_methods(['GET'])
@auth_decorators.login_required
@auth_decorators.permission_required('can_view_all_users')
def users_list(request):
    """
    Lists users.  Can only be viewed by those with the permission
    to view users.

    :param request: 'Request' object
    :return 'Response' object
    """
    pass

@http_decorators.require_http_methods(['GET', 'POST'])
@auth_decorators.login_required
@auth_decorators.permission_required('can_create_user')
def users_create(request):
    """
    View for creating a user model.  Can only be accessed by those
    with the permission to create users.

    :param request: 'Request' object
    :return 'Response' object
    """
    pass

@http_decorators.require_http_methods(['GET', 'POST'])
@auth_decorators.login_required
@custom_decorators.ownership_or_required
def users_update(request, pk):
    """
    View for updating a user model.  Can only be accessed if either the
    currently logged in user is accessing their own user update page,
    or the currently logged in user has the permission to edit all
    information.

    :param request: 'Request' object
    :param pk: Primary key of user to lookup
    :return 'Response' object
    """
    pass

@http_decorators.require_http_methods(['GET', 'POST'])
@auth_decorators.login_required
@custom_decorators.ownership_or_required
def users_delete(request, pk):
    """
    View for deleting a user model.  Can only be accessed if either the
    currently logged in user is accessing their own deletion page,
    or the currently logged int user has the permission to edit all
    information.

    :param request: 'Request' object
    :param pk: Primary key of user to lookup
    :return 'Response' object
    """
    pass

@http_decorators.require_http_methods(['GET'])
@auth_decorators.login_required
@auth_decorators.permission_required('can_view_all_users')
def users_detail(request, pk):
    """
    View for displaying a particular user's information.  Can only be
    accessed by a user who the permission to view all user information.

    :param request: 'Request' object
    :param pk: Primary key of user to lookup
    :return 'Response' object
    """
    pass
