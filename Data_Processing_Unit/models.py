# from django.db import models
# from django.utils import timezone
# Create your models here.
import datetime

# Create your models here.
from mongoengine import *
from mongoengine import signals

DATABASE = ''
USERNAME = ''
PASSWORD = ''
HOST_IP = ''
PORT = ''

# disconnect('default')
# CONNECT TO MONGO DB
# connect(db='OSINT_Core',host='192.168.18.20', port=27017, username='ocs', password='rapidev')
connect(db='OSINT_System', host='192.168.18.20', port=27017)


# connect('OSINT_Core')

class Raw_Data(Document):
    GTR = IntField()
    CTR = IntField()
    data = DictField()


class Change_Record(Document):
    GTR = IntField()
    CTR = IntField()
    recent_CTR = IntField()
    # attribute_keylist = DictField()


"""
class experiment(Document):
    GTR= IntField()
    name= StringField()
    marks= IntField()

class News_Fetched_Data(Document):

    news_site = StringField(max_length=100,required=True)
    title = StringField(max_length=1000)
    description = StringField(max_length=2000)
    url = URLField()
    time = StringField(max_length=50)
    global_target_id = IntField()
    processed = BooleanField()
    target_update_count = LongField()
    created_on = DateTimeField()
"""


class Person_Tweets(EmbeddedDocument):
    tweet_type = StringField(max_length=50)  # it can be off refference, to , from type
    username_tweet = StringField(max_length=50)
    id = IntField()
    text = StringField()
    url = StringField()
    retweeet_count = IntField()
    favourite_count = IntField()
    replies_count = IntField()
    datetime_created = StringField(max_length=50)
    is_reply = BooleanField()
    is_retweet = BooleanField()
    sentiment = StringField()
    user_id = StringField(max_length=50)


"""
class Search_Tweets(EmbeddedDocument):
    tweet_type = StringField(max_length=50)  # it can be of phrase,hashtag,location,sincedate,untilldate,positive or negative attitude, type
    username_tweet = StringField(max_length=50)
    id = StringField()
    text = StringField()
    url = StringField()
    retweeet_count = IntField()
    favourite_count = IntField()
    replies_count = IntField()
    datetime_created = StringField(max_length=50)
    is_reply = BooleanField()
    is_retweet = BooleanField()
    user_id = StringField(max_length=50)


class Twitter_Search(Document):
    GTR = IntField()
    hashtags = ListField()
    pharse  = StringField(max_length=50)
    date = StringField(max_length=30)
    distance = StringField(max_length=30)
    target_update_count = LongField()
    tweets = ListField(EmbeddedDocumentField(Search_Tweets))
    created_on = DateTimeField()
"""


class Twitter_Response_TMS(Document):
    GTR = IntField()
    author_account = LongField()
    name = StringField(max_length=50)
    location = StringField()
    profile_url = StringField()
    biodata = StringField()
    # interests = ListField()
    frequent_hashtags = ListField()
    website = StringField()
    joined_twitter = StringField()
    tweets_count = StringField()
    follower_count = StringField()
    following_count = StringField()
    likes_count = StringField()
    moments = StringField()
    # close_associates = ListField()
    profile_summary = StringField()
    post_frequency_graph = ListField()
    target_update_count = LongField()
    behaviour = StringField()
    common_words = ListField()
    sentiments = ListField()
    topic = ListField()
    emotions = ListField()
    posting_time_charts = ListField()
    tweets = ListField(EmbeddedDocumentField(Person_Tweets))


class Linkedin_Response_TMS(Document):
    GTR = IntField()
    target_type = StringField()
    name = StringField()
    headline = StringField()
    company = StringField()
    school = StringField()
    location = StringField()
    image_url = StringField()
    followers = StringField()
    email = StringField()
    phone = StringField()
    connected = StringField()
    websites = ListField()
    target_update_count = LongField()
    profile_summary = StringField()
    current_company_link = StringField()
    skills = ListField()
    experience = DictField()
    interests = ListField()
    accomplishments = DictField()
    field_of_interest = StringField()
    experience_education_graph = ListField()

    description = StringField()
    company_size = StringField()
    industry = StringField()
    headquarters = StringField()
    company_type = StringField()
    founded = StringField()
    specialties = StringField()
    number_of_employees = IntField()
    jobs = DictField()


"""
class Linkedin_Company(Document):
    GTR = IntField()
    description = StringField()
    name = StringField()
    author_account = StringField()
    company_size = StringField()
    website = URLField()
    industry = StringField()
    headquarters = StringField()
    company_type = StringField()
    founded = StringField()
    specialties = StringField()
    number_of_employees = IntField()
    image_url = StringField()
    target_update_count = LongField()
    profile_summary = StringField()
    jobs = DictField()
"""


class Instagram_Posts(EmbeddedDocument):
    owner_id = IntField()
    owner_username = StringField()
    caption = StringField()
    comments_count = IntField()
    likes_count = IntField()
    display_url = URLField()


class Instagram_Response_TMS(Document):
    GTR = IntField()
    target_type = StringField()
    biography = StringField()
    external_url = URLField()
    followed_by = IntField()
    follow = IntField()
    fullname = StringField()
    username = StringField()
    person_id = IntField()
    is_business_account = BooleanField()
    is_joined_recently = BooleanField()
    is_verified = BooleanField()
    profile_picture_url = URLField()
    connected_fb_page = URLField()
    # created_on = DateTimeField()
    target_update_count = LongField()
    profile_summary = StringField()
    behaviour = StringField()
    common_words = ListField()
    sentiments = ListField()
    topic = ListField()
    emotions = ListField()

    posts = ListField(EmbeddedDocumentField(Instagram_Posts))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        print('.........................................MongoSignal..............................................')


# signals.pre_save.connect(Instagram_Person.pre_save, sender=Instagram_Person)

class Facebook_Response_TMS(Document):
    GTR = IntField()
    name = StringField()
    author_id = IntField()
    target_type = StringField()
    # author_account = StringField()
    profile_picture_url = DictField()
    work = ListField()
    education = ListField()
    professional_skills = ListField()
    location_details = ListField()
    contact_information = ListField()
    web_links = DictField()
    general_information = DictField()
    relationship = ListField()
    family = ListField()
    life_events_timeline = ListField()
    friends = ListField()
    posts = ListField()
    comments = DictField()
    mentions = ListField()
    close_associates = ListField()
    pictures = ListField()
    check_ins = ListField()
    interests = DictField()
    profile_overview_summary = StringField()
    profile_friends_summary = StringField()
    profile_interest_summary = StringField()
    profile_close_associates_summary = StringField()
    posting_time_charts = ListField()
    sentiments = ListField()
    behaviour = StringField()
    common_words = ListField()
    sentiments = ListField()
    topic = ListField()
    emotions = ListField()
    target_update_count = LongField()


"""
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self.name)



class Profile_Analysis_Data(Document):
    GTR = IntField()
    social_site = StringField()
    author_account = StringField()
    summary = StringField()
    suspicious  = IntField()
    fake_profile = IntField()


class Post_Analysis_Data(Document):
    pass

class Tweet_Analysis_Data(Document):
    pass

class News_Analysis_Data(Document):
    pass

class News_Channel_Analysis_Data(Document):
    pass

"""













