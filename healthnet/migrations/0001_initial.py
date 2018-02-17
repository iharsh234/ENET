# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('role', models.IntegerField(default=0, choices=[(0, 'Unknown'), (10, 'Patient'), (20, 'Nurse'), (30, 'Doctor'), (40, 'Admin')])),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, 'None'), (1, 'Account'), (2, 'Patient'), (3, 'Admin'), (4, 'Appointment'), (5, 'Medical Test'), (6, 'Prescription'), (7, 'Admission'), (8, 'Medical Info'), (9, 'Message')])),
                ('timePerformed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('account', models.ForeignKey(to='healthnet.Account', related_name='actions_account')),
            ],
        ),
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('discharged_timestamp', models.DateTimeField(null=True, blank=True)),
                ('reason', models.CharField(choices=[('Pneumonia', 'Pneumonia'), ('Congestive Heart Failure', 'Congestive Heart Failure'), ('Hardening of the arteries', 'Hardening of the arteries'), ('Heart Attack', 'Heart Attack'), ('Chronic Obstruction Lung Disease', 'Chronic Obstruction Lung Disease'), ('Stroke', 'Stroke'), ('Irregular Heartbeat', 'Irregular Heartbeat'), ('Congestive Heart Failure', 'Congestive Heart Failure'), ('Complications of procedures, devices, implants and grafts', 'Complications of procedures, devices, implants and grafts'), ('Mood Disorders', 'Mood Disorders'), ('Fluid and Electrolyte Disorders', 'Fluid and Electrolyte Disorders'), ('Urinary Infections', 'Urinary Infections'), ('Asthma', 'Asthma'), ('Diabetes mellitus with and without complications', 'Diabetes mellitus with and without complications'), ('Skin Infections', 'Skin Infections'), ('Gallbladder Disease', 'Gallbladder Disease'), ('Gastrointestinal Bleeding', 'Gastrointestinal Bleeding'), ('Hip Fracture', 'Hip Fracture'), ('Appendicitis', 'Appendicitis'), ('Other', 'Other')], max_length=20)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('account', models.ForeignKey(to='healthnet.Account', related_name='admissions_account')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(default='Active', max_length=50)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('doctor', models.ForeignKey(to='healthnet.Account', related_name='appointments_doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(default='United States', max_length=50)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('bloodType', models.CharField(choices=[('A+', 'A+ Type'), ('B+', 'B+ Type'), ('AB+', 'AB+ Type'), ('O+', 'O+ Type'), ('A-', 'A- Type'), ('B-', 'B- Type'), ('AB-', 'AB- Type'), ('O-', 'O- Type')], max_length=10)),
                ('vision', models.CharField(choices=[('OD', 'Right Eye'), ('OS', 'Left Eye'), ('OU', 'Both Eye')], max_length=10)),
                ('glass_prescription', models.CharField(choices=[('OD', 'Right Eye'), ('OS', 'Left Eye'), ('OU', 'Both Eye')], max_length=10)),
                ('dv', models.CharField(choices=[('OD', 'Right Eye'), ('OS', 'Left Eye'), ('OU', 'Both Eye')], max_length=10)),
                ('nv', models.CharField(choices=[('OD', 'Right Eye'), ('OS', 'Left Eye'), ('OU', 'Both Eye')], max_length=10)),
                ('patching', models.CharField(choices=[('DO', 'DOING'), ('ND', 'NOT DOING'), ('BT', 'VTE/HTE/BOTH')], max_length=10)),
                ('compliance', models.CharField(choices=[('RE', 'Regular'), ('IR', 'Irregular'), ('SE', 'Sessions')], max_length=10)),
                ('treatment_plan', models.CharField(max_length=700)),
                ('account', models.ForeignKey(to='healthnet.Account', related_name='medicalinfo_account')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalTest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(choices=[('CO', 'Cover Test'), ('PB', 'PBCT'), ('ST', 'Stereopsis (Near)'), ('TF', 'Titmus Fly Test'), ('WC', 'Wirt Circle Test'), ('AT', 'Animal Test'), ('BC', 'WFDT/4D Base Cut')], max_length=10)),
                ('date', models.DateField()),
                ('distance', models.FloatField(null=True, blank=True)),
                ('near', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=200)),
                ('private', models.BooleanField(default=True)),
                ('completed', models.BooleanField()),
                ('image1', models.FileField(null=True, upload_to='medtests/%Y/%m/%d', blank=True)),
                ('image2', models.FileField(null=True, upload_to='medtests/%Y/%m/%d', blank=True)),
                ('doctor', models.ForeignKey(to='healthnet.Account', related_name='medicaltests_doctor')),
                ('hospital', models.ForeignKey(to='healthnet.Hospital')),
                ('patient', models.ForeignKey(to='healthnet.Account', related_name='medicaltests_patient')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=300)),
                ('body', models.CharField(max_length=1000)),
                ('sender_deleted', models.BooleanField(default=False)),
                ('target_deleted', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(to='healthnet.Account', related_name='messages_sender')),
                ('target', models.ForeignKey(to='healthnet.Account', related_name='messages_target')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=200)),
                ('read', models.BooleanField(default=False)),
                ('sent_timestamp', models.DateTimeField(auto_now_add=True)),
                ('read_timestamp', models.DateTimeField(null=True, blank=True)),
                ('account', models.ForeignKey(to='healthnet.Account', related_name='notifications_account')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('medication', models.CharField(max_length=100)),
                ('strength', models.CharField(max_length=30)),
                ('instruction', models.CharField(max_length=200)),
                ('refill', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(to='healthnet.Account', related_name='prescriptions_doctor')),
                ('patient', models.ForeignKey(to='healthnet.Account', related_name='prescriptions_patient')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50, blank=True)),
                ('lastname', models.CharField(max_length=50, blank=True)),
                ('insurance', models.CharField(max_length=50, blank=True)),
                ('emergencyContactName', models.CharField(max_length=50, blank=True)),
                ('emergencyContactNumber', models.CharField(max_length=20, blank=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, blank=True)),
                ('birthday', models.DateField(default=datetime.date(1000, 1, 1))),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('allergies', models.CharField(max_length=250, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('linkedEmergencyContact', models.ForeignKey(null=True, related_name='profiles_contact', to='healthnet.Account')),
                ('prefHospital', models.ForeignKey(null=True, related_name='profiles_prefhospital', to='healthnet.Hospital')),
                ('primaryCareDoctor', models.ForeignKey(null=True, related_name='profiles_primarycaredoctor', to='healthnet.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('game', models.IntegerField()),
                ('score', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to='healthnet.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='hospital',
            name='location',
            field=models.OneToOneField(to='healthnet.Location'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='hospital',
            field=models.ForeignKey(to='healthnet.Hospital'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='healthnet.Account', related_name='appointments_patient'),
        ),
        migrations.AddField(
            model_name='admission',
            name='hospital',
            field=models.ForeignKey(to='healthnet.Hospital'),
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.OneToOneField(to='healthnet.Profile'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
