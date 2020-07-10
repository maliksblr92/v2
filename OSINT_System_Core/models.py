"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

HEALTH_STATUS = (
        ('good', ('Health is good')),
        ('ok', ('Health is ok')),
        ('bad', ('Health is bad')),
)

WEBSITE_TYPE = (
    ('ss', ('Social Site')),
    ('ns', ('News Site')),
    ('bs', ('Blog Site')),
)

IMPACT_LIST = (
        ('+ve', ('Positive Impact')),
        ('-ve', ('Negative Impact')),
)

class Supported_Socail_Sites(models.Model):

    title = models.CharField(max_length=100)
    website_type = models.CharField(max_length=20,default='bs',choices=WEBSITE_TYPE)
    base_url = models.URLField()
    website_status = models.BooleanField(default=True) # True for valid and False for invalid
    health_status = models.CharField(max_length=50,choices=HEALTH_STATUS)
    created_on = models.DateTimeField(default=timezone.now())
    created_by = models.ForeignKey(User,default='this user is deleted', on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.title



class Keyword_Groups(models.Model):

    title = models.CharField(max_length=50)
    impact = models.CharField(max_length=30,choices=IMPACT_LIST)

    def __str__(self):
        return self.title


class Keywords(models.Model):
    keyword_group = models.OneToOneField(Keyword_Groups,on_delete=models.CASCADE)
    keyword_list = models.CharField(max_length=500)

class Periodic_Tasks(models.Model):
    model_name = models.CharField(max_length=100,default='no name')
    target_id = models.IntegerField()
    periodic_interval = models.IntegerField()
    expired_on = models.DateTimeField()
    revoke_time = models.DateTimeField()


"""
