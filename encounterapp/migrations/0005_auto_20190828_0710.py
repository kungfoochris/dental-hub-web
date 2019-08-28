# Generated by Django 2.0 on 2019-08-28 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encounterapp', '0004_screeing_blood_pressure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screeing',
            name='blood_pressure',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Low', 'Low'), ('High', 'High')], default='Normal', max_length=15),
        ),
    ]
