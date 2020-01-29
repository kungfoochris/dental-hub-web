# Generated by Django 2.1 on 2020-01-13 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationapp', '0011_auto_20191127_0533'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='visualization',
            index=models.Index(fields=['activities_id', 'geography_id'], name='visualizati_activit_28d1e0_idx'),
        ),
        migrations.AddIndex(
            model_name='visualization',
            index=models.Index(fields=['-created_at'], name='visualizati_created_31e5da_idx'),
        ),
    ]