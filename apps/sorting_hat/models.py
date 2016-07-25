class Student(object):
    def __init__(self, first_name, last_name, quest_id, school, program, gender='M', *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.quest_id = quest_id
        self.school = school
        self.program = program
        self.gender = gender

    def is_double_degree(self):
        patts = [
            'double degree',
            'dd'
        ]
        if self.program is None:
            return False
        return any(patt in self.program.lower() for patt in patts)

    def is_software_engineer(self):
        patts = [
            'software',
            'engineering'
        ]
        if self.program is None:
            return False
        return any(patt in self.program.lower() for patt in patts)

class SortingTeam(object):
    def __init__(self, double_degree=False, *args, **kwargs):
        self.double_degree = double_degree
        self.students = []

    @property
    def male_students(self):
        return list(s for s in self.students if s.gender == 'M')

    @property
    def female_students(self):
        return list(s for s in self.students if not s.gender == 'M')

    @property
    def ratio(self):
        return len(self.male_students()) / (len(self.female_students()) * 1.0)

    def has_first_name(self, first_name):
        return first_name in list(s.first_name for s in self.students)

    def add(self, student):
        if not self.students:
            self.students = []
        self.students.append(student)
