# Generated by Django 2.2.7 on 2019-12-10 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OSINT_System_Core', '0004_auto_20191210_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supported_socail_sites',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 10, 11, 20, 28, 621532, tzinfo=utc)),
        ),
    ]
