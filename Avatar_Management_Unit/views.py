from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import reverse,render
from bson import ObjectId
from Avatar_Management_Unit.models import *
import datetime


class Create_Avatar(View):

    def get(self,request,*args,**kwargs):

        return HttpResponse('on Create avatar')

    def post(self,request):
        a = Avatar_AMS()


        a.create('awaisazam230@gmail.com',first_name='awais',last_name='azam',gender='male',marital_status='single')


        return HttpResponse('on Create avatar')


class Add_Work(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")
        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            a.add_work('sky scraper',datetime.date.today(),datetime.date.today(),'islamabad','do it right','anycomp pvt ltd')

            return HttpResponse('work added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

class Add_Education(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")
        institute = 'the gramar school'
        degree = 'matric'
        grades = 'a'
        field_of_study = ''
        start_date = ''
        end_date = ''

        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            if(a is not None):
                a.add_education(institute,degree,grades,field_of_study,start_date,end_date)

            return HttpResponse('work added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

class Add_Skill(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")

        name = 'painter'
        level = '3'
        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            if(a is not None):
                a.add_skills(name,level)

            return HttpResponse('skill added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

class Add_Interest(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")

        category = 'arts'
        name = 'painting'
        link = 'www.url.com'

        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            if(a is not None):
                a.add_interests(category,name,link)

            return HttpResponse('interst added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

class Add_Life_Event(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")

        year = '2008'
        event = 'birthday'

        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            if(a is not None):
                a.add_life_events(year,event)

            return HttpResponse('event added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

class Add_Social_Account(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")

        social_media_type = 'facebook'
        username = 'awais.a'
        password = 'abc123def'

        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            a.add_social_accounts(social_media_type,username,password)

            return HttpResponse('account added')
        except Exception as e:
            print(e)
            return HttpResponse(e)

#.............................................Views For Avatar Actions.................................................

class Schedule_Action_Post(View):

    def get(self, request, *args, **kwargs):

        action_type = ACTION_TYPE
        account_types_supported = None

        return HttpResponse('on Schedule An Action View')

    def post(self, request):

        avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")
        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)

            account_type = 'facebook'
            title = 'happy eid'
            description = 'on special day of eid'
            account_credentials = Avatar_AMS.get_social_account(a, account_type)
            type = 'post'

            #temp variables

            text = 'post text'
            reaction = 'love'
            post_url = ''
            social_media = account_credentials.social_media_type
            username = account_credentials.username
            password = account_credentials.password

            data = {'text':text,'reaction':reaction,'target_post':post_url,'social_media':social_media,'username':username,'password':password}

            act_s = Action_Schedule_AMS(title=title,description=description,account_credentials=account_credentials,data=data,type=type)
            act_s.save()

            return HttpResponse('account added')
        except Exception as e:
            print(e)
            return HttpResponse(e)