import django.contrib.auth.models as auth
import django.db.models as models

__all__ = ['User']

class UserManager(auth.BaseUserManager):
    """
    Definition of a custom user manager.  The purpose of this class is
    to change the default behaviour for when a user is created.  In
    particular, the newly created users should not be active unless
    they are a leader, or it was otherwise specified.
    """
    def _create_user(self, username, password, is_staff, is_superuser, **kwargs):
        """
        Creates a new instance of a 'User' with the specified username and password.
        IF the user is not staff, then they are implicitly not active.  This is to
        prevent an issue where CAS login automatically creates a user model whom
        access may want to be prevented.

        :param username: Username for the user
        :param password: Passowrd for the user
        :param is_staff: Boolean to indicate if user is staff
        :param is_superuser: Boolean to indicate if user is a superuser
        :param kwargs: Keyword arguments dictionary
        :return 'User'
        """
        first_year = User.FIRST_YEAR
        position = kwargs.get('position', first_year)
        is_active = is_staff if position == first_year else True
        kwargs['position'] = position
        kwargs['is_active'] = is_active
        kwargs['is_staff'] = is_staff
        kwargs['is_superuser'] = is_superuser
        kwargs['is_admin'] = is_superuser
        kwargs['username'] = username
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **kwargs):
        """
        Creates a new user.  The new user is implicitly not staff or a superuser.

        :param username: Username for the new user
        :param password: Password for the new user
        :param kwargs: Keyword arguments dictionary
        :return 'User'
        """
        return self._create_user(username, password, False, False, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        """
        Creates a new superuser.  The superuser is implicitly staff.

        :param username: Username for the new user
        :param password: Password for the new user
        :param kwargs: Keyword arguments dictionary
        :return 'User'
        """
        return self._create_user(username, password, True, True, **kwargs)

class User(auth.AbstractBaseUser, auth.PermissionsMixin):
    """
    Definition of a User class.  A User class inherits from the
    AbstractBaseUser class provided by the Django Authentication
    Framework.  The main difference between a User and AbstractBaseUser,
    ignoring the additional fields, is that our Users may not have
    passwords; as is the case where they authenticaate via CAS which
    will obviously not forward us the password.  We want to allow this
    type of authentication, as Users should be using CAS to login in
    the majority of cases.
    """
    class Meta:
        permissions = (
            ('can_create_user', 'Can create a new user account.'),
            ('can_signup_user', 'Can signup a new first-year student and assign a team.'),
            ('can_adjust_scores', 'Can adjust the scores for teams.'),
            ('can_post_announcements', 'Can post announcements to the website.'),
            ('can_view_all_users', 'Can view all users.'),
            ('can_view_all_teams', 'Can view all team\'s information.'),
            ('can_edit_team', 'Can edit their own team\'s information.'),
            ('can_edit_all', 'Can edit all information.'),
        )

    # Defines the manager for querying for objects of this model type.
    # We use the the default Django UserManager, as our needs are
    # around the same.
    objects = auth.UserManager()

    # Here we define the different user groups we have.  A user can
    # belong to only one of these groups.
    FIRST_YEAR = 'firstyear'
    PINK_TIE = 'pink'
    HEAD_PINK_TIE = 'headpinktie'
    BLACK_TIE = 'black'
    HEAD_BLACK_TIE = 'headblacktie'
    MEDIA = 'media'
    TEAMSTER = 'teamster'
    DEVISOR = 'devisor'
    TIE_GUARD = 'tieguard'
    MATH_FOC = 'mathfoc'
    ADVISOR = 'advisor'
    ADMIN = 'admin'

    STUDENT_ROLES = (
        (FIRST_YEAR, 'First-Year Student'),
        (PINK_TIE, 'Pink-Tie Leader'),
        (HEAD_PINK_TIE, 'Head Pink-Tie Leader'),
        (BLACK_TIE, 'Black-Tie Leader'),
        (HEAD_BLACK_TIE, 'Head Black-Tie Leader'),
        (MEDIA, 'Media'),
        (TEAMSTER, 'Teamster'),
        (DEVISOR, 'Devisor'),
        (TIE_GUARD, 'Tie Guard'),
        (MATH_FOC, 'MathFOC'),
        (ADVISOR, 'Orientation Advisor'),
        (ADMIN, 'Admin'),
    )

    DOUBLE_DEGREE_CS = 'DDC'
    DOUBLE_DEGREE_MATH = 'DDM'

    PROGRAMS = (
        (DOUBLE_DEGREE_CS, 'Computer Science Double Degree'),
        (DOUBLE_DEGREE_MATH, 'Mathematics Double Degree'),
        ('ITM', 'IT Management'),
        ('MEC', 'Mathematical Economics'),
        ('MPH', 'Mathematical Physics'),
        ('ACS', 'Actuarial Science'),
        ('CPM', 'Computational Mathematics'),
        ('CFM', 'Computing & Financial Management'),
        ('FRM', 'Financial Analysis & Risk Management'),
        ('OPT', 'Mathematical Optimization'),
        ('STT', 'Statistics'),
        ('PRM', 'Pure Mathematics'),
        ('TCH', 'Math Teaching'),
        ('HON', 'Honours Mathematics'),
        ('COS', 'Computer Science'),
        ('MTS', 'Mathematical Studies'),
        ('BIO', 'Bioinformatics'),
        ('MFM', 'Mathematical Finance'),
        ('BUS', 'Business Administration'),
        ('COO', 'Combinatorics & Optimization'),
        ('APM', 'Applied Mathematics'),
        ('SCC', 'Scientific Computation'),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'full_name']

    objects = UserManager()

    # User Model fields
    username = models.CharField(max_length=120, blank=False, unique=True)
    full_name = models.CharField(max_length=120, blank=False)
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    email = models.EmailField(blank=True)

    # These additional fields are optional, but provide some
    # information that we may want to use in the future.
    program = models.CharField(max_length=50, choices=PROGRAMS, blank=True)

    # User Role fields
    position = models.CharField(max_length=50, choices=STUDENT_ROLES, blank=False)

    # Fields required by default for any Django user object
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    @property
    def is_first_year(self):
        """
        Returns 'True' if the user is a first year, otherwise 'False'.

        :return bool
        """
        return (self.position == self.FIRST_YEAR)

    @property
    def is_leader(self):
        """
        Returns 'True' if this user is a leader, otherwise 'False'.

        :return bool
        """
        leader_positions = [self.PINK_TIE, self.HEAD_PINK_TIE, self.BLACK_TIE, self.HEAD_BLACK_TIE]
        return (self.position in leader_positions) or self.is_mod or self.is_foc

    @property
    def is_mod(self):
        """
        Returns 'True' if the user is a MOD, otherwise 'False'.

        :return bool
        """
        return (self.position in [self.MEDIA, self.TEAMSTER, self.DEVISOR, self.TIE_GUARD])

    @property
    def is_foc(self):
        """
        Returns 'True' if the user is a FOC, otherwise 'False'.

        :return bool
        """
        return (self.position == self.MATH_FOC)

    @property
    def quest_id(self):
        """
        Returns the quest identifier for this user.  Alias to 'username'.

        :return string
        """
        return self.username

    @property
    def double_degree(self):
        """
        Returns 'True' if this user is in the Double Degree program, otherwise 'False'.

        :return bool
        """
        if self.program is None:
            return False
        return (self.program in [self.DOUBLE_DEGREE_CS, self.DOUBLE_DEGREE_MATH])

    def get_program_name(self):
        """
        Returns the name of the program this user is in.

        :return string
        """
        names = dict(self.PROGRAMS)
        if self.program is not None:
            return names[self.program]
        return None

    def get_position_name(self):
        """
        Returns the name of the position this user has.

        :return string
        """
        names = dict(self.STUDENT_ROLES)
        return names[self.position]

    def get_short_name(self):
        """
        Short name method for Django.  Returns the first name.

        :return string
        """
        return self.first_name

    def get_full_name(self):
        """
        Full name method for Django.  Returns user's full name.

        :return string
        """
        return self.full_name

    def __str__(self):
        """
        :return string
        """
        return self.full_name

    def __unicode__(self):
        """
        :return string
        """
        return self.__str__()
