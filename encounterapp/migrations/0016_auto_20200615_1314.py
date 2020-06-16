# Generated by Django 2.1 on 2020-06-15 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encounterapp', '0015_auto_20200615_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='modify_status',
            field=models.CharField(choices=[('pending', 'Pending '), ('approved', 'Approved'), ('Deny', 'Deny')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='other_reason_for_deletion',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='reason_for_modification',
            field=models.TextField(default=''),
        ),
    ]
