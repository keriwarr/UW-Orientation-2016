from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from users.models import CustomUser


def validate_image(image):
    w, h = get_image_dimensions(image)
    if abs(w - h) >= settings.MAX_IMAGE_SIZE_DIFFERENCE:
        raise ValidationError('Image dimensions must be within %spx of each other' % settings.MAX_IMAGE_SIZE_DIFFERENCE)

    sz = image._size
    megabyte_limit = settings.MAX_IMAGE_SIZE
    bytes_per_megabyte = 1024
    normalized_limit = megabyte_limit * bytes_per_megabyte * bytes_per_megabyte
    if sz > normalized_limit:
        raise ValidationError('Max image size is %sMB' % megabyte_limit)

    content_type = image.content_type.split('/')[-1].lower()
    valid_content_types = ['png', 'jpg', 'jpeg']
    if content_type not in valid_content_types:
        raise ValidationError('Image must be one of: %s' % ', '.join(valid_content_types))

    return None

def login_response_callback(tree):
    """
    Handles the response from a CAS login authentication.  Here
    we create the user provided they don't exist, otherwise log
    in the user.  When a user is first created, we mark them
    as disabled, they must contact a administrator to gain
    access to the Orientation website as a user.

    @param tree ElementTree object.
    @returns None
    """
    username = tree[0][0].text
    email = '{}@uwaterloo.ca'.format(username)

    user, user_created = CustomUser.objects.get_or_create(username=username)

    if user_created:
        user.is_active = False
        user.email = email
        user.save()
