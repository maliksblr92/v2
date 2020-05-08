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
    GTR = StringField()
    CTR = IntField()
    data = DictField()


class Change_Record(Document):
    GTR = StringField()
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
    GTR = StringField()
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
    emotions = ListField()
    posting_time_charts = ListField()
    tweets = ListField(EmbeddedDocumentField(Person_Tweets))


class Linkedin_Profile_Response_TMS(Document):
    GTR = StringField()
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
    field_of_interest = ListField()
    experience_education_graph = ListField()
    linked_to = DictField()


class Linkedin_Company_Response_TMS(Document):
    GTR = StringField()
    target_type = StringField()
    name = StringField()
    image_url = StringField()
    websites = StringField()
    target_update_count = LongField()
    description = StringField()
    company_size = StringField()
    industry = StringField()
    headquarters = StringField()
    company_type = StringField()
    founded = StringField()
    specialties = StringField()
    number_of_employees = IntField()
    jobs = DictField()
    linked_to = DictField()


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
    GTR = StringField()
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
    emotions = ListField()

    posts = ListField(EmbeddedDocumentField(Instagram_Posts))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        print('.........................................MongoSignal..............................................')


# signals.pre_save.connect(Instagram_Person.pre_save, sender=Instagram_Person)
class Facebook_Posts(EmbeddedDocument):
    post_id = IntField()
    author_name = StringField()
    auther_id = IntField()
    author_url = StringField()
    author_media_directory = StringField()
    post_link = URLField()
    entity_type = StringField()
    associated_links = ListField()
    headline = StringField()
    post_text = StringField()
    complete_time = DateTimeField()
    reactions_statistics = IntField()
    comments_statistics = IntField()
    shares_statistics = IntField()
    picture_directory = ListField()
    sentiment = StringField()
    video_directory = ListField()
    reactions = DictField()
    comments = ListField()


class Page_Posts(EmbeddedDocument):
    post_id = LongField()
    author_username = StringField()
    author_name = StringField()
    media_directory = StringField()
    tags = ListField()
    post_link = URLField()
    associated_links = ListField()
    headline = StringField()
    timestamp = DateTimeField()
    content_type = DictField()
    post_text = StringField()
    picture_links = ListField()
    video_links = ListField()
    reactions_statistics = IntField()
    comments_statistics = IntField()
    shares_statistics = IntField()
    reactions = DictField()
    comments = ListField()
    sentiment = StringField()


class Facebook_Profile_Response_TMS(Document):
    GTR = StringField()
    name = StringField()
    username = StringField()
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
    relationship = StringField()
    family = ListField()
    events = ListField()
    friends = ListField()
    posts = ListField(EmbeddedDocumentField(Facebook_Posts))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        print('.........................................MongoSignal..............................................')

    # comments= DictField()
    # mentions= ListField()
    close_associates = ListField()
    # pictures= ListField()
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
    emotions = ListField()
    target_update_count = LongField()
    linked_to = ListField()


class Facebook_Page_Response_TMS(Document):
    GTR = StringField()
    target_update_count = LongField()
    username = StringField()
    name = StringField()
    target_type = StringField()
    owner = StringField()
    scope = StringField()
    facebook_type = StringField()
    statistics = DictField()
    page_info = ListField()
    contact_information = ListField()
    additional_info = ListField()
    countries_involved = ListField()
    page_history = ListField()
    ads_status = StringField()
    liked_pages = ListField()
    page_posts = ListField(EmbeddedDocumentField(Page_Posts))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        print('.........................................MongoSignal..............................................')

    posting_time_charts = ListField()
    sentiments = ListField()
    behaviour = StringField()
    common_words = ListField()
    close_associates = ListField()
    linked_to = ListField()


class Facebook_Group_Response_TMS(Document):
    GTR = StringField()
    target_update_count = LongField()
    username = StringField()
    name = StringField()
    target_type = StringField()
    description = StringField()
    group_privacy = StringField()
    group_visibility = StringField()
    group_category = StringField()
    group_posting_stats = DictField()
    group_members_stats = DictField()
    group_creator = DictField()
    group_timestamp = DateTimeField()
    group_history = ListField()
    group_rules = ListField()
    group_admins = ListField()
    group_moderators = ListField()
    num_admins = IntField()
    num_moderators = IntField()
    events = ListField()
    page_members = ListField()
    close_associates = ListField()
    posts = ListField()
    posting_time_charts = ListField()
    sentiments = ListField()
    behaviour = StringField()
    common_words = ListField()
    linked_to = ListField()


class Trends(Document):
    trend_type = StringField()
    trend_graph = DictField()
    popular_hashtag = ListField()
    top_Trends = ListField()
    country = StringField()
    wordcloud = ListField()
    common_words = ListField()
    spelling_variants = ListField()


class News(Document):
    GTR = StringField()
    CTR = IntField()
    channel = StringField()
    most_used_hashtags = ListField()
    wordcloud = StringField()
    most_emerging_news = ListField()
    news = ListField()
    common_words = ListField()
    spelling_variants = ListField()



class Dynamic_Crawling_Response_TMS(Document):
    GTR = StringField()
    CTR = IntField()
    name = StringField()
    registrar = StringField()
    creation_date = DateTimeField()
    expiration_date = DateTimeField()
    data = DictField()


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













