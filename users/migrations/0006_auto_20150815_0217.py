# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import teams.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150806_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='program',
            field=models.CharField(blank=True, max_length=3, choices=[(b'DDC', b'Computer Science Double Degree'), (b'DDM', b'Mathematics Double Degree'), (b'ITM', b'IT Management'), (b'MEC', b'Mathematical Economics'), (b'MPH', b'Mathematical Physics'), (b'ACS', b'Actuarial Science'), (b'CPM', b'Computational Mathematics'), (b'CFM', b'Computing & Financial Management'), (b'FRM', b'Financial Analysis & Risk Management'), (b'OPT', b'Mathematical Optimization'), (b'STT', b'Statistics'), (b'PRM', b'Pure Mathematics'), (b'TCH', b'Math Teaching'), (b'HON', b'Honours Mathematics'), (b'COS', b'Computer Science'), (b'MTS', b'Mathematical Studies'), (b'BIO', b'Bioinformatics'), (b'MFM', b'Mathematical Finance'), (b'BUS', b'Business Administration'), (b'COO', b'Combinatorics & Optimization'), (b'APM', b'Applied Mathematics'), (b'SCC', b'Scientific Computation')]),
        ),
        migrations.AddField(
            model_name='customuser',
            name='school',
            field=models.CharField(max_length=120, blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, upload_to=b'users/photo', validators=[teams.validators.validate_image]),
        ),
    ]
