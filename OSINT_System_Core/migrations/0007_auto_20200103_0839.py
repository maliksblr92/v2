# Generated by Django 2.2.7 on 2020-01-03 08:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OSINT_System_Core', '0006_auto_20191212_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodic_Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('target_id', models.IntegerField()),
                ('periodic_interval', models.IntegerField()),
                ('expired_on', models.DateTimeField()),
                ('revoke_time', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='supported_socail_sites',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 3, 8, 39, 19, 671704, tzinfo=utc)),
        ),
    ]