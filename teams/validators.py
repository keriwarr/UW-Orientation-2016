from django.core.exceptions import ValidationError


MAX_IMAGE_SIZE = 5
MEGABYTE_MULTIPLIER = 1024 * 1024


def validate_image(image):
    """
    Validates an image for our rules on size limitations.
    We limit image uploads to 5 MB in size.

    @param image
    @returns None
    """
    img_size = image.file.size
    limit = MAX_IMAGE_SIZE * MEGABYTE_MULTIPLIER
    if img_size > limit:
        msg = 'Max file size is {0}MB'.format(MAX_IMAGE_SIZE)
        raise ValidationError(msg)
