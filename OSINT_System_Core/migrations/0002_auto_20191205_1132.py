# Generated by Django 2.2.7 on 2019-12-05 11:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OSINT_System_Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supported_socail_sites',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 5, 11, 32, 46, 445914, tzinfo=utc)),
        ),
    ]
