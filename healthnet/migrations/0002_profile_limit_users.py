# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='limit_users',
            field=models.IntegerField(default=20),
        ),
    ]
