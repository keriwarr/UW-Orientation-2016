# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0002_team_extra_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamCheer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_edited_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_video', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('welcome_message', models.TextField(blank=True)),
                ('last_edited_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='teamcheer',
            name='profile',
            field=models.ForeignKey(related_name='cheers', to='teams.TeamProfile'),
        ),
        migrations.AddField(
            model_name='team',
            name='profile',
            field=models.OneToOneField(null=True, blank=True, to='teams.TeamProfile'),
        ),
    ]
