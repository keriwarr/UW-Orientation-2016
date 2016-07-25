import os
import time

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

from teams.models import Team
from teams.validators import validate_image
from users.roles import *
from users.programs import PROGRAMS


def upload_user_photo(instance, fname):
    """
    Files will be uploaded to MEDIA_ROOT/users/photo/TIMESTAMP-USERID.EXT
    """
    root_dir = CustomUser.USER_PHOTO_PATH
    ext = fname.split(os.path.sep)[-1]
    output_fname = '{}-{}.{}'.format(time.time(), instance.id, ext)
    return os.path.join(root_dir, output_fname)

class CustomUserManager(UserManager):
    def create_superuser(self, username, password, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        email = None
        if 'email' in kwargs:
            email = kwargs['email']
            del kwargs['email']
        return self._create_user(username, email, password, **kwargs)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    # Field to use for as the unique identifier
    USERNAME_FIELD = 'username'

    # Specify the roles that the user may have (e.g. leader)
    ROLE_CHOICES = (
        (FOC, 'FOC'),
        (MOD, 'MOD'),
        (HEAD_LEADER, 'Head Leader'),
        (LEADER, 'Leader'),
        (FIRST_YEAR, 'First Year'),
    )

    # Specifies the page for where the user photo uploads will be stored
    USER_PHOTO_PATH = os.path.join('users', 'photo')

    # Specifies the user manager
    objects = CustomUserManager()

    # User model fields
    first_name = models.CharField(max_length=120, default='')
    last_name = models.CharField(max_length=120, default='')
    school = models.CharField(max_length=120, blank=True)
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True)
    disabled = models.BooleanField(default=False)
    team = models.ForeignKey(Team, related_name='members', blank=True, null=True)
    position = models.CharField(max_length=2, choices=ROLE_CHOICES, default=FIRST_YEAR)
    program = models.CharField(max_length=3, choices=PROGRAMS, blank=True)
    photo = models.ImageField(upload_to=USER_PHOTO_PATH, blank=True, validators=[validate_image])
    double_degree = models.BooleanField(default=False)

    # Fields required by default for any user object
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    @property
    def is_first_year(self):
        return self.position == FIRST_YEAR

    @property
    def is_leader(self):
        return self.position != FIRST_YEAR

    @property
    def is_mod(self):
        return self.position in [FOC, MOD]

    @property
    def position_name(self):
        positions = dict(CustomUser.ROLE_CHOICES)
        return positions[self.position]

    def get_full_name(self):
        if self.team is not None:
            return '{0} - {1} <Team {2}>'.format(self.username, self.get_short_name(), self.team.name)
        return '{0} - {1} <No Team>'.format(self.username, self.get_short_name())

    def get_short_name(self):
        if len(self.first_name) == 0:
            return self.username
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()
