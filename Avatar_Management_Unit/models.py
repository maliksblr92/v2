from django.db import models

# Create your models here.
from mongoengine import *

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


# ------------------------------------------------------- Avatar Entity ---------------------------------------------------------------------




class Work(EmbeddedDocument):
    title = StringField(max_length=300)
    start_date = DateField()
    end_data = DateField()
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


class Avatar(Document):
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

    works= ListField(EmbeddedDocumentField(Work))
    educations = ListField(EmbeddedDocumentField(Work))
    skills = ListField(EmbeddedDocumentField(Work))
    interests = ListField(EmbeddedDocumentField(Work))
    locations = ListField(EmbeddedDocumentField(Work))
    life_events = ListField(EmbeddedDocumentField(Work))
    social_media_accounts = ListField(EmbeddedDocumentField(Work))

    def evaluate_health(self):
        pass


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

        self.save()


    def add_work(self,title,start_date,end_date,location,description,company):

        work = Work(title,start_date,end_date,location,description,company)
        self.works.append(work)
        self.save()

    def add_education(self,institute,degree,grades,field_of_study,start_date,end_date):

        education = Education(institute,degree,grades,field_of_study,start_date,end_date)
        self.educations.append(education)
        self.save()


    def add_skills(self,name,level):
        skill = Skill(name,level)

    def add_interests(self,category,name,link):
        interest = Interest(category,name,link)
        self.interests.append(interest)
        self.save()

    def add_life_events(self,year,event):
        event = LifeEvent(year,event)
        self.life_events.append(event)
        self.save()


    def add_social_accounts(self,social_media_type,username,password):
        social_account = SocialMediaAccount(social_media_type,username,password)
        self.social_media_accounts.append(social_account)
        self.save()


# ----------------------------------------------------------- Avatar Actions -----------------------------------------------


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