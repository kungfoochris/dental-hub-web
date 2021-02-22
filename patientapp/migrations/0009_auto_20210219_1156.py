# Generated by Django 2.1 on 2021-02-19 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0008_patient_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='activity_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_area', to='addressapp.Activity'),
        ),
    ]