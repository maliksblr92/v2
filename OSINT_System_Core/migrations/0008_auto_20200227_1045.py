# Generated by Django 2.2.7 on 2020-02-27 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Public_Data_Acquisition_Unit', '0015_auto_20200227_1045'),
        ('OSINT_System_Core', '0007_auto_20200103_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keywords',
            name='keyword_group',
        ),
        migrations.DeleteModel(
            name='Periodic_Tasks',
        ),
        migrations.RemoveField(
            model_name='supported_socail_sites',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Keyword_Groups',
        ),
        migrations.DeleteModel(
            name='Keywords',
        ),
        migrations.DeleteModel(
            name='Supported_Socail_Sites',
        ),
    ]
