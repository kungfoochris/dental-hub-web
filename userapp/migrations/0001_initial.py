# Generated by Django 2.0 on 2019-06-24 11:44

from django.db import migrations, models
import userapp.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default=userapp.models.user.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='admin', max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
