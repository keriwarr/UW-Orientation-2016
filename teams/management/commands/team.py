import os
import re
import csv
import sys
import json
import shutil
import collections

from django import db
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.sorting_hat import sorting_hat
from apps.sorting_hat.models import Student
from teams.models import pink_tie_teams, Team
from users.models import CustomUser
from users.roles import HEAD_LEADER, LEADER, MOD, FOC

BASE_DIR = settings.BASE_DIR
LOGO_DIR = 'team_logos'
BANNER_DIR = 'team_banners'

class Command(BaseCommand):
    help = 'Command line utilities for interacting with teams'

    def list_rankings(self, show_score=False):
        team_data = collections.defaultdict(list)
        for team in pink_tie_teams():
            team_data[team.score].append(team)
        od = collections.OrderedDict(sorted(team_data.items()))
        for (rank, teams) in enumerate(od.itervalues(), start=1):
            for team in teams:
                score = ''
                if show_score:
                    score = ' - Score: {0}'.format(team.score)
                self.stdout.write('{0}. {1}{2}'.format(rank, team.name, score))

    def sort_into_teams(self, fname, program_fname):
        """
        Information in the CSV is formatted as:
        FirstName, FirstNamePreferred, Surname, Email, City, Province, Country, Gender, School

        Information in the Program Information CSV is formatted as:
        StudentId, HomeEmail, CampusEmail, Program, LongDescription
        """
        program_information = {}
        if program_fname is not None:
            with open(program_fname, 'rU') as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                student_information = []
                for row in reader:
                    email = row[2]
                    if not '@' in email:
                        continue
                    quest_id = email.split('@')[0]
                    program_information[quest_id] = row[4]

        with open(fname, 'rU') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            student_information = []
            for row in reader:
                student_information.append(row)

            students = []

            for info in student_information:
                if not '@' in info[3]:
                    continue
                quest_id = info[3].split('@')[0]
                program = program_information[quest_id] if quest_id in program_information else None
                student = Student(info[1], info[2], quest_id, info[8], program, info[7])
                students.append(student)

            self.stdout.write('Team Creation Statistics:')

            teams = sorting_hat.match_students(students)
            for (idx, team) in enumerate(teams):
                self.stdout.write('{0}: {1} Men, {2} Women, Total: {3}'.format(
                    idx, len(team.male_students), len(team.female_students), len(team.students)))

            self.stdout.write('\n')
            self.stdout.write('Total Number of Students: {0}\n'.format(sum(map(lambda team: len(team.students), teams))))

            eligible_software_teams = [
                'Animal Cross Product',
                'League of Lemmas',
                'Little Big Parameter',
                'LnKey Kong',
                'Omegaman',
                'Sinesweeper',
                'Super Math Brothers'
            ]
            user_teams = list(team for team in pink_tie_teams() if not team.double_degree)
            user_teams = list(t for t in user_teams if t.name in eligible_software_teams) + \
                         list(t for t in user_teams if t.name not in eligible_software_teams)
            user_teams = list(team for team in pink_tie_teams() if team.double_degree) + user_teams

            while True:
                choice = raw_input('Create Students? [y/n] ')
                if choice.lower() == 'n':
                    break
                elif choice.lower() == 'y':
                    for (idx, team_obj) in enumerate(teams):
                        team = user_teams[idx]
                        try:
                            for student in team_obj.students:
                                create_user(student, team)
                        except db.IntegrityError as e:
                            self.stdout.write('Error in creating user:\n{0}'.format(str(e)))
                            break
                    break

    def load_leaders(self, fname):
        """
        Information in the CSV is formatted as:
        Header:
        Team Number, Team Name, Facebook Group
        Rows:
        Name, Preferred Name, UserID, Position, Program
        """
        with open(fname, 'rU') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            current_team = None
            for row in reader:
                number, name = row[0], row[1]
                if len(number) == 0 or number.lower() == 'name':
                    continue
                elif 'Team' in number:
                    current_team = Team.objects.get(name=name)
                    continue
                elif len(row[2]) == 0:
                    continue
                user = CustomUser.objects.filter(username=row[2])
                if user.count() > 0:
                    user = user.first()
                else:
                    user = CustomUser()
                user.is_active = True
                user.first_name = row[1]
                user.last_name = ''
                user.username = row[2]
                user.school = 'University of Waterloo'
                user.team = current_team
                if 'head' in row[3].lower():
                    user.position = HEAD_LEADER
                elif 'mod' in row[3].lower():
                    user.position = MOD
                elif 'foc' in row[3].lower():
                    user.position = FOC
                else:
                    user.position = LEADER
                sys.stdout.write('Creating {0}leader: {1}\n'.format('head ' if user.position == HEAD_LEADER else '', user))
                user.save()

    def load_teams(self, oweek_dir):
        oweek_dir_path = oweek_dir
        media_path = os.path.join(BASE_DIR, 'media')
        logo_path = os.path.join(BASE_DIR, 'media', Team.LOGO_IMAGE_PATH)
        banner_path = os.path.join(BASE_DIR, 'media', Team.BANNER_IMAGE_PATH)
        paths = [media_path, logo_path, banner_path]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

        if oweek_dir_path[0] != '/':
            oweek_dir_path = os.path.join(BASE_DIR, oweek_dir_path)

        with open(os.path.join(oweek_dir_path, 'teams.json'), 'r') as f:
            team_json = json.loads(f.read())
            for team_data in team_json:
                t, _ = Team.objects.get_or_create(name=team_data['name'])
                t.name = team_data['name']
                t.type = team_data['type'].upper()
                t.double_degree = team_data['double_degree'] if 'double_degree' in team_data else False

                logo = find_image(team_data['short'], oweek_dir_path, LOGO_DIR)
                if logo is not None:
                    f = logo.split('/')[-1]
                    new_path = os.path.join(BASE_DIR, 'media', Team.LOGO_IMAGE_PATH, f)
                    shutil.copy2(logo, new_path)
                    t.logo = new_path.replace(BASE_DIR + '/', '')

                banner = find_image(team_data['short'], oweek_dir_path, BANNER_DIR)
                if banner is not None:
                    f = banner.split('/')[-1]
                    new_path = os.path.join(BASE_DIR, 'media', Team.BANNER_IMAGE_PATH, f)
                    shutil.copy2(banner, new_path)
                    t.banner = new_path.replace(BASE_DIR + '/', '')

                t.save()

    def add_arguments(self, parser):
        parser.add_argument('--ranks', action='store_true', dest='ranks', default=False, help='Output the rankings of the teams')
        parser.add_argument('--scores', action='store_true', dest='show_scores', default=False, help='Display the team scores')
        parser.add_argument('--sort', dest='sort', default=None, metavar='file', help='Pass a CSV of the student information')
        parser.add_argument('--load', dest='dir', default=None, help='Load teams from the oweek-dir')
        parser.add_argument('--program_information', dest='program_information', default=None, metavar='file', help='Pass a CSV of student program information')
        parser.add_argument('--leaders', dest='leaders', default=None, metavar='file', help='Pass a CSV of the leader information')

    def handle(self, *args, **options):
        if options.get('ranks', False) is True:
            self.list_rankings(options.get('show_scores', False))
        elif options.get('sort', None) is not None:
            self.sort_into_teams(options.get('sort', None), options.get('program_information', None))
        elif options.get('dir', None) is not None:
            self.load_teams(options.get('dir', None))
        elif options.get('leaders', None) is not None:
            self.load_leaders(options.get('leaders', None))

def create_user(student, team):
    sys.stdout.write('Creating user: %s %s <%s>\n' % (student.first_name, student.last_name, student.quest_id))
    user = CustomUser.objects.filter(username=student.quest_id)
    if user.count() > 0:
        user = user.first()
    else:
        user = CustomUser()
    user.is_active = True
    user.first_name = student.first_name
    user.last_name = student.last_name
    user.username = student.quest_id
    user.school = student.school
    if student.program is not None:
        user.program = student.program
    user.double_degree = student.is_double_degree()
    user.team = team
    user.save()

def list_dir_files(path):
    return (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))

def find_image(short_name, base_dir, directory):
    for f in list_dir_files(os.path.join(base_dir, directory)):
        if short_name.lower() in f.lower():
            return os.path.join(base_dir, directory, f)
    return None
