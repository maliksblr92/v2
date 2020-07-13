# Generated by Django 2.2.7 on 2019-12-16 12:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Public_Data_Acquisition_Unit', '0004_auto_20191216_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_target_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 554749, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 555177, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_page',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 554233, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 553757, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='facebook_target_person',
            name='expired_on',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='facebook_target_search',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 555593, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='global_target_record',
            name='author_type',
            field=models.CharField(choices=[('facebook_person', 'Author is a Facebook Users Profile'), ('facebook_page', 'Author is a Facebook Page'), ('facebook_group', 'Author is a Facebook Group'), ('facebook_hashtag', 'Author is a Facebook HashTag'), ('facebook_search', 'Author is a Facebook Search'), ('twitter_person', 'Author is a Twitter Person'), ('twitter_search', 'Author is a Twitter Search'), ('instagram_author', 'Author is a Instagram Person'), ('instagram_search', 'Author is a Instagram Search'), ('News_Target', 'Author is a News Target')], max_length=100),
        ),
        migrations.AlterField(
            model_name='news_site_target',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 556938, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_hashtag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 556482, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twitter_target_person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 12, 16, 36, 556047, tzinfo=utc)),
        ),
    ]
