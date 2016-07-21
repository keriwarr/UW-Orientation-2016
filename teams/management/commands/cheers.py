import os
import yaml

from django.core.management.base import BaseCommand
from django.conf import settings

from teams.models import Team, TeamProfile, TeamCheer


class Command(BaseCommand):
    help = 'Populates teams with their cheers'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1, type=str)

    def handle(self, *args, **options):
        fname = options['file'][0]
        cheers = {}

        with open(fname, 'r') as stream:
            cheers = yaml.load(stream)

        for team in Team.objects.all():
            if team.profile is None:
                profile = TeamProfile()
                profile.save()
                team.profile = profile
                team.save()

            for cheer in cheers:
                cheer_obj = None
                name = cheer['name']

                if team.profile.cheers.filter(name=name).count() > 0:
                    cheer_obj = team.profile.cheers.filter(name=name)[0]
                else:
                    cheer_obj = TeamCheer()
                    cheer_obj.name = name

                cheer_obj.text = cheer['text']
                cheer_obj.profile = team.profile
                cheer_obj.save()
