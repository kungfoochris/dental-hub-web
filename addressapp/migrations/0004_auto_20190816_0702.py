# Generated by Django 2.0 on 2019-08-16 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addressapp', '0003_district_municipality_ward'),
    ]

    operations = [
        migrations.RenameField(
            model_name='district',
            old_name='district',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='municipality',
            old_name='municipality',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='municipality',
            old_name='municipality_type',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='municipality',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addressapp.District'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='municipality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addressapp.Municipality'),
        ),
    ]
