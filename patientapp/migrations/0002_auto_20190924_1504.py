# Generated by Django 2.0 on 2019-09-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='recall_geography',
            field=models.CharField(default='', max_length=150),
        ),
    ]
