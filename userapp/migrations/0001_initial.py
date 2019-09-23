# Generated by Django 2.0 on 2019-09-23 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userapp.models.role
import userapp.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addressapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default=userapp.models.user.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='admin', max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('image', models.FileField(default='profile/default-avatar.png', upload_to='profile')),
                ('email', models.EmailField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.CharField(default=userapp.models.role.keygenerator, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('location', models.ManyToManyField(to='addressapp.Ward')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='userapp.Role')),
            ],
            options={
                'abstract': False,
            },
            bases=('userapp.user',),
        ),
    ]
