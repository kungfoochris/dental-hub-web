# Generated by Django 2.0 on 2019-09-23 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import treatmentapp.models.treatment


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('encounterapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.CharField(default=treatmentapp.models.treatment.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('tooth18', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth17', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth16', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth15', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth14', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth13', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth12', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth11', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth21', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth22', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth23', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth24', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth25', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth26', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth27', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth28', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth48', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth47', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth46', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth45', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth44', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth43', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth42', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth41', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth31', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth32', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth33', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth34', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth35', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth36', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth37', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth38', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth55', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth54', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth53', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth52', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth51', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth61', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth62', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth63', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth64', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth65', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth85', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth84', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth83', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth82', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth81', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth71', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth72', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth73', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth74', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('tooth75', models.CharField(choices=[('NONE', 'NONE'), ('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('SMART', 'SMART')], default='NONE', max_length=30)),
                ('fv_applied', models.BooleanField(default=False, verbose_name='fluoride varnish')),
                ('treatment_plan_complete', models.BooleanField(default=False, verbose_name='treatment complete')),
                ('notes', models.TextField(blank=True)),
                ('sdf_whole_mouth', models.BooleanField(default=False)),
                ('updated_at', models.DateField(null=True)),
                ('created_at', models.DateField()),
                ('encounter_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='encounterapp.Encounter')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='update_treatment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
