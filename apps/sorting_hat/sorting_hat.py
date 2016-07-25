import sys

from apps.sorting_hat.models import Student, SortingTeam
from teams.models import pink_tie_teams as list_pink_tie_teams
from users.roles import FIRST_YEAR

def compare_student_teams(team1, team2, desired_gender):
    if len(team1.students) < len(team2.students):
        return -1
    elif len(team1.students) > len(team2.students):
        return 1
    elif desired_gender == 'M':
        if len(team1.male_students) > len(team2.male_students):
            return 1
        return -1
    elif desired_gender == 'F':
        if len(team1.female_students) > len(team2.female_students):
            return 1
        return -1
    return 0

def match_students(students, num_teams=12, has_dd_team=True):
    """
    Bucket method for taking sets of students and putting them into teams.
    Returns the team assignments which can then be used to create the user
    models.

    @param students List of Student objects.
    @param num_teams The number of teams to create
    @param has_dd_team Boolean indicating if there is a Double-Degree team
    @returns List of SortingTeams
    """
    prepended_teams = []
    if has_dd_team:
        # If we have a Double Degree team, we want to grab all the students that
        # are the Double Degree program to funnel them into that team.
        double_degree = filter(lambda s: s.is_double_degree(), students)
        students = filter(lambda s: s not in double_degree, students)
        double_degree_team = SortingTeam(double_degree=True)
        double_degree_team.students = double_degree
        # Assign to prepended and decrement the count so that we'll add the
        # Double Degree team at the end.
        prepended_teams = [double_degree_team]
        num_teams = num_teams - 1
    teams = list(SortingTeam() for _ in range(num_teams))
    # This is a hack, but Software Engineering wants all their students into
    # a small number of teams that is managable for them.  Right now that is hardcoded
    # as four.
    num_software_team_split = 6
    software_engineers = filter(lambda s: s.is_software_engineer(), students)
    software_teams = teams[:num_software_team_split]
    for software_engineer in software_engineers:
        comparison = lambda t1, t2: compare_student_teams(t1, t2, software_engineer.gender)
        sorted_teams = sorted(software_teams, cmp=comparison)
        min_indices = list(software_teams.index(t) for t in sorted_teams)
        min_indice = min_indices[0]
        team_indice = min_indice
        while True:
            if not teams[team_indice].has_first_name(software_engineer.first_name):
                break
            if len(min_indices) == 0:
                break
            team_indice = min_indices.pop(0)
        if len(min_indices) == 0:
            team_indice = min_indice
        software_teams[team_indice].add(software_engineer)
    students = filter(lambda s: s not in software_engineers, students)
    # First group the students by their schools.  We'll use this as a metric for
    # splitting them up so that they are with new people.
    schools = {}
    for student in students:
        if student.school not in schools:
            schools[student.school] = []
        schools[student.school].append(student)
    # Now that we have the schools, we want to divy them up equally between the
    # different groups whiel minimizing the occurrence of duplicate first names
    # among the first year students.
    for (school, students) in schools.iteritems():
        for student in students:
            sorted_teams = sorted(teams, cmp=lambda t1, t2: compare_student_teams(t1, t2, student.gender))
            min_indices = list(teams.index(t) for t in sorted_teams)
            min_indice = min_indices[0]
            team_indice = min_indice
            while len(min_indices) > 0:
                if not teams[team_indice].has_first_name(student.first_name):
                    break
                team_indice = min_indices.pop(0)
            if len(min_indices) == 0:
                team_indice = min_indice
            teams[team_indice].add(student)
    return prepended_teams + teams

def find_pink_tie_team_assignment(student_data):
    """
    Finds the appropriate Pink tie team for a new student.

    @param student_data The new student data
    @returns The team to assign them to
    """
    student = Student(**student_data)
    teams = list_pink_tie_teams()
    double_degree_team = next((team for team in teams if team.double_degree), None)
    if student.is_double_degree() and double_degree_team is not None:
        # If the student is a Double-Degree student and we have a Double Degree
        # team, then we can terminate prematurely and return that team.
        return double_degree_team
    # Assign the student to the team that currently has the least members.
    # This is dumber than the above method because we can't guarantee equality
    # in numbers at this point.
    teams = list(team for team in teams if not team.double_degree)
    sorted_teams = sorted(teams, key=lambda t: len(t.first_years))
    minimum_members = len(sorted_teams[0].first_years)
    filtered_teams = filter(lambda t: len(t.first_years) == minimum_members, sorted_teams)
    if len(filtered_teams) == 1:
        return filtered_teams[0]
    # In the event of a tie in the number of members on a team, we choose the one that
    # minimizes the cost.
    first_name = student.first_name
    school = student.school
    min_cost_index, min_team_cost = 0, sys.maxint
    for (index, team) in enumerate(filtered_teams):
        num_with_same_first_name = len(team.members.filter(first_name=first_name))
        num_with_same_school = len(team.members.filter(school=school))
        cost = num_with_same_first_name + num_with_same_school
        if cost < min_team_cost:
            min_team_cost = cost
            min_cost_index = index
    return filtered_teams[min_cost_index]
