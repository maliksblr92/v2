from django.db import models

# Create your models here.
from mongoengine import *
import datetime
# -------------------------------------------------------- connection ------------------------------------------------------
disconnect('default')
#CONNECT TO MONGO DB
#connect(db='OSINT_System',host='192.168.18.20', port=27017)


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
    current = BooleanField(required=True)



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
    hobbies = ListField(StringField())
    movies = ListField(StringField())
    songs = ListField(StringField())



class Location(EmbeddedDocument):
    location = StringField(max_length=500)
    details = StringField(max_length=500)



class LifeEvent(EmbeddedDocument):
    year = DateField()
    event = StringField(max_length=1000)




class SocialMediaAccount(EmbeddedDocument):
    social_media_type = StringField(choices=SOCIAL_MEDIA_TYPE)
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    password = StringField()
    phone_number = StringField()
    username = StringField()
    dob = DateField()
    gender = StringField()


class SocialMediaPost(EmbeddedDocument):
    social_media_type = StringField(choices=SOCIAL_MEDIA_TYPE)
    post_text = StringField()
    post_date = DateField()

class Marriage(EmbeddedDocument):
    spouse = StringField(required=True)
    location = StringField()
    wedding_date = DateField(required=True)
    divorce_date = DateField()

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
    # address = StringField(min_length=10)
    address = StringField()
    # nationality = StringField(min_length=5)
    nationality = StringField()

    works= ListField(default=[])
    educations = ListField(default=[])
    skills = ListField(default=[])
    interests = DictField()
    locations = ListField(default=[])
    life_events = ListField(default=[])
    social_media_accounts = ListField(default=[])
    marriages = EmbeddedDocumentListField(Marriage)
    biography = ListField(StringField())
    social_media_posts = EmbeddedDocumentListField(SocialMediaPost)


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
        if 'address' in kwargs: self.address = kwargs['address']
        if 'nationality' in kwargs: self.nationality = kwargs['nationality']

        self.evaluate_health()

    def add_work(self, title, company, location, description,
                 start_date, end_date, is_current):

        work = Work(
            title=title,
            start_date=start_date,
            end_date=end_date,
            location=location,
            description=description,
            company=company,
            current=is_current)
        self.works.append(work)
        self.correct_current_job(work)
        self.evaluate_health()
        return 'true'

    def add_education(self, institute, degree, grades,
                      field_of_study, start_date, end_date):

        education = Education(
            institute,
            degree,
            grades,
            field_of_study,
            start_date,
            end_date)
        self.educations.append(education)
        self.evaluate_health()
        return 'true'


    def add_skills(self,name,level):
        skill = Skill(name,level)
        self.skills.append(skill)
        self.evaluate_health()

    def add_interests(self, hobbies, movies, songs):
        # print(self.interests, hobbies, movies, songs)
        if self.interests:
            # print('interest if')
            self.interests['hobbies'].extend(hobbies)
            self.interests['movies'].extend(movies)
            self.interests['songs'].extend(songs)
        else:
            # print('interest else')
            self.interests = {
                'hobbies': hobbies,
                'movies': movies,
                'songs': songs
            }
        
        #self.save()
        self.evaluate_health()
        return 'true'

    def add_life_events(self,year,event):
        event = LifeEvent(year,event)
        self.life_events.append(event)
        self.evaluate_health()
        return 'true'

    def add_biography(self, biography):
        self.biography.append(biography)
        self.save()
        return 'true'
#added password in the dictionary
    def add_social_accounts(self, social_media_type, first_name,
                            last_name, email, password,phone_number, username, dob, gender):
        social_account = SocialMediaAccount(
            social_media_type, first_name,
            last_name, email,password, phone_number, user_name, dob, gender)
        self.social_media_accounts.append(social_account)
        self.evaluate_health()
        return 'true'

    def add_social_post(self, social_media_type, post, post_date):
        social_post = SocialMediaPost(social_media_type, post, post_date)
        self.social_media_posts.append(social_post)
        self.save()
        return 'true'

    def add_marriage(self, spouse, location, wedding_date, divorce_date):
        # print(spouse, location, wedding_date, divorce_date)
        marriage = Marriage(spouse, location, wedding_date, divorce_date)
        # print(self.first_name)
        # print(self.marriages)
        # self.marriages.append(marriage)
        if self.marriages.count():
            print('marriage if')
            self.marriages.append(marriage)
        else:
            print('marriage else')
            self.marriages = []
            self.marriages.append(marriage)
        self.evaluate_health()
        return 'true'
    
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
    
    def correct_current_job(self, correct_current_job_id):
        """
        This method is for the case when multiple jobs were added for an avatar
        and 1 of them was current job, now another new current job is added,
        which means the previous current job has to be converted to past job.
        """
        pass

    @staticmethod
    def get_all_avatars_id_and_names():
        return Avatar_AMS.objects().fields(first_name=1, last_name=1)
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
