# Generated by Django 2.0 on 2019-08-15 08:19

import addressapp.models.activity
import addressapp.models.address
import addressapp.models.geography
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityArea',
            fields=[
                ('id', models.CharField(default=addressapp.models.activity.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('area', models.CharField(choices=[('Health Post', 'Health Post'), ('School Seminar', 'School Seminar'), ('Community Outreach, ', 'Community Outreach'), ('Training, ', 'Training ')], max_length=30)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.CharField(default=addressapp.models.address.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=50)),
                ('municipality', models.CharField(max_length=50)),
                ('municipality_type', models.CharField(max_length=50)),
                ('ward', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='ward_number')),
            ],
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.CharField(default=addressapp.models.geography.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=50)),
                ('municipality', models.CharField(max_length=50)),
                ('municipality_type', models.CharField(max_length=50)),
                ('ward', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='ward_number')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
