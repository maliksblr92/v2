"""
from Public_Data_Acquisition_Unit.models import News_Site_Target,\
    Twitter_Target_Search,\
    Twitter_Target_Person,\
    Facebook_Target_Person,\
    Linkedin_Target_Person,\
    Linkedin_Target_Company,\
    Instagram_Target_Person,\
    Instagram_Target_Search

from django.utils import timezone
from OSINT_System_Core.models import Periodic_Tasks
from django.db.models.signals import post_save
from django.dispatch import receiver
from Data_Processing_Unit import tasks


import datetime
import os
#this manager is responsible to recive sygnals dispatched by difference models


@receiver(post_save,sender=News_Site_Target)
def news_site_target_created(sender,instance,**kwargs):

    #signal occured on when a news target is submitted

    global_target_reff = instance.global_target_reff.id
    news_site = instance.news_site
    top = instance.top
    tasks.fetch_news(news_site,top,global_target_reff)
    print('..............................News Task Submitted...{0}...{1}..'.format(news_site,top))




@receiver(post_save,sender=Twitter_Target_Search)
def twitter_search_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted


    GTR = instance.global_target_reff.id
    tweet_type = instance.search_type
    hashtags = instance.hashtags
    phrase = instance.phrase
    date = instance.date
    location = instance.location
    radius = instance.distance
    periodic_interval = instance.periodic_interval

    hashtags = hashtags.split(',')

    if (periodic_interval != 0):
        model_name = 'Twitter_Target_Search'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                            target_id=instance.id,
                                            periodic_interval=instance.periodic_interval,
                                            expired_on=instance.expired_on,
                                            revoke_time=datetime.datetime.now()
                                            )

        obj.save()

    tasks.fetch_twitter_tweets(GTR,tweet_type,'prince.nuada.16',hashtags,phrase,date,location,radius)
    print('..............................Twitter Search Target Sumbitted...........................................')

@receiver(post_save,sender=Twitter_Target_Person)
def twitter_person_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted

    GTR = instance.global_target_reff.id
    tweet_type = instance.tweets_type
    id = instance.author_id
    name = instance.author_name
    account = instance.author_account
    url = instance.author_url
    periodic_interval = instance.periodic_interval

    if (periodic_interval != 0):
        model_name = 'Twitter_Target_Person'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                            target_id=instance.id,
                                            periodic_interval=instance.periodic_interval,
                                            expired_on=instance.expired_on,
                                            revoke_time=datetime.datetime.now()
                                            )

        obj.save()

    tasks.fetch_twitter_person_tweets(GTR,tweet_type,id,name,account,url)
    print('..............................Twitter Person Target Sumbitted...........................................')

@receiver(post_save,sender=Facebook_Target_Person)
def facebook_person_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted

    GTR = instance.global_target_reff.id
    id = instance.author_id
    name = instance.author_name
    account = instance.author_account
    url = instance.author_url
    periodic_interval = instance.periodic_interval



    if(periodic_interval != 0):
        model_name = 'Facebook_Target_Person'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                            target_id=instance.id,
                                            periodic_interval=instance.periodic_interval,
                                            expired_on=instance.expired_on,
                                            revoke_time=datetime.datetime.now()
                                            )

        obj.save()

    tasks.fetch_facebook_person(GTR, ['overview', 'posts', 'closeAssociates', 'checkIns', 'interests'], account)
    print('..............................Facebook Person Target Sumbitted...........................................')

@receiver(post_save,sender=Linkedin_Target_Person)
def linkedin_person_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted

    GTR = instance.global_target_reff.id
    id = instance.author_id
    name = instance.author_name
    account = instance.author_account
    url = instance.author_url
    periodic_interval = instance.periodic_interval

    print(GTR,id,name,account,url,periodic_interval)

    if (periodic_interval != 0):
        model_name = 'Linkedin_Target_Person'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                            target_id=instance.id,
                                            periodic_interval=instance.periodic_interval,
                                            expired_on=instance.expired_on,
                                            revoke_time=datetime.datetime.now()
                                            )

        obj.save()

    tasks.fetch_linkedin_person(GTR,account)

    print('..............................LinkedIn Person Target Sumbitted...........................................')


@receiver(post_save,sender=Linkedin_Target_Company)
def linkedin_company_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted

    GTR = instance.global_target_reff.id
    id = instance.author_id
    name = instance.author_name
    account = instance.author_account
    url = instance.author_url
    periodic_interval = instance.periodic_interval



    print(str(instance))
    #print(str(instance).split(' ')[0], GTR, id, name, account, url, periodic_interval)

    if (periodic_interval != 0):
        model_name = 'Linkedin_Target_Company'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                            target_id=instance.id,
                                            periodic_interval=instance.periodic_interval,
                                            expired_on=instance.expired_on,
                                            revoke_time=timezone.now()
                                            )

        obj.save()

    tasks.fetch_linkedin_company(GTR,account)
    print('..............................LinkedIn Company Target Sumbitted...........................................')

@receiver(post_save,sender=Instagram_Target_Person)
def instagram_person_target_created(sender,instance,**kwargs):
    #signal occured on when a news target is submitted

    GTR = instance.global_target_reff.id
    id = instance.author_id
    name = instance.author_name
    account = instance.author_account
    url = instance.author_url
    periodic_interval = instance.periodic_interval

    print(str(instance).split(' ')[0],GTR, id, name, account, url, periodic_interval)

    if(periodic_interval != 0):
        model_name = 'Instagram_Target_Person'
        obj = Periodic_Tasks.objects.create(model_name=model_name,
                                      target_id=instance.id,
                                      periodic_interval=instance.periodic_interval,
                                      expired_on=instance.expired_on,
                                    revoke_time=timezone.now()
                                    )

        obj.save()

    tasks.fetch_instagram_person(GTR,['overview','post'],account)

    print('..............................Instagram Person Target Sumbitted...........................................')

"""