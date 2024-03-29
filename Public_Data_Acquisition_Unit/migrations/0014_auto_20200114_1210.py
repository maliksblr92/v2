# Generated by Django 2.2.7 on 2020-01-14 12:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Public_Data_Acquisition_Unit', '0013_auto_20200114_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_target_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 612014, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_group',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='facebook_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 612456, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_hashtag',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='facebook_target_page',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 611485, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 610875, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_person',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='facebook_target_search',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 612882, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_search',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='instagram_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 615237, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='instagram_target_person',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='instagram_target_search',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 615705, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='instagram_target_search',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='linkedin_target_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 616638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='linkedin_target_company',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='linkedin_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 616159, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='linkedin_target_person',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='news_site_target',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 614737, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news_site_target',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='twitter_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 613850, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_hashtag',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='twitter_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 613389, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_person',
            name='expired_on',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='twitter_target_search',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 12, 10, 12, 614305, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_search',
            name='expired_on',
            field=models.DateTimeField(),
        ),
    ]
