# Generated by Django 2.2.7 on 2020-08-05 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('rank', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('cnic', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('employee_number', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.OneToOneField(default='EMPTY', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
