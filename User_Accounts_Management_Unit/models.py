from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from mongoengine import *
from django.contrib.auth.models import User
# Create your models here.
import datetime 



class User_Profile_Manager(models.Manager):
    # create a new user profile 
    def create_user_profile(self,user_id,address,contact,rank,description,dob,cnic,employee_number,profile_pic):
            user_profile = self.create(
                                user_id=user_id,
                                address=address,
                                rank=rank,
                                description=description,
                                contact=contact,
                                dob=dob,
                                cnic=cnic,
                                employee_number=employee_number,
                                profile_pic=profile_pic)
            user_profile.save()
            if user_profile:
                return True
            else: 
                return False
    # get a single user profile   by id 
    @staticmethod
    def getUserProfile(id):
       Fetched_User_Profile=User_Profile.objects.get(id=id)
       return Fetched_User_Profile 
      # delete a single user profile   by id 
    @staticmethod
    def deleteUserProfile(id):
        Deleteable_User_Profile=User_Profile.objects.get(id=id)
        if(Deleteable_User_Profile):
            Deleteable_User_Profile.delete()
            return True
        else:
            return False
    #  getupdate a single user profile  
    @staticmethod
    def getUpdateProfile(id,address,contact,rank,description,dob,cnic,employee_number,profile_pic):
       
       try:
           Update_User_Profile=User_Profile.objects.filter(id = id).update(
           address=address,
           contact=contact,
           rank=rank,
           description=description,
           dob=dob,
           cnic=cnic,
           employee_number=employee_number,
           profile_pic=profile_pic
           )
           if Update_User_Profile:
                return Update_User_Profile 
           else:
                return False
       except Exception as e:
           return False
       


class User_Profile(models.Model):
    # user_id = models.ForeignKey('auth.User', unique=True ,on_delete=models.CASCADE,)
    user_id=models.OneToOneField(User,unique=True ,on_delete=models.CASCADE,default='EMPTY')
    address=models.CharField(max_length=200,null=True,blank=True)
    rank=models.CharField(max_length=200,null=True,blank=True)
    description=models.CharField(max_length=400,null=True,blank=True)
    contact=models.CharField(max_length=200,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    cnic=models.CharField(max_length=200,null=True,blank=True)
    profile_pic=models.ImageField(null=True,blank=True)
    employee_number=models.CharField(max_length=200,null=True,blank=True)
    objects = User_Profile_Manager()
    def __str__(self):
        return self.cnic
    
           