# Generated by Django 2.1 on 2022-01-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encounterapp', '0040_modifydelete_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refer',
            name='other',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
