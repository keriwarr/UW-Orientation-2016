# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=120)),
                ('full_name', models.CharField(max_length=120)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('program', models.CharField(blank=True, max_length=50, choices=[(b'DDC', b'Computer Science Double Degree'), (b'DDM', b'Mathematics Double Degree'), (b'ITM', b'IT Management'), (b'MEC', b'Mathematical Economics'), (b'MPH', b'Mathematical Physics'), (b'ACS', b'Actuarial Science'), (b'CPM', b'Computational Mathematics'), (b'CFM', b'Computing & Financial Management'), (b'FRM', b'Financial Analysis & Risk Management'), (b'OPT', b'Mathematical Optimization'), (b'STT', b'Statistics'), (b'PRM', b'Pure Mathematics'), (b'TCH', b'Math Teaching'), (b'HON', b'Honours Mathematics'), (b'COS', b'Computer Science'), (b'MTS', b'Mathematical Studies'), (b'BIO', b'Bioinformatics'), (b'MFM', b'Mathematical Finance'), (b'BUS', b'Business Administration'), (b'COO', b'Combinatorics & Optimization'), (b'APM', b'Applied Mathematics'), (b'SCC', b'Scientific Computation')])),
                ('position', models.CharField(max_length=50, choices=[(b'firstyear', b'First-Year Student'), (b'pink', b'Pink-Tie Leader'), (b'headpinktie', b'Head Pink-Tie Leader'), (b'black', b'Black-Tie Leader'), (b'headblacktie', b'Head Black-Tie Leader'), (b'media', b'Media'), (b'teamster', b'Teamster'), (b'devisor', b'Devisor'), (b'tieguard', b'Tie Guard'), (b'mathfoc', b'MathFOC'), (b'advisor', b'Orientation Advisor'), (b'admin', b'Admin')])),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('can_create_user', 'Can create a new user account.'), ('can_signup_user', 'Can signup a new first-year student and assign a team.'), ('can_adjust_scores', 'Can adjust the scores for teams.'), ('can_post_announcements', 'Can post announcements to the website.'), ('can_view_all_users', 'Can view all users.'), ('can_view_all_teams', "Can view all team's information."), ('can_edit_team', "Can edit their own team's information."), ('can_edit_all', 'Can edit all information.')),
            },
        ),
    ]
