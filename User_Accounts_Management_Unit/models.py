from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from mongoengine import *
# Create your models here.
import datetime 

# class AppUserManager(BaseUserManager):
#     def create_user(self,email,username,password=None):
#         if not email:
#             raise ValueError("User Must have an email address")
#         if not username:
#             raise ValueError("Users must have a username")
#         user=self.model(
#         # normilize converts all charachter to lower case
#         email=self.normilize_email(email),
#         username=username,
#     )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self,email,username,password):
#         user=self.model(
#             email.self.normilize_email(email),
#             password=password,
#             username=username,
#         )
#         user_is_admin=True
#         user._is_staff=True
#         user.is_superuser=True
#         user.save(using=self._db)
#         return user



class User_Profile_Manager(models.Manager):
    def create_user_profile(self,first_name,last_name,current_address,permanent_address,profile_pic):
            user_profile = self.create(
                               first_name=first_name,
                               last_name=last_name,
                               current_address=current_address,
                               permanent_address=permanent_address,
                               profile_pic=profile_pic)
            user_profile.save()
            if user_profile:
                return True
            else: 
                return False
    


class User_Profile(models.Model):
    first_name=models.EmailField(max_length=30)
    last_name=models.CharField(max_length=30)
    current_address=models.CharField(max_length=200)
    permanent_address=models.CharField(max_length=200)
    profile_pic=models.CharField(max_length=200)
    objects = User_Profile_Manager()
    def __str__(self):
        return self.first_name
    
    # USERNAME_FIELD='username'
    # REQUIRED_FIELDS=['username',]
    # objects=AppUserManager()
    
    
    # def has_perm(self,perm,obj=None):
    #     return self.is_admin

    # def has_module_perms(self,app_label):
    #     return True
    
    
    # class Apps_Users(Document):
    #     username = StringField(default='')
    #     email = StringField(default='')
    #     password= StringField(default='')
    #     date_joined = StringField(default='')
    #     last_login = DateTimeField(default=datetime.datetime.utcnow())
    #     is_admin = BooleanField(default=True)
    #     is_active = BooleanField(default=True)
    #     is_staff = BooleanField(default=False)
    #     is_superuser=BooleanField(default=True)
    #     created_on = DateTimeField(default=datetime.datetime.utcnow())
    #     updated_on = DateTimeField(default=datetime.datetime.utcnow())
    # # expire_on = DateTimeField(default=datetime.datetime.utcnow()+ datetime.timedelta(days=30))




    # def __str__(self):
    #     return self.email

    # def __repr__(self):
    #     return self.username

    # def create(self,username,email,password,last_login,is_admin,is_active,is_staff,is_superuser,kwargs):
    #     # if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        
    #     Email=self.normilize_email(email)
    #     Username=self.normalize_username(username)
    #     Password=self.set_password(password)
    #     self.username = username
    #     self.email = Email
    #     self.password = Username
    #     self.last_login = last_login
    #     self.is_admin = is_admin
    #     self.is_active = is_active
    #     self.is_staff = is_staff
    #     self.is_superuser = is_superuser
        

    #     self.save()

    # meta = {'indexes': [
    #     {'fields': ['$title', "$topic"],
    #      'default_language': 'english',
    #      'weights': {'title': 10, 'topic': 2}
    #      }
    # ]}

    # @staticmethod
    # def find_object(query):
    #     return Keybase_KMS.objects.search_text(query)
