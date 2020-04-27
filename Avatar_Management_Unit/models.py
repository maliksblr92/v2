from django.db import models

# Create your models here.
from mongoengine import *
import datetime
# -------------------------------------------------------- connection ------------------------------------------------------
disconnect('default')
#CONNECT TO MONGO DB
connect(db='OSINT_System',host='192.168.18.20', port=27017)


SOCIAL_MEDIA_TYPE = (

    ('facebook', ('Facebook')),
    ('twitter', ('Twitter')),
    ('instagram', ('Instagram')),
    ('linkedin', ('Linkedin')),
    ('reddit', ('Reddit')),
)

ACTION_TYPE = (

    ('post', ('Post')),
    ('comment', ('Comment')),
    ('reaction', ('Reaction')),
    ('share', ('Share')),

)

ACTION_STATUS = (

    ('performed', ('Performed Sucessfully')),
    ('error', ('Not Performed Due To Error')),

)
# ------------------------------------------------------- Avatar Entity ---------------------------------------------------------------------




class Work(EmbeddedDocument):
    title = StringField(max_length=300)
    start_date = DateField()
    end_date = DateField()
    location = StringField(max_length=300)
    description = StringField(max_length=500)
    company = StringField(max_length=100)




class Education(EmbeddedDocument):
    institution = StringField(max_length=500)
    degree = StringField(max_length=500)
    grades = StringField(max_length=100)
    field_of_study = StringField(max_length=100)
    start_date = DateField()
    end_date = DateField()




class Skill(EmbeddedDocument):
    name = StringField(max_length=200)
    level = StringField(max_length=100)




class Interest(EmbeddedDocument):
    category = ListField(StringField(max_length=100))
    name = StringField()
    link = StringField()



class Location(EmbeddedDocument):
    location = StringField(max_length=500)
    details = StringField(max_length=500)



class LifeEvent(EmbeddedDocument):
    year = DateField()
    event = StringField(max_length=1000)




class SocialMediaAccount(EmbeddedDocument):
    social_media_type = StringField(choices=SOCIAL_MEDIA_TYPE)
    username = StringField()
    password = StringField()


class Avatar_AMS(Document):
    health = IntField(min_value=0, max_value=100, default=0)

    first_name = StringField(max_length=200)
    last_name = StringField(max_length=200)
    gender = StringField(max_length=200)
    marital_status = StringField(max_length=200)
    birthday = DateField()
    languages = ListField(StringField(max_length=100))
    religious_views = StringField(max_length=500)
    email = EmailField(required=True)
    phone_number = StringField(max_length=20)
    profile_image = ImageField()
    cover_image = ImageField()

    works= ListField(default=[])
    educations = ListField(default=[])
    skills = ListField(default=[])
    interests = ListField(default=[])
    locations = ListField(default=[])
    life_events = ListField(default=[])
    social_media_accounts = ListField(default=[])


    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email





    def evaluate_health(self):

        self.health = 0

        self.health = 52 #just for basic profile

        if (len(self.works) > 0): self.health += 8
        if(len(self.educations) > 0 ): self.health += 7
        if (len(self.skills) > 0): self.health += 3
        if (len(self.interests) > 0): self.health += 5
        if (len(self.locations) > 0): self.health += 8
        if (len(self.life_events) > 0): self.health += 5
        if (len(self.social_media_accounts) > 0): self.health += 2

        self.save()

    def create(self,email,**kwargs):
        self.email = email

        if 'first_name' in kwargs : self.first_name = kwargs['first_name']
        if 'last_name' in kwargs: self.last_name = kwargs['last_name']
        if 'gender' in kwargs: self.gender = kwargs['gender']
        if 'marital_status' in kwargs: self.marital_status = kwargs['marital_status']
        if 'birthday' in kwargs: self.birthday = kwargs['birthday']
        if 'languages' in kwargs: self.languages = kwargs['languages']
        if 'religious_views' in kwargs: self.religious_views = kwargs['religious_views']
        if 'email' in kwargs: self.email = kwargs['email']
        if 'profile_image' in kwargs: self.profile_image = kwargs['profile_image']
        if 'cover_image' in kwargs: self.cover_image = kwargs['cover_image']

        self.evaluate_health()

    def add_work(self,title,start_date,end_date,location,description,company):

        work = Work(title=title,start_date=start_date,end_date=end_date,location=location,description=description,company=company)
        self.works.append(work)
        self.evaluate_health()

    def add_education(self,institute,degree,grades,field_of_study,start_date,end_date):

        education = Education(institute,degree,grades,field_of_study,start_date,end_date)
        self.educations.append(education)
        self.evaluate_health()


    def add_skills(self,name,level):
        skill = Skill(name,level)
        self.skills.append(skill)
        self.evaluate_health()

    def add_interests(self,category,name,link):
        interest = Interest(category,name,link)
        self.interests.append(interest)
        #self.save()
        self.evaluate_health()

    def add_life_events(self,year,event):
        event = LifeEvent(year,event)
        self.life_events.append(event)
        self.evaluate_health()


    def add_social_accounts(self,social_media_type,username,password):
        social_account = SocialMediaAccount(social_media_type,username,password)
        self.social_media_accounts.append(social_account)
        self.evaluate_health()

    def get_avatar_health(self):
        return self.health

    @staticmethod
    def get_all_avatars():
        return Avatar_AMS.objects()

    @staticmethod
    def search_avatars(text):
        return Avatar_AMS.objects.search_text(text)

    @staticmethod
    def get_object_by_id(object_id):
        return Avatar_AMS.objects(id=object_id).first()

    @staticmethod
    def get_action_supported_avatar(account_type='facebook'):
        ava_list = []
        avatars = Avatar_AMS.objects()
        for avatar in avatars:
            if(len(avatar.social_media_accounts)>0):
                social_accounts = avatar.social_media_accounts
                for account in social_accounts:
                    if(account.social_media_type == account_type):
                        ava_list.append(avatar)

        return ava_list

    @staticmethod
    def get_social_account(avatar,account_type='facebook'):
        social_accounts = avatar.social_media_accounts
        for account in social_accounts:
            if (account.social_media_type == account_type):
                return account

    @staticmethod
    def get_all_social_accounts(avatar):
        return avatar.social_media_accounts

    meta = {'indexes': [
        {'fields': ['$first_name', "$last_name"],
         'default_language': 'english',
         'weights': {'first_name': 10, 'last_name': 2}
         }
    ]}

    @staticmethod
    def find_object(query):
        return Avatar_AMS.objects.search_text(query)
# ----------------------------------------------------------- Avatar Actions -----------------------------------------------



class Action_Schedule_AMS(Document):

    title = StringField()
    description = StringField()
    account_credentials = DynamicField() #ListField() # 0 : social_media_type, 1 : username
    data = DictField()

    type = StringField(choices=ACTION_TYPE)
    status = StringField(choices=ACTION_STATUS)
    expired = BooleanField(default=False)
    performed = BooleanField(default=False)

    perform_on = DateTimeField(default=datetime.datetime.utcnow())
    created_on = DateTimeField(default=datetime.datetime.utcnow())


    def __str__(self):
        return self.title +', type :'+ self.type

    def __repr__(self):
        return self.title +', type :'+ self.type

    def expire_me(self):
        self.expired = True
        self.save()



    @staticmethod
    def get_all_expired_actions():
        return Action_Schedule_AMS.objects(expired=True)

    @staticmethod
    def get_all_active_actions():
        return Action_Schedule_AMS.objects(expired=False)

    @staticmethod
    def get_all_actions():
        return Action_Schedule_AMS.objects()



"""
class AvatarAction(Document):
    avatar_id = UUIDField()
    avatar_time = DateTimeField()
    action_type = StringField(max_length=100)
    action_status = StringField(max_length=100)


class Post(AvatarAction):
    text = StringField(max_length=1000)
    image = ImageField()


class Reaction(AvatarAction):
    target_post = StringField()


class Comment(Reaction):
    text = StringField(max_length=400)


class Like(Reaction):
    sentiment = StringField(max_length=100)


class Share(Reaction):
    text = StringField(max_length=200)

"""