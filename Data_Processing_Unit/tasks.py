from huey import RedisHuey,SqliteHuey,signals
from huey.contrib.djhuey import task,signal

import requests
from Data_Processing_Unit.data_to_mongodb import *
import datetime
import logging

logger = logging.Logger(__name__)

huey = SqliteHuey(filename='/tmp/demo.db')

from Public_Data_Acquisition_Unit.data_acquistion_manager import Acquistion_Manager

"""
    bellow are the class objects used in this module for requesting to crawler 
    and saving that data to mongo db 
"""
acq_manager = Acquistion_Manager() #object for acquistion manager to send api based http requests to ESS
news_data = News_Data()
facebook_data = Facebook_Data()
twitter_data = Twitter_Data()
instagram_data  = Instagram_Data()
linkedin_data = Linked_In_Data()


@task()
def fetch_news(news_site,top=10,GTR_ID=1):
    #fetch data from ess server

    try:
        for news in news_site:
            print('.......................................fetching News now working on  {0}...........................'.format(news))
            response = acq_manager.ess_add_news_target(top,news)
            if(response is not None):
                news_data.insert_news_data_to_mongodb(response,news,top,GTR_ID=0)

    except Exception as e:
        print(e)


#@huey.task()
def fetch_smart_search(username,search_site):
    try:
        response = acq_manager.ess_add_smart_serach_target(username,search_site)

        return response
    except Exception as e:
        print(e)

#@huey.task()
def fetch_twitter_trends_country(country='Pakistan'):
    try:
        response = acq_manager.ess_add_twitter_trends_country_target(country)
        if(response is not None):
            print(response)
            return response# insert data to mongodb here

    except Exception as e:
        logger.error(e)

#@huey.task()
def fetch_twitter_trends_worldwide():
    try:
        response = acq_manager.ess_add_twitter_trends_worldwide_target()
        if(response is not None):
            print(response)
            return response# insert data to mongodb here

    except Exception as e:
        logger.error(e)


def dispatch_notification(GTR=0,author_account=''):
    payload = {}
    response = requests.get('http://192.168.18.20:8000/core/dispatcher/'+str(GTR)+'/'+author_account, headers={}, params=payload)


@task()
def fetch_instagram_person(GTR,author_type,author_account):
    try:
        response = acq_manager.ess_add_instagram_person_target(author_type[0],author_account)
        if(response is not None):
            print(response)
            instagram_data.insert_instagram_profile_to_mongodb(GTR,response,author_account)

    except Exception as e:
        logger.error(e)
    dispatch_notification(GTR,author_account)

@task()
def fetch_facebook_person(GTR,pattern_type,author_account,):
    responses = {} # list to get multiple target results in a single fetch task


    try:

        for pattern in pattern_type :

            print('........fetching .. {0}......'.format(pattern))
            response = acq_manager.ess_add_facebook_person_target(author_account,pattern)
            if(not 'error' in response):
                responses.update({pattern:response})
            else:
                print('........Error Detected In .. {0}.......Inserting None...'.format(pattern))
                responses.update({pattern:None})

        facebook_data.insert_facebook_person_mongodb(GTR,responses,author_account)

    except Exception as e:
        logger.error(e)
    dispatch_notification(GTR, author_account)

@task()
def fetch_twitter_tweets(GTR,tweet_type='phrase',username='itsaadee',hashtag=['pmln','pti'],phrase='living my dreams',date='2015-1-1',location='NYC',distance='15mi'):

    response = None

    if(tweet_type == 'phrase'):
        response  = acq_manager.ess_add_twitter_phrase_target(tweet_type)
    elif (tweet_type == 'hashtag'):
        response = acq_manager.ess_add_twitter_hashtags_target(hashtag)
    elif (tweet_type == 'location'):
        response = acq_manager.ess_add_twitter_location_target(location,distance)
    elif (tweet_type == 'since'):
        response = acq_manager.ess_add_twitter_since_date_target(phrase,date)
    elif (tweet_type == 'untill'):
        response = acq_manager.ess_add_twitter_untill_date_target(phrase,date)
    elif (tweet_type == 'positive'):
        response = acq_manager.ess_add_twitter_positive_phrase_target(phrase)
    elif (tweet_type == 'negative'):
        response = acq_manager.ess_add_twitter_negative_phrase_target(phrase)
    elif (tweet_type == 'refferencing'):
        response = acq_manager.ess_add_twitter_refferencing_target(username)
    elif (tweet_type == 'to'):
        response = acq_manager.ess_add_twitter_to_user_target(username)
    elif (tweet_type == 'from'):
        response = acq_manager.ess_add_twitter_from_user_target(username)
    else:
        print('invalid tweet type')


    if (response is not None):
        if(tweet_type != 'refferencing' or tweet_type != 'to' or tweet_type != 'from'):
            twitter_data.insert_search_tweets_mongodb(GTR,hashtag,phrase,date,distance,response,tweet_type)

        else:
            pass

    else:
        print('response is empty or task did not executed successfully ')

@task()
def fetch_twitter_person_tweets(GTR,tweet_type='to',id='23245',name='atifaslam',account='itsaadee',url = 'https://twitter.com/itsaadee'):

    #fetch twitter person's basic information here
    #and then request again for the tweets

    response = None

    response_profile = acq_manager.ess_add_twitter_profile_target(account)

    if (tweet_type == 'refferencing'):
        response = acq_manager.ess_add_twitter_refferencing_target(account)
    elif (tweet_type == 'to'):
        response = acq_manager.ess_add_twitter_to_user_target(account)
    elif (tweet_type == 'from'):
        response = acq_manager.ess_add_twitter_from_user_target(account)
    else:
        print('invalid tweet type')


    if (response is not None):
        if(tweet_type != 'refferencing' or tweet_type != 'to' or tweet_type != 'from'):
            twitter_data.insert_person_tweets_mongodb(GTR,id,name,account,response,response_profile,tweet_type,url)
        else:
            pass
    else:
        print('response is empty or task did not executed successfully ')
    dispatch_notification(GTR, account)

@task()
def fetch_linkedin_person(GTR,author_account):
    try:

        response = acq_manager.ess_add_linkedin_person_target(author_account)

        if(response is not None):
            #print(response)
            linkedin_data.insert_linkedin_person_to_mongodb(GTR,response,author_account)

    except Exception as e:
        logger.error(e)
    dispatch_notification(GTR, author_account)

@task()
def fetch_linkedin_company(GTR,author_account):
    try:
        response = acq_manager.ess_add_linkedin_company_target(author_account)

        if(response is not None):
            print(response)
            linkedin_data.insert_linkedin_company_to_mongodb(GTR,response,author_account)

    except Exception as e:
        logger.error(e)
    dispatch_notification(GTR, author_account)

"""
@signal()
def all_signal_handler(signal, task, exc=None):
    # This handler will be called for every signal.

    print('%s - %s' % (signal, task.id))

@signal(signal.SIGNAL_ERROR, signal.SIGNAL_LOCKED, signal.SIGNAL_CANCELED, signal.SIGNAL_REVOKED)
def task_not_executed_handler(signal, task, exc=None):
    # This handler will be called for the 4 signals listed, which
    # correspond to error conditions.
    print('[%s] %s - not executed' % (signal, task.id))

@signal(signal.SIGNAL_COMPLETE)
def task_success(signal, task):
    # This handle will be called for each task that completes successfully.
    print('.............................task executed....................................')

"""