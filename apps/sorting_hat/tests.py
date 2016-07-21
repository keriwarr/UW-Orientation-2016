import os
import json
from django.test import TestCase

import apps.sorting_hat.models as models
from apps.sorting_hat.sorting_hat import match_students


BASE_DIR = os.path.dirname(__file__)

class SortingHatTestCase(TestCase):
    def setUp(self):
        pass

    def test_simple_01(self):
        # We have 5 members of the Stark family, the algorithm
        # should ensure that they are all not on the same team.
        num_teams = 5
        has_dd_team = False # No DD team
        path = os.path.join(BASE_DIR, 'fixtures', 'simple_01.json')
        with open(path, 'r') as f:
            students = map(lambda d: models.Student(**d), json.loads(f.read()))
            num_students = len(students)
            matchings = match_students(students, num_teams, has_dd_team)
            num_matched_students = 0
            for team in matchings:
                num_matched_students += len(team.students)
                schools = list(s.school for s in team.students)
                self.assertEqual(len(schools), len(set(schools)))
            self.assertEqual(num_students, num_matched_students)

    def test_simple_double_degree_01(self):
        # In this test, we have 3 teams adn 5 members of teh Stark family.
        # We have Double Degree teams, of which teh Stark family has 4
        # members who are Double Degrees so we expect them to be all on one
        # team, and the remaining teams to be unique in schools.
        num_teams = 3
        has_dd_team = True
        path = os.path.join(BASE_DIR, 'fixtures', 'simple_01.json')
        with open(path, 'r') as f:
            students = map(lambda d: models.Student(**d), json.loads(f.read()))
            num_students = len(students)
            has_double_degree_team = False
            matchings = match_students(students, num_teams, has_dd_team)
            num_matched_students = 0
            for team in matchings:
                num_matched_students += len(team.students)
                if team.double_degree:
                    for student in team.students:
                        self.assertEqual(student.is_double_degree(), True)
                    has_double_degree_team = True
                else:
                    schools = list(s.school for s in team.students)
                    self.assertEqual(len(schools), len(set(schools)))
            self.assertEqual(num_students, num_matched_students)
            self.assertEqual(has_double_degree_team, True)

    def test_simple_02(self):
        # In this test, we have 5 students from the same school, 4 from different
        # schools, and 3 teams in total, so we expect that each team has no more
        # than 2 people from the same team and are the same in size.
        num_teams = 3
        has_dd_team = False # No DD team
        path = os.path.join(BASE_DIR, 'fixtures', 'simple_02.json')
        with open(path, 'r') as f:
            students = map(lambda d: models.Student(**d), json.loads(f.read()))
            num_students = len(students)
            matchings = match_students(students, num_teams, has_dd_team)
            num_matched_students = 0
            for team in matchings:
                num_matched_students += len(team.students)
                schools = list(s.school for s in team.students)
                self.assertEqual(len(team.students), num_students / num_teams)
                self.assertTrue(abs(len(schools) - len(set(schools))) <= 1)
            self.assertEqual(num_students, num_matched_students)
