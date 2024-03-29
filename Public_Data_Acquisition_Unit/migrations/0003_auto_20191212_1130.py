# Generated by Django 2.2.7 on 2019-12-12 11:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Public_Data_Acquisition_Unit', '0002_auto_20191210_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_target_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 583448, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 583881, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_page',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 582931, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 582467, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_search',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 584295, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 585220, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 11, 30, 46, 584730, tzinfo=utc)),
        ),
    ]
