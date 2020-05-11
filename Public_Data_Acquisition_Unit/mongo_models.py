from mongoengine import *
import datetime
from OSINT_System_Core.publisher import publish

DATABASE = ''
USERNAME = ''
PASSWORD = ''
HOST_IP = ''
PORT = ''

disconnect('default')
#CONNECT TO MONGO DB
connect(db='OSINT_System',host='192.168.18.20', port=27017)

#connect('OSINT_System')

#global data tuples

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

LINKEDIN_PROFILE_TYPE = (
    ('Person', ('Person Profile')),
    ('Company', ('Company Profile'))
)

WEBSITE_TYPE = (
    ('social', ('Social Website')),
    ('news', ('News Website')),
    ('blog', ('Blog Website')),
    ('fake', ('Inforced_Crawling'))
)

NEWS_SITES = (
        ('bbc', ('BBC News')),
        ('ary', ('ARY News')),
        ('geo', ('GEO News')),
        ('dawn', ('DAWN News')),
)

#.....................................................................DOCUMENTS COMMON TO ALL Sections...........................................................
class Supported_Website(Document):
    """
    Supporte_Website is a collection which have the detail of the supported sites by the OSINT System.
    It is initialized by a FirstRunner Script on project initialization once.

    """
    name = StringField()
    url = StringField(unique=True)
    website_type = StringField(choices=WEBSITE_TYPE)
    target_type = ListField()

    def __str__(self):
        return self.name+'_'+self.website_type

    def __repr__(self):
        return self.name+'_'+self.website_type

    @staticmethod
    def get_all_social_websites():
        return Supported_Website.objects(website_type='social')

    @staticmethod
    def get_all_news_websites():
        return Supported_Website.objects(website_type='news')

    @staticmethod
    def get_all_blog_websites():
        return Supported_Website.objects(website_type='blog')

    @staticmethod
    def get_all_supported_sites():
        return Supported_Website.objects

    @staticmethod
    def get_target_type_by_index(website_name,index):
        return Supported_Website.objects(name=website_name.capitalize()).first().target_type[int(index)]

class Global_Target_Reference(Document):

    website = ReferenceField(Supported_Website)
    target_type = StringField()
    created_on = DateTimeField(default=datetime.datetime.utcnow())

    """
    def __init__(self,website,target_type_index):

        #sw = Supported_Website.objects(id=website_id)[0]
        super().__init__(website,website.target_type[target_type_index])
        self.save()
    """
    def create(self,website,target_type_index):
        self.website = website
        self.target_type = website.target_type[target_type_index]
        self.save()
        return self.id

    def __str__(self):
        return self.website.name

    def __repr__(self):
        return self.website.name+'_'+self.target_type


    @staticmethod
    def targets_added_all_time():
        return Global_Target_Reference.objects.order_by('-created_on')

    @staticmethod
    def targets_added_today():
        return Global_Target_Reference.objects(Q(created_on__lte=datetime.datetime.utcnow()) & Q(created_on__gte=datetime.datetime.utcnow()-datetime.timedelta(days=1)))

    @staticmethod
    def targets_added_count_by_date_range(start_datetime,end_date):
        return Global_Target_Reference.objects(Q(created_on__gte=start_datetime) & Q(created_on__lte=end_date))

    @staticmethod
    def target_added_count_by_website_type(website_type='social'):
        GTRS = Global_Target_Reference.objects
        objects = []
        for gtr in GTRS:
            if(gtr.website.website_type == website_type):
                objects.append(gtr)

        return objects

    @staticmethod
    def target_added_count_by_website(website_id):
        return Global_Target_Reference.objects(website__id=website_id)

    @staticmethod
    def get_targets_by_website_name_count(website='facebook'):
        GTRS = Global_Target_Reference.objects
        objects = []
        for gtr in GTRS:
            if (gtr.website.name.lower() == website):
                objects.append(gtr)

        return len(objects)

    @staticmethod
    def target_sites_percetage_share():
        total_targets_count = len(Global_Target_Reference.targets_added_all_time())
        sites = Supported_Website.get_all_supported_sites()
        data_resp = []

        for site in sites:
            site_count = Global_Target_Reference.get_targets_by_website_name_count(site.name.lower())
            temp_dict = {site.name.lower():(site_count/total_targets_count)*100}
            data_resp.append(temp_dict)
        return data_resp

    @staticmethod
    def target_count_for_all_sites():
        sites = Supported_Website.get_all_supported_sites()
        data_resp = []

        for site in sites:
            site_count = Global_Target_Reference.get_targets_by_website_name_count(site.name.lower())
            temp_dict = {site.name.lower(): site_count}
            data_resp.append(temp_dict)
        return data_resp


#.....................................................................BASE DOCUMENT SECTION STARTED...........................................................

class Facebook_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """
    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()


    @staticmethod
    def get_all_targets():
        return Facebook_Target.objects.order_by('created_on')

class Youtube_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """
    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()


    @staticmethod
    def get_all_targets():
        return Facebook_Target.objects.order_by('created_on')

class Reddit_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """
    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()


class Twitter_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """

    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()

class Instagram_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """

    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()

class Linkedin_Target(Document):


    GTR = ReferenceField(Global_Target_Reference) # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)

    meta = {'allow_inheritance': True}

    #def __init__(self):
    #    super().__init__()

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """

    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()
#.....................................................................BASE TARGET SECTIONS ENDED.....................................................


#.....................................................................Facebook Targets Sections......................................................

class Facebook_Profile(Facebook_Target):


    user_id = StringField(default='null') # make user_id unique for soul one facebook profile target
    username = StringField(default='null') # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    #def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        #super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']


                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control', module_name=__name__)
                return self
            else:
                #raise Exception('unable to create a facebook profile, username or user_id is not provided')
                #print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a facebook profile, username or user_id is not provided', message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)
    """
    define all the function related to all the profile targets of facebook in the bellow section of this class
    
    """


class Youtube_Channel(Youtube_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',
                        module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                # print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a youtube profile, username or user_id is not provided',
                        message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """


class Facebook_Page(Facebook_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',
                        module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                # print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a facebook page, username or user_id is not provided',
                        message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """

class Facebook_Group(Facebook_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',
                        module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                # print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a facebook Group, username or user_id is not provided',
                        message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """
class Facebook_Search(Facebook_Target):


    url = StringField(default='null')
    target_type = StringField(default='null')
    search_phrase = StringField(default='null')
    search_keywords = ListField(default=[])
    hashtags = ListField(default=[])

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.search_phrase +' '+self.search_keywords+' '+self.hashtags

    def __repr__(self):
        return self.search_phrase +' '+self.convert_list_to_string(self.search_keywords)+' '+self.convert_list_to_string(self.hashtags)

    def create(self, GTR, **kwargs):
        # super().__init__(GTR)
        try:
            if ('search_phrase' in kwargs or 'search_keywords' in kwargs or 'hashtags' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'search_phrase' in kwargs: self.search_phrase = kwargs['search_phrase']
                if 'search_keywords' in kwargs: self.search_keywords = kwargs['search_keywords']
                if 'hashtags' in kwargs: self.hashtags = kwargs['hashtags']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format('facebook search'), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a facebook search, username or user_id is not provided', message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    def convert_list_to_string(self,list):

        str_data = ''
        for item in list:
            str_data  = str_data +' '+ str(item)

        return str_data

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class
    
    """

#.....................................................................Reddit Target Section...............................

class Reddit_Profile(Reddit_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self), message_type='control',
                        module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                # print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a reddit profile, username or user_id is not provided',
                        message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """

class Reddit_Subreddit(Reddit_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)
        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self), message_type='control',
                        module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                # print('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a reddit subreddit, username or user_id is not provided',
                        message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of reddit in the bellow section of this class

    """

#.....................................................................Twitter Targets Sections...........................................................

class Twitter_Profile(Twitter_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:

            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a twitter profile, username or user_id is not provided', message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)
    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """

#.....................................................................Instagram Targets Sections...........................................................

class Instagram_Profile(Instagram_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')

    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:
            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'url' in kwargs: self.url = kwargs['url']
                # if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a instagram profile, username or user_id is not provided', message_type='warning', module_name=__name__)
                return None
        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)
    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """
#.....................................................................Linkedin Targets Sections...........................................................

class Linkedin_Profile(Linkedin_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')
    #profile_type = StringField(default='person')
    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:

            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                if 'profile_type' in kwargs: self.profile_type = kwargs['profile_type']
                if 'url' in kwargs: self.url = kwargs['url']
                #if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a linkedin profile, username or user_id is not provided',message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """


class Linkedin_Company(Linkedin_Target):
    user_id = StringField(default='null')  # make user_id unique for soul one facebook profile target
    username = StringField(default='null')  # make username unique for soul one facebook profile target
    name = StringField(default='null')
    url = StringField(default='null')
    target_type = StringField(default='null')
    #profile_type = StringField(default='person')
    # def __init__(self):
    #    super().__init__()

    def __str__(self):
        return self.username if self.username != 'null' else self.user_id

    def __repr__(self):
        return self.username if self.username != 'null' else self.user_id

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:

            if ('user_id' in kwargs or 'username' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'user_id' in kwargs: self.user_id = kwargs['user_id']
                if 'username' in kwargs: self.username = kwargs['username']
                if 'name' in kwargs: self.name = kwargs['name']
                #if 'profile_type' in kwargs: self.profile_type = kwargs['profile_type']
                if 'url' in kwargs: self.url = kwargs['url']
                #if 'target_type' in kwargs : self.target_type = kwargs['target_type']

                self.GTR = GTR
                self.target_type = GTR.target_type
                super().initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.username), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a linkedin profile, username or user_id is not provided',message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    """
    define all the function related to all the profile targets of facebook in the bellow section of this class

    """

#.....................................................................Custom Targets Sections...........................................................

class Keybase_Crawling(Document):

    GTR = ReferenceField(Global_Target_Reference)  # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)
    target_type = StringField(default='keybase_crawling')

    title = StringField()
    keybase_ref = DynamicField()



    def __str__(self):
        return str(self.keybase_ref.title)

    def __repr__(self):
        return str(self.keybase_ref.title)

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:

            if ('keybase_ref' in kwargs or 'title' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'title' in kwargs: self.title = kwargs['title']
                if 'keybase_ref' in kwargs: self.keybase_ref = kwargs['keybase_ref']


                self.GTR = GTR
                self.target_type = GTR.target_type
                self.initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.title), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a dynamic crawling target, url or title is not provided', message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    def make_me_expire(self):
        self.is_expired = True
        self.save()

class Dynamic_Crawling(Document):

    GTR = ReferenceField(Global_Target_Reference)  # GTR should be unique for each facebook target
    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    need_screenshots = BooleanField(default=False)

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    expired_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    periodic_interval = IntField(default=0, choices=PERIODIC_INTERVALS)
    target_type = StringField(default='dynamic_crawling')

    title = StringField()
    url = StringField()
    ip = BooleanField()
    domain = BooleanField()
    pictures = BooleanField()
    videos = BooleanField()
    headings = BooleanField()
    paragraphs = BooleanField()
    links = BooleanField()

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return str(self.title)

    def create(self, GTR, kwargs):
        # super().__init__(GTR)

        try:

            if ('url' in kwargs or 'title' in kwargs):
                # if(kwargs['user_id'] is not None or kwargs['username'] is not None):
                # above condition confirms that username or user_id must be there to create a profile target

                if 'title' in kwargs: self.title = kwargs['title']
                if 'url' in kwargs: self.url = kwargs['url']
                if 'ip' in kwargs: self.ip = kwargs['ip']
                if 'domain' in kwargs: self.domain = kwargs['domain']
                if 'videos' in kwargs: self.videos = kwargs['videos']
                if 'headings' in kwargs: self.headings = kwargs['headings']
                if 'paragraphs' in kwargs: self.paragraphs = kwargs['paragraphs']
                if 'links' in kwargs: self.links = kwargs['links']
                if 'pictures' in kwargs: self.pictures = kwargs['pictures']

                self.GTR = GTR
                self.target_type = GTR.target_type
                self.initialize_basic(kwargs)

                self.save()
                publish('target for {0} created successfully'.format(self.title), message_type='control',module_name=__name__)
                return self
            else:
                # raise Exception('unable to create a facebook profile, username or user_id is not provided')
                publish('unable to create a dynamic crawling target, url or title is not provided', message_type='warning', module_name=__name__)
                return None

        except Exception as e:
            publish(str(e), message_type='error', module_name=__name__)

    def initialize_basic(self,kwargs):

        # initializing default attributes

        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'need_screenshots' in kwargs: self.need_screenshots = kwargs['need_screenshots']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expired_on' in kwargs: self.expired_on = kwargs['expired_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']
        if 'periodic_interval' in kwargs: self.periodic_interval = kwargs['periodic_interval']

    """
    define all the function related to all the targets of facebook in the bellow section of this class
    """
    def am_i_expired(self):
        return self.is_expired

    def make_me_expire(self):
        self.is_expired = True
        self.save()
#.....................................................................Periodic Targets Models...........................................................

class Periodic_Targets(Document):
    GTR = ReferenceField(Global_Target_Reference)
    CTR = IntField(default=0)
    target_reff = DynamicField()
    re_invoke_time = DateTimeField(default=datetime.datetime.utcnow())


    def __str__(self):
        return str(self.GTR.name)

    def __repr__(self):
        return str(self.target_reff.username)

    @staticmethod
    def get_all_periodic_task():
        return Periodic_Targets.objects

class Share_Resource(Document):

    share_with = ListField()
    seen = BooleanField(default=False)
    processed = BooleanField(default=False)
    user_id = IntField()
    username = StringField()


    resource_ref = DynamicField()
    message = StringField()

    created_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())


    @staticmethod
    def get_pao_resources():
        return Share_Resource.objects(share_with='pao')

    @staticmethod
    def get_rdo_resources():
        return Share_Resource.objects(share_with='rdo')

class Rabbit_Messages(Document):

    message_type = StringField(default='info')
    message_data = DictField()
    created_on = DateTimeField(default=datetime.datetime.utcnow())


    @staticmethod
    def get_all_messages():
        return Rabbit_Messages.objects()

    @staticmethod
    def get_messages_with_date_range(start,end):
        return Rabbit_Messages.objects(Q(created_on__gte=start) & Q(created_on__lte=end))

    @staticmethod
    def get_top_messages(top=10,message_type='message'):
        return Rabbit_Messages.objects(message_type=message_type).order_by('-id')[:top]



class Timeline_Posts(Document):

    target_site = StringField()
    target_type = StringField()
    gtr_id = StringField(unique=True)

    username = StringField(unique=True)
    title = StringField()
    posts = ListField()
    all_seen = BooleanField(default=False)
    seenn_indexes = ListField() # it stores the indexes of the "posts list field" indexes in this list will considered seen


    @staticmethod
    def get_qualified_objects():
        """
        qulified objects are those objects which have atleast one unseen post

        :return: objects
        """

        qualified_objs = []

        tl_objs = Timeline_Posts.objects(all_seen=False)
        for obj in tl_objs:
            for post in obj.posts:
                if(not post['seen']):
                    qualified_objs.append(obj)


        return qualified_objs

    @staticmethod
    def get_qualified_posts(top=10):
        """
        qulified objects are those objects which have atleast one unseen post

        :return: objects
        """

        qualified_posts = []

        tl_objs = Timeline_Posts.objects()
        count = 0

        for obj in tl_objs:


            for post in obj.posts:



                if (not post['seen']):
                    count = count +1
                    qualified_posts.append(post)
                    post['seen'] = True
                    obj.save()

                if (count >= top):
                    break

        return qualified_posts
