# Generated by Django 2.0 on 2019-07-03 07:34

from django.db import migrations, models
import django.db.models.deletion
import treatmentapp.models.treatment


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('encounterapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.CharField(blank=True, max_length=200)),
                ('uid', models.CharField(default=treatmentapp.models.treatment.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('teeth1', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth2', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth3', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth4', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth5', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth6', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth7', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth8', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth9', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth10', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth11', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth12', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth13', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth14', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth15', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth16', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth17', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth18', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth19', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth20', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth21', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth22', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth23', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth24', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth25', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth26', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth27', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth28', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth29', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth30', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth31', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('teeth32', models.CharField(choices=[('SDF', 'SDF'), ('SEAL', 'SEAL'), ('ART', 'ART'), ('EXO', 'EXO'), ('UNTR', 'UNTR'), ('No_Treatment', 'Null')], default='No_Treatment', max_length=30)),
                ('fluoride_varnish', models.BooleanField(default=False, verbose_name='fluoride varnish')),
                ('treatment_complete', models.BooleanField(default=False, verbose_name='treatment complete')),
                ('note', models.TextField(blank=True)),
                ('encounter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='encounterapp.Encounter')),
            ],
        ),
    ]
