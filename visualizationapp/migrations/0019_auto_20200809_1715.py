# Generated by Django 2.1 on 2020-08-09 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationapp', '0018_auto_20200601_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualization',
            name='encounter_id',
            field=models.CharField(db_index=True, max_length=60),
        ),
    ]
