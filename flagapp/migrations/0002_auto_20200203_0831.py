# Generated by Django 2.1 on 2020-02-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flagapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flag',
            name='message',
        ),
        migrations.AlterField(
            model_name='flag',
            name='updated_at',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]
