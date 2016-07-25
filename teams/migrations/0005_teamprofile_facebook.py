# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_teamcheer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofile',
            name='facebook',
            field=models.URLField(blank=True),
        ),
    ]
