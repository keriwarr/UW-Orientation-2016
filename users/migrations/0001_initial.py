# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import teams.validators
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('teams', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('username', models.CharField(unique=True, max_length=120)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('disabled', models.BooleanField(default=False)),
                ('position', models.CharField(default=b'FY', max_length=2, choices=[(b'F', b'FOC'), (b'M', b'MOD'), (b'HL', b'Head Leader'), (b'L', b'Leader'), (b'FY', b'First Year')])),
                ('photo', models.ImageField(blank=True, upload_to=b'users/photo', validators=[teams.validators.validate_image])),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('team', models.ForeignKey(related_name='members', blank=True, to='teams.Team', null=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
    ]
