# Generated by Django 2.2.7 on 2020-07-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Accounts_Management_Unit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]