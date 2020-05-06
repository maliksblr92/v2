"""
from django.utils import timezone
import datetime

from Public_Data_Acquisition_Unit.models import News_Site_Target, \
        Twitter_Target_Search, \
        Twitter_Target_Person, \
        Facebook_Target_Person, \
        Linkedin_Target_Person, \
        Linkedin_Target_Company, \
        Instagram_Target_Person, \
        Instagram_Target_Search


from Data_Processing_Unit import tasks
from OSINT_System_Core.models import Periodic_Tasks
import random
import logging

from django_eventstream import send_event

from threading import Thread
import time

logger = logging.Logger(__name__)

class Digger(Thread):
    def __init__(self, seconds):
        '''Note that when you override __init__, you must
           use super() to call __init__() in the base class
           so you'll get all the "chocolately-goodness" of
           threading (i.e., the magic that sets up the thread
           within the OS) or it won't work.
        '''

        self.d_assis = D_Assis()
        super().__init__()
        self.delay = seconds
        self.is_done = False

    def done(self):
        self.is_done = True

    def run(self):
        while not self.is_done:
            time.sleep(self.delay)
            num = random.randint(10,100)

            self.d_assis.task_polling()


            #print('......................................DIGGER LIVE..........................................')



        print('thread done')


class D_Assis(object):
    def __init__(self):
        pass


    def get_periodic_task_list(self):
        task_list = Periodic_Tasks.objects.all()
        return task_list

    def do_invoke_tasks(self,model_name,object_id):

        if(model_name == 'Instagram_Target_Person'):
            instance = Instagram_Target_Person.objects.get(pk=object_id)
            GTR = instance.global_target_reff.id
            id = instance.author_id
            name = instance.author_name
            account = instance.author_account
            url = instance.author_url
            periodic_interval = instance.periodic_interval
            print(str(instance).split(' ')[0], GTR, id, name, account, url, periodic_interval)

            tasks.fetch_instagram_person(GTR,['overview','post'],account)

        if (model_name == 'Linkedin_Target_Person'):
            instance = Linkedin_Target_Person.objects.get(pk=object_id)

            GTR = instance.global_target_reff.id
            id = instance.author_id
            name = instance.author_name
            account = instance.author_account
            url = instance.author_url
            periodic_interval = instance.periodic_interval

            print(GTR, id, name, account, url, periodic_interval)

            tasks.fetch_linkedin_person(GTR, account)

            print('..............................LinkedIn Person Target Sumbitted...........................................')

        if (model_name == 'Linkedin_Target_Company'):
            instance = Linkedin_Target_Company.objects.get(pk=object_id)

            GTR = instance.global_target_reff.id
            id = instance.author_id
            name = instance.author_name
            account = instance.author_account
            url = instance.author_url
            periodic_interval = instance.periodic_interval

            print(GTR, id, name, account, url, periodic_interval)
            tasks.fetch_linkedin_company(GTR, account)

            print('..............................LinkedIn Company Target Sumbitted...........................................')

        if (model_name == 'Facebook_Target_Person'):
            instance = Facebook_Target_Person.objects.get(pk=object_id)
            GTR = instance.global_target_reff.id
            id = instance.author_id
            name = instance.author_name
            account = instance.author_account
            url = instance.author_url
            periodic_interval = instance.periodic_interval

            tasks.fetch_facebook_person(GTR, ['overview', 'posts', 'closeAssociates', 'checkIns', 'interests'], account)

            print('..............................Facebook Person Target Sumbitted...........................................')

        if (model_name == 'Twitter_Target_Person'):
            instance = Twitter_Target_Person.objects.get(pk=object_id)

            GTR = instance.global_target_reff.id
            tweet_type = instance.tweets_type
            id = instance.author_id
            name = instance.author_name
            account = instance.author_account
            url = instance.author_url
            periodic_interval = instance.periodic_interval

            tasks.fetch_twitter_person_tweets(GTR, tweet_type, id, name, account, url)
            print('..............................Twitter Person Target Sumbitted...........................................')

        if (model_name == 'Twitter_Target_Search'):
            instance = Twitter_Target_Search.objects.get(pk=object_id)
            GTR = instance.global_target_reff.id
            tweet_type = instance.search_type
            hashtags = instance.hashtags
            phrase = instance.phrase
            date = instance.date
            location = instance.location
            radius = instance.distance

            hashtags = hashtags.split(',')

            tasks.fetch_twitter_tweets(GTR,tweet_type,'prince.nuada.16',hashtags,phrase,date,location,radius)
            print('..............................Twitter Search Target Sumbitted...........................................')

        if(model_name == 'System_Defined_Task'):
            tasks.fetch_news(['ary','bbc','geo','dawn','abp','ndtv','indiatoday','zee'])
            print('..............................System Defined Task Submitted...........................................')

    def task_polling(self):
        tasks_list = self.get_periodic_task_list()

        for task in tasks_list:
            time_now = timezone.now()
            invoke_time = task.revoke_time

            if(time_now > invoke_time):
                # then invoke the task
                task.revoke_time = timezone.now() + datetime.timedelta(minutes=task.periodic_interval)
                task.save()
                self.do_invoke_tasks(task.model_name,task.target_id)
                print('*************************************Task Reinvoked {0}*****************************'.format(task.model_name))

            self.remove_expired_tasks(task)
        print('..................................Task Polling Survey Completed..................................')

    def remove_expired_tasks(self,task):
        time_now = timezone.now()
        expiry_time = task.expired_on

        if(time_now > expiry_time):
            task.delete()
            print('######################################### expired task deleted #####################################')



"""


