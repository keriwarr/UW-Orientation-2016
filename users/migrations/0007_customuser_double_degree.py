# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150815_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='double_degree',
            field=models.BooleanField(default=False),
        ),
    ]
