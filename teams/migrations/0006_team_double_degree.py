# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_teamprofile_facebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='double_degree',
            field=models.BooleanField(default=False),
        ),
    ]
