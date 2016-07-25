# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import teams.validators
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150726_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, upload_to=users.models.upload_user_photo, validators=[teams.validators.validate_image]),
        ),
    ]
