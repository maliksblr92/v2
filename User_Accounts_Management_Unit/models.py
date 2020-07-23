from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from mongoengine import *
# Create your models here.
import datetime 



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
    
 