# Generated by Django 2.0 on 2019-09-23 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import patientapp.models.patient


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addressapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.CharField(default=patientapp.models.patient.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('middle_name', models.CharField(blank=True, max_length=60)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=30)),
                ('dob', models.DateField(verbose_name='date of birth')),
                ('phone', models.CharField(max_length=17, verbose_name='phone number')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='register_date')),
                ('latitude', models.DecimalField(decimal_places=8, default=12, help_text='author latitude', max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=8, default=12, help_text='author longitude', max_digits=12)),
                ('education', models.CharField(max_length=50)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateField()),
                ('recall_date', models.DateField(blank=True, null=True)),
                ('recall_time', models.TimeField(blank=True, null=True)),
                ('recall_geography', models.CharField(blank=True, max_length=150, null=True)),
                ('activity_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_area', to='addressapp.Activity')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_obj', to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addressapp.District')),
                ('geography', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_geography', to='addressapp.Geography')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addressapp.Municipality')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='update_patient', to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addressapp.Ward')),
            ],
        ),
    ]
