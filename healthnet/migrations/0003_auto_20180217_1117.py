# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0002_profile_limit_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalinfo',
            name='bloodType',
        ),
        migrations.AlterField(
            model_name='admission',
            name='reason',
            field=models.CharField(max_length=20, choices=[('Isometric Refractive Amblyopia', 'Isometric Refractive Amblyopia'), ('Anisometric Refractive Amblyopia', 'Anisometric Refractive Amblyopia'), ('Strabismic', 'Strabismic'), ('Mixed Amblyopia', 'Mixed Amblyopia'), ('Deprivation Amblyopia', 'Deprivation Amblyopia'), ('Suppression', 'Suppression'), ('Visual perceptual skills deficiency', 'Visual perceptual skills deficiency'), ('Other', 'Other')]),
        ),
        migrations.AlterField(
            model_name='medicalinfo',
            name='vision',
            field=multiselectfield.db.fields.MultiSelectField(max_length=8, choices=[('OD', 'Right Eye'), ('OS', 'Left Eye'), ('OU', 'Both Eye')]),
        ),
    ]
