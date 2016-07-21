# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20150725_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcheer',
            name='name',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
