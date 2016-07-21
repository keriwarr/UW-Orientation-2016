# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import teams.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(default=b'PT', max_length=2, choices=[(b'PT', b'Pink Tie'), (b'BT', b'Black Tie'), (b'TG', b'Tie Guard'), (b'TS', b'Teamster'), (b'MF', b'Math FOC'), (b'MD', b'Media'), (b'DV', b'Devisors')])),
                ('score', models.PositiveIntegerField(default=0)),
                ('logo', models.ImageField(upload_to=b'teams/logos', validators=[teams.validators.validate_image])),
                ('banner', models.ImageField(blank=True, upload_to=b'teams/banners', validators=[teams.validators.validate_image])),
            ],
        ),
    ]
