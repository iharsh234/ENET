# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0003_auto_20180217_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalinfo',
            name='bloodType',
            field=models.CharField(max_length=10, choices=[('A+', 'A+ Type'), ('B+', 'B+ Type'), ('AB+', 'AB+ Type'), ('O+', 'O+ Type'), ('A-', 'A- Type'), ('B-', 'B- Type'), ('AB-', 'AB- Type'), ('O-', 'O- Type')], default='None'),
        ),
    ]
