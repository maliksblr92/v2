"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from OSINT_System_Core.models import Supported_Socail_Sites
# Create your models here.

AUTHOR_TYPE = (
        ('facebook_person', ('Author is a Facebook Users Profile')),
        ('facebook_page', ('Author is a Facebook Page')),
        ('facebook_group', ('Author is a Facebook Group')),
        ('facebook_hashtag', ('Author is a Facebook HashTag')),
        ('facebook_search', ('Author is a Facebook Search')),
        ('twitter_person', ('Author is a Twitter Person')),
        ('twitter_search', ('Author is a Twitter Search')),
        ('instagram_author', ('Author is a Instagram Person')),
        ('instagram_search', ('Author is a Instagram Search')),
        ('News_Target', ('Author is a News Target')),
    )

AUTHOR_TYPE_FACEBOOK = (
        ('facebook_person', ('Author is a Facebook Users Profile')),
        ('facebook_page', ('Author is a Facebook Page')),
        ('facebook_group', ('Author is a Facebook Group')),
        ('facebook_hashtag', ('Author is a Facebook HashTag')),
        ('facebook_search', ('Author is a Facebook Search')),
    )

AUTHOR_TYPE_TWITTER = (
        ('twitter_person', ('Author is a Twitter Person')),
        ('twitter_search', ('Author is a Twitter Search')),
    )

AUTHOR_TYPE_LINKEDIN = (
        ('linkedin_person', ('Author is a Linkedin Person')),
        ('linkedin_search', ('Author is a Linkedin Search')),
    )

AUTHOR_TYPE_INSTAGRAM = (
        ('instagram_person', ('Author is a Instagram Person')),
        ('instagram_search', ('Author is a Instagram Search')),
    )

SEARCH_TYPE_TWITTER = (
        ('phrase', ('search using text phrase')),
        ('hashtag', ('search using hastags')),
        ('location', ('search using location')),
        ('bydate', ('search using date')),
    )

TWEETS_TYPE_TWITTER = (
        ('refferencing', ('tweets should be of refferencing type')),
        ('to', ('tweets should be of to type')),
        ('from', ('tweets should be of from type')),
    )

AUTHOR_TYPE_NEWS = (
        ('ary', ('Author is Ary News Target')),
        ('bbc', ('Author is a BBC News Target')),
        ('geo', ('Author is a Geo News Target')),
        ('dawn', ('Author is a DAWN News Target')),
        ('abp', ('Author is a ABP News Target')),
        ('ndtv', ('Author is a NDTV News Target')),
        ('abp', ('Author is a IndiaToday News Target')),
    )


PERIODIC_INTERVALS = (
        (0,('on time only')),
        (5,('once per 5 minutes ')),
        (10, ('once per 10 minutes ')),
        (15, ('once per 15 minutes ')),
        (30, ('once per 30 minutes ')),
        (40, ('once per 40 minutes ')),
        (60, ('once per 60 minutes ')),
        (90, ('once per 90 minutes ')),
        (120, ('once per 120 minutes ')),
        (180, ('once per 180 minutes ')),
        (360, ('once per 360 minutes ')),
        (720, ('once per 720 minutes ')),
    )

IS_ENABLED = (
        (True,('Target is Enabled')),
        (False,('Target is Disabled'))
    )

IS_EXPIRED = (
    (True, ('Target is Expired')),
    (False, ('Target is Functional'))
)

NEWS_SITES = (
        ('bbc', ('BBC News')),
        ('ary', ('ARY News')),
        ('geo', ('GEO News')),
        ('dawn', ('DAWN News')),
)


class Global_Target_Record(models.Model):


    social_site_reff = models.ForeignKey(Supported_Socail_Sites,on_delete=models.CASCADE) # add social site forignkey refferencs
    ess_target_reff = models.CharField(max_length=100,null=True)
    author_type = models.CharField(max_length=100,choices=AUTHOR_TYPE)

    def __str__(self):
        return self.author_type

class Facebook_Target_Person(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    author_id = models.CharField(max_length=100)
    author_account = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.author_name

class Facebook_Target_Page(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    page_id = models.CharField(max_length=100)
    page_account = models.CharField(max_length=100)
    page_name = models.CharField(max_length=100)
    page_url = models.URLField()
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Facebook_Target_Group(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    group_id = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)
    group_url = models.URLField()
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Facebook_Target_Hashtag(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    target_keywords = models.CharField(max_length=1000) #should enter comma seprated kewwords to look in to page
    web_page_url = models.URLField() #any facebook page or profiles url to get the hashtags from
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Facebook_Target_Search(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    target_keywords = models.CharField(max_length=1000) #should enter comma seprated kewwords to look in to page
    web_page_url = models.URLField() #any facebook page or profiles url to get the hashtags from
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())


class Twitter_Target_Person(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=100)
    author_account = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()
    tweets_type  = models.CharField(max_length=20,default='from')
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Twitter_Target_Hashtag(models.Model):


    global_target_reff = models.OneToOneField(Global_Target_Record,on_delete=models.CASCADE)
    target_keywords = models.CharField(max_length=1000) #should enter comma seprated kewwords to look in to page
    web_page_url = models.URLField() #any facebook page or profiles url to get the hashtags from
    expired_on  = models.DateTimeField()
    is_enabled = models.BooleanField(default=True,choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False,choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50,choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Twitter_Target_Search(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    hashtags = models.CharField(max_length=200,default='')  # should enter comma seprated kewwords to look in to page
    phrase = models.CharField(max_length=200,default='')
    date = models.CharField(max_length=30,default='')
    location = models.CharField(max_length=30,default='')
    distance = models.CharField(max_length=20,default='')
    search_type = models.CharField(max_length=50,choices=SEARCH_TYPE_TWITTER)
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class News_Site_Target(models.Model):


    #save targets for news sites
    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    news_site = models.CharField(max_length=30,choices=NEWS_SITES)
    top = models.IntegerField(default=10)
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Instagram_Target_Person(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=100)
    author_account = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Instagram_Target_Search(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    target_keywords = models.CharField(max_length=1000)  # should enter comma seprated kewwords to look in to page
    web_page_url = models.URLField()  # any facebook page or profiles url to get the hashtags from
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

class Linkedin_Target_Person(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=100)
    author_account = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id) + '   ' + self.author_name

class Linkedin_Target_Company(models.Model):

    global_target_reff = models.OneToOneField(Global_Target_Record, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=100)
    author_account = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()
    expired_on = models.DateTimeField()
    is_enabled = models.BooleanField(default=True, choices=IS_ENABLED)
    is_expired = models.BooleanField(default=False, choices=IS_EXPIRED)
    need_screenshots = models.BooleanField(default=False)
    periodic_interval = models.IntegerField(max_length=50, choices=PERIODIC_INTERVALS)
    created_on = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)+ '   '+self.author_name

"""