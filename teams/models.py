import os

from django.db import models
import jsonfield

from teams.roles import *
from teams.validators import validate_image
from users.roles import (FIRST_YEAR, LEADER, HEAD_LEADER)


class TeamCheer(models.Model):
    """
    Represents a Team cheer.
    """
    name = models.CharField(max_length=100, default='')
    text = models.TextField(blank=False)
    profile = models.ForeignKey('TeamProfile', related_name='cheers', blank=False)
    # Fields for keeping track of changes to the model for audit purposes.
    # Changes to the model will record the user who made those changes.
    created_by = models.ForeignKey('users.CustomUser', blank=True, null=True, related_name='+')
    last_edited_by = models.ForeignKey('users.CustomUser', blank=True, null=True, related_name='+')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class TeamProfile(models.Model):
    """
    Profile for a Team.  This contains the information used to display the team in
    the teams profile section of the website.  Leaders on that team may make edits
    to the profile, as well as MODs/FOC
    """
    facebook = models.URLField(blank=True)
    team_video = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    welcome_message = models.TextField(blank=True)
    # Fields for keeping track of changes to the model for audit purposes.
    # Changes to the model will record the user who made those changes.
    last_edited_by = models.ForeignKey('users.CustomUser', blank=True, null=True, related_name='+')

    def __str__(self):
        return 'Team Profile <%s>' % (self.team.name)

    def __unicode__(self):
        return self.__str__()

class Team(models.Model):
    """
    Represents an orientation team.  An orientation team has a score
    in a list of members in that team that are either composed of all
    Black-Ties, MODs, FOC or a combination of leaders and first years.
    """
    TEAM_TYPES = (
        (PINK_TIE, 'Pink Tie'),
        (BLACK_TIE, 'Black Tie'),
        (MOD, 'MOD'),
        (MATHFOC, 'Math FOC'),
    )

    LOGO_IMAGE_PATH = os.path.join('teams', 'logos')
    BANNER_IMAGE_PATH = os.path.join('teams', 'banners')

    name = models.CharField(max_length=256, blank=False)
    type = models.CharField(max_length=2, choices=TEAM_TYPES, default=PINK_TIE)
    score = models.PositiveIntegerField(default=0)
    profile = models.OneToOneField('TeamProfile', blank=True, null=True)
    logo = models.ImageField(upload_to=LOGO_IMAGE_PATH, blank=False, validators=[validate_image])
    banner = models.ImageField(upload_to=BANNER_IMAGE_PATH, blank=True, validators=[validate_image])
    extra_data = jsonfield.JSONField(blank=True)
    double_degree = models.BooleanField(default=False)

    @property
    def is_double_degree(self):
        return self.double_degree

    @property
    def is_first_year_team(self):
        return len(self.first_years) > 0 or self.type == PINK_TIE

    @property
    def first_years(self):
        return self.members.filter(position=FIRST_YEAR)

    @property
    def head_leaders(self):
        return self.members.filter(position=HEAD_LEADER)

    @property
    def leaders(self):
        return self.members.filter(position__in=[HEAD_LEADER, LEADER])

    @property
    def num_members(self):
        return len(self.members)

    def __str__(self):
        team_dict = dict(self.TEAM_TYPES)
        return '%s <%s Team>' % (self.name, team_dict[self.type])

    def __unicode__(self):
        return self.__str__()

def pink_tie_teams():
    """
    Returns all the Pink-Tie teams.
    """
    return Team.objects.filter(type=PINK_TIE).order_by('name')
