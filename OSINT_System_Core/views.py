from django.shortcuts import render
from django.contrib.auth.models import User, Group
from Data_Processing_Unit.tasks import fetch_instagram_person, fetch_twitter_tweets
from datetime import timedelta
from Data_Processing_Unit import tasks
from .mixins import RequireLoginMixin, IsTSO, IsTMO, IsRDO, IsPAO
from bson import ObjectId
# from OSINT_System_Core.models import Supported_Socail_Sites
# from OSINT_System_Core.serializers import Supported_Socail_Sites_Serializer
# from OSINT_System_Core.core_db_manager import Coredb_Manager

from rest_framework.views import APIView
from django.http import JsonResponse

# imports for the find objects view

from Keybase_Management_System.models import Keybase_KMS
from Portfolio_Management_System.models import Portfolio_PMS
from Avatar_Management_Unit.models import Avatar_AMS

from django.http import HttpResponse, HttpResponseRedirect
from Data_Processing_Unit.processing_manager import Processing_Manager
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from django.shortcuts import reverse, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from Data_Processing_Unit import tasks
import datetime
from django.utils import timezone
from django_eventstream import send_event
from Public_Data_Acquisition_Unit.mongo_models import Rabbit_Messages

from bs4 import BeautifulSoup
import requests
import json
from OSINT_System_Core.core_manager import Update_Bigview
import time
import os
from Data_Processing_Unit.models import News
from Data_Processing_Unit.models import Trends
from django.core import serializers
from django.shortcuts import get_object_or_404
from mongoengine.queryset.visitor import Q
from Public_Data_Acquisition_Unit.mongo_models import Global_Target_Reference
from System_Log_Management_Unit.system_log_manager import System_Stats
# djangorestframework moduels below
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import viewsets, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from OSINT_System_Core.Data_Sharing import Keybase_Match, Portfolio_Link, Portfolio_Include, Keybase_Include, \
    Mongo_Lookup
from Public_Data_Acquisition_Unit.mongo_models import Share_Resource as Share_Resource_M
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

# Create your views here.

# processing_manager = Processing_Manager()
acq = Acquistion_Manager()
# coreDb = Coredb_Manager()
log_manager = ""
pl = Portfolio_Link()
pi = Portfolio_Include()
km = Keybase_Match()
ss = System_Stats()

# FACEBOOK_AUT,TWITTER_AUT,INSTAGRAM_AUT,NEWS_AUT,PERIODIC_INT,SEARCH_TYPE_TWITTER,TWEETS_TYPE,LINKEDIN_AUT= coreDb.get_author_types_all()


class Main(View):
    def get(self, request):
        # response = fetch_instagram_profile('author','atifaslam')   #author or post
        # response =  acq_manager.ess_add_facebook_person_target('prince.nuada.16','closeAssociates')
        # response = acq_manager.ess_add_instagram_target('author','atifaslam')
        # response = acq_manager.ess_add_linkedin_person_target()
        # response = acq_manager.ess_add_linkedin_company_target('facebook')

        # response = acq_manager.ess_add_twitter_phrase_target('PSL')
        # response = fetch_twitter_tweets('refferencing','itsaadee')
        # return JsonResponse(response,safe=False)
        # print(processing_manager.fetch_news())

        eta = datetime.datetime.now() + datetime.timedelta(seconds=40)
        tasks.add.schedule((4, 5), eta=eta)

        return render(request, 'OSINT_System_Core/main.html', {})


# ...........................................Views for Target Forms.......


class Target_Author_Instagram(View):
    def get(self, request):
        return render(
            request,
            'OSINT_System_Core/target_submission_instagram.html',
            {})


class Target_Author_Facebook(View):
    def get(self, request):
        return render(
            request,
            'OSINT_System_Core/target_submission_facebook.html',
            {})


class Target_Author_Twitter(View):
    def get(self, request):
        return render(
            request,
            'OSINT_System_Core/target_submission_twitter.html',
            {})


class Target_Author_Linkedin(View):
    def get(self, request):
        return render(
            request,
            'OSINT_System_Core/target_submission_linkedin.html',
            {})


class Target_Headlines_Main(View):
    def get(self, request):
        # send_event('test', 'message', {'text': 'hello world'})

        return render(
            request,
            'OSINT_System_Core/sources_target_headlines_main.html',
            {})


"""

#...........................................Views for Target Submission.............................................
#@method_decorator(csrf_exempt,name='dispatch')
class News_Target(APIView):
    #view class to submit news targets here

    #permission_classes = (IsAuthenticated,)

    def get(self,request):
        #coreDb.insert_news_target(3,'bbc',10,'News_Target',5,True,True,5)

        author_type_choice,news_site_choice,periodic_interval_choice = coreDb.get_choices_list_all()

        sss = coreDb.get_supported_social_sites_list()
        sss_list = list(sss)


        form_data = {'news_target_form':{'author_types':NEWS_AUT,'intervals':periodic_interval_choice}}
        #return JsonResponse(form_data,safe=False)
        return Response(form_data)

    def post(self,request):
        #sss_id = request.POST.get('sss_id',None)
        #news_site = request.POST.get('news_site',None)

        #is_enabled = request.POST.get('is_enabled', None)
        #is_expired = request.POST.get('is_expired', None)

        author_type = request.data.get('author_type', None)
        top = request.data.get('top', None)
        expired_on = request.data.get('expired_on', None)
        periodic_interval = request.data.get('periodic_interval')

        if(author_type and top and expired_on and periodic_interval):
            #above condition checks to see if any of the parameter is not empty

            #convert data type as required
            # is_enabled = True if is_enabled == 1 else False
            # is_expired = True if is_expired == 1 else False
            #sss_id = int(sss_id)

            top = int(top)
            expired_on = int(expired_on)
            periodic_interval = int(periodic_interval)

            result =  'ok' #coreDb.insert_news_target(sss_id, news_site, top, author_type, expired_on, is_enabled, is_expired, periodic_interval)

            if(result is not None):
                return Response({'response':'target submitted successfully'})
        return Response({'response':'system is unable to submit target'})


@method_decorator(csrf_exempt, name='dispatch')
class Add_Instagram_Target(APIView):

    #class to add targets of instagram to the system

    #permission_classes = (IsAuthenticated,)

    def get(self,request):

        form_data = {'instagram_target_form': {'author_types': INSTAGRAM_AUT , 'intervals': PERIODIC_INT}}
        # return JsonResponse(form_data,safe=False)
        return JsonResponse(form_data)


    def post(self,request):

        print(request.data)
        author_type = request.data.get('author_type', None)

        need_screenshots = request.data.get('need_screenshots',None)
        expired_on = request.data.get('expired_on', None)
        print(expired_on)
        expired_on = convert_expired_on_to_datetime(expired_on)
        periodic_interval = request.data.get('periodic_interval')

        if(author_type == 'instagram_person'):
            author_id = request.data.get('author_id',None)
            author_account = request.data.get('author_account', None)
            author_name = request.data.get('author_name', None)
            author_url = request.data.get('author_url', None)

            print(author_type, author_name, author_account, author_url, expired_on, need_screenshots, periodic_interval)
            periodic_interval = int(periodic_interval)
            if(author_id and author_account and author_name and author_url):
                coreDb.insert_instagram_person_target(author_type,author_id,author_account,author_name,author_url,need_screenshots,expired_on,periodic_interval)
                return JsonResponse({'response': 'success submitted','status':'200'})

            else:
                return JsonResponse({'response': 'some of the parameters left empty','status':'401'})

        elif(author_type == 'instagram_search'):
            target_keyword = request.data.get('target_keywords')
            page_url = request.data.get('page_url')

            if(target_keyword and page_url):
                return JsonResponse({'response': 'success submitted','status':'200'})
            else:
                return JsonResponse({'response': 'some of the parameters left empty','status':'401'})
        else:
            return JsonResponse({'response': 'failed to submit, given author type is not supported','status':'401'})

class Add_Twitter_Target(APIView):
    #class to add targets of twitter to the system

    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        sss = coreDb.get_supported_social_sites_list()
        sss_list = list(sss)

        form_data = {'twitter_target_form': {'author_types': TWITTER_AUT, 'intervals': PERIODIC_INT,'tweets_type':TWEETS_TYPE,'search_type':SEARCH_TYPE_TWITTER}}
        # return JsonResponse(form_data,safe=False)
        return JsonResponse(form_data)

    def post(self, request):
        print(request.data)
        #sss_id = request.POST.get('sss_id', None)
        author_type = request.data.get('author_type', None)


        expired_on = request.data.get('expired_on', None)
        expired_on = convert_expired_on_to_datetime(expired_on)
        # is_enabled = request.data.get('is_enabled', None)
        # is_expired = request.data.get('is_expired', None)
        periodic_interval = request.data.get('periodic_interval')

        if (author_type == 'twitter_person'):
            author_id = request.data.get('author_id', None)
            author_account = request.data.get('author_account', None)
            author_name = request.data.get('author_name', None)
            author_url = request.data.get('author_url', None)
            tweets_type = request.data.get('tweets_type',None)

            need_screenshots = request.data.get('need_screenshots', None)
            print(author_type, author_id,author_name, author_account, author_url, expired_on, need_screenshots, periodic_interval)
            author_id = int(author_id)

            periodic_interval = int(periodic_interval)
            if (author_id and author_account and author_name and author_url and tweets_type):

                try:
                    print('................................about to add target .............................')
                    coreDb.insert_twitter_person_target(author_type,author_id,author_account,author_name,author_url,tweets_type,need_screenshots,expired_on,periodic_interval)

                except Exception as e:
                    print(e)

                return JsonResponse({'response': 'success submitted', 'status': '200'})
            else:
                return JsonResponse({'response': 'some of the parameters left empty', 'status': '401'})
        elif (author_type == 'twitter_search'):
            #target_keyword = request.data.get('target_keywords')
            #page_url = request.data.get('page_url')

            phrase  = request.data.get('phrase',None)
            hashtags = request.data.get('hashtags',None)
            location  = request.data.get('location',None)
            radius = request.data.get('radius',None)
            date = request.data.get('date',None)
            positive_attitude  = request.data.get('positive_attitude',None)
            negative_attitude = request.data.get('negative_attitude',None)
            search_type = request.data.get('search_type',None)



            if(search_type is not None):

                if (phrase is not None and hashtags is not None and location is not None and radius is not None and date is not None and positive_attitude is not None and negative_attitude is not None ):

                    expired_on = int(expired_on)
                    periodic_interval = int(periodic_interval)
                    print(expired_on)

                    coreDb.insert_twitter_search_target(author_type,search_type,phrase,hashtags,location,radius,date,positive_attitude,negative_attitude,expired_on,periodic_interval)
                    return JsonResponse({'response': 'success submitted', 'status': '200'})
                else:
                    return JsonResponse({'response': 'some of the parameters left empty', 'status': '401'})


        else:
            return JsonResponse({'response': 'failed to submit, given author type is not supported'})


class Add_Facebook_Target(APIView):

    #class to add targets of Facebook to the system
    #it is sole class to add facebook targets for person,page,group,search,tags,
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        sss = coreDb.get_supported_social_sites_list()
        sss_list = list(sss)

        form_data = {'facebook_target_form': {'author_types': FACEBOOK_AUT, 'intervals': PERIODIC_INT}}
        # return JsonResponse(form_data,safe=False)
        return Response(form_data)

    def post(self, request):

        author_type = request.data.get('author_type', None)
        expired_on = request.data.get('expired_on', None)
        expired_on = convert_expired_on_to_datetime(expired_on)
        print(expired_on,type(expired_on))
        periodic_interval = request.data.get('periodic_interval')



        if (author_type == 'facebook_person'):
            author_id = request.data.get('id', None)
            author_account = request.data.get('account', None)
            author_name = request.data.get('name', None)
            author_url = request.data.get('url', None)
            need_screenshots = request.data.get('need_screenshots', None)

            print(author_type, author_name, author_account, author_url, expired_on, need_screenshots, periodic_interval)
            #type conversions bellow

            author_id = int(author_id)
            need_screenshots = bool(need_screenshots)
            periodic_interval = int(periodic_interval)




            if (author_id and author_account and author_name and author_url ):
                try:
                    coreDb.insert_facebook_person_target(author_type,author_id,author_account,author_name,author_url,need_screenshots,expired_on,periodic_interval)
                    return JsonResponse({'response': 'success submitted', 'status': '200'})
                except Exception as e :
                    print(e)
                    return JsonResponse({'response': 'some of the parameters left empty', 'status': '401'})
            else:
                return Response({'response': 'some of the parameters left empty'+author_type})

        elif (author_type == 'facebook_page'):
            author_id = request.data.get('id', None)
            author_account = request.data.get('account', None)
            author_name = request.data.get('name', None)
            author_url = request.data.get('url', None)
            need_screenshots = request.data.get('need_screenshots', None)

            if (author_id and author_account and author_name and author_url and need_screenshots):
                return Response({'response': 'success submitted'+author_type})
            else:
                return Response({'response': 'some of the parameters left empty'})
        elif (author_type == 'facebook_group'):
            author_id = request.data.get('id', None)
            author_account = request.data.get('account', None)
            author_name = request.data.get('name', None)
            author_url = request.data.get('url', None)
            need_screenshots = request.data.get('need_screenshots', None)

            if (author_id and author_account and author_name and author_url and need_screenshots):
                return Response({'response': 'success submitted'+author_type})
            else:
                return Response({'response': 'some of the parameters left empty'})
        elif (author_type == 'facebook_hashtag'):
            target_keyword = request.data.get('target_keywords')
            page_url = request.data.get('page_url')

            if (target_keyword and page_url):
                return Response({'response': 'success submitted'+author_type})
            else:
                return Response({'response': 'some of the parameters left empty'})

        elif (author_type == 'facebook_search'):
            target_keyword = request.data.get('target_keywords')
            page_url = request.data.get('page_url')

            if (target_keyword and page_url):
                return Response({'response': 'success submitted'+author_type})
            else:
                return Response({'response': 'some of the parameters left empty'})

        else:
            return Response({'response': 'failed to submit, given author type is not supported'})


class Add_Linkedin_Target(APIView):

    #class to add targets of instagram to the system

    #permission_classes = (IsAuthenticated,)

    def get(self,request):

        sss = coreDb.get_supported_social_sites_list()
        sss_list = list(sss)

        form_data = {'linkedin_target_form': {'author_types': LINKEDIN_AUT , 'intervals': PERIODIC_INT}}
        # return JsonResponse(form_data,safe=False)
        return JsonResponse(form_data)


    def post(self,request):

        #print(request.body)
        #first convert request body to json and then read its pararmeters
        #post_parameters = request.body.decode('utf8').replace("'", '"')
        #print(post_parameters.__len__())

        #sss_id = request.POST.get('sss_id', None)

        author_type = request.data.get('author_type', None)

        need_screenshots = request.data.get('need_screenshots',None)
        expired_on = request.data.get('expired_on', None)
        expired_on = convert_expired_on_to_datetime(expired_on)
        periodic_interval = request.data.get('periodic_interval',None)

        if(author_type == 'linkedin_person'):
            author_id = request.data.get('author_id',None)
            author_account = request.data.get('author_account', None)
            author_name = request.data.get('author_name', None)
            author_url = request.data.get('author_url', None)


            periodic_interval = int(periodic_interval)

            if(author_id and author_account and author_name and author_url):
                print(author_id,author_account,author_name,author_url)
                coreDb.insert_linkedin_person_target(author_type,author_id,author_account,author_name,author_url,need_screenshots,expired_on,periodic_interval)
                return JsonResponse({'response': 'success submitted','status':'200'})
            else:
                return JsonResponse({'response': 'some of the parameters left empty','status':'401'})

        elif(author_type == 'linkedin_company'):
            author_id = request.data.get('author_id', None)
            author_account = request.data.get('author_account', None)
            author_name = request.data.get('author_name', None)
            author_url = request.data.get('author_url', None)



            if(author_id and author_account and author_name and author_url):
                coreDb.insert_linkedin_company_target(author_type,author_id,author_account,author_name,author_url,need_screenshots,expired_on,periodic_interval)
                return JsonResponse({'response': 'success submitted','status':'200'})
            else:
                return JsonResponse({'response': 'some of the parameters left empty','status':'401'})
        else:
            return JsonResponse({'response': 'failed to submit, given author type is not supported','status':'401'})

#...................................................Views for Tagets Retrivals Already Set ...................................................

"""

"""

class Get_Facebook_Targets(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):

        resp = coreDb.get_facebook_targets()
        print(resp)
        return JsonResponse(resp,safe=False)

class Get_Twitter_Targets(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):

        resp = coreDb.get_twitter_targets()
        return JsonResponse(resp,safe=False)

class Get_Instagram_Targets(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):

        resp = coreDb.get_instagram_targets()
        return JsonResponse(resp,safe=False)

class Get_Linkedin_Person_Targets(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):

        resp = coreDb.get_linkedin_person_targets()
        return JsonResponse(resp,safe=False)

class Dashboard(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request):

        return render(request,'OSINT_System_Core/dashboard.html',{})

class Supported_Social_Site_List(APIView):

    #list of all the supported sites in OSINT CORE


    def get(self,request,format = None):
        sss = Supported_Socail_Sites.objects.all()

        serializer = Supported_Socail_Sites_Serializer(sss,many=True)
        print(serializer.data)
        return JsonResponse(serializer.data,safe=False)
"""


# ...................................................Views for General Que

class Crawler_Internet_Connection(View):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        resp = acq.crawler_internet_connection()
        return JsonResponse(resp, safe=False)


class Microcrawler_Status(View):
    # permission_classes = (IsAuthenticated,)
    # resp = acq.mircocrawler_status()
    def get(self, request, *args, **kwargs):
        resp = acq.mircocrawler_status()
        return JsonResponse(resp, safe=False)


# ...................................................Views for SmartSearch

class Smart_Search(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        resp = tasks.fetch_smart_search(
            username=kwargs['author_account'],
            search_site=kwargs['search_site'])
        return JsonResponse(resp, safe=False)


# ...................................................Views for Graphs ....


class Overview_Pie_Chart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.article_stat_for_slo()
        return JsonResponse(res, safe=False)


class Extracted_All_Sites(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.extracted_selected_all_sites()
        return JsonResponse(res, safe=False)


class Extracted_All_Social_Sites(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.extracted_selected_all_social_sites()
        return JsonResponse(res, safe=False)


class Sent_To_Pco(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.send_to_pco()
        return JsonResponse(res, safe=False)


class Overview_Rpo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.send_to_rpo()
        return JsonResponse(res, safe=False)


class Article_Stat_Overview(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.article_stat_overview()
        return JsonResponse(res, safe=False)


class Article_Stat_Slo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.article_stat_for_slo()
        return JsonResponse(res, safe=False)


class My_Article_Stat(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.my_article_stat()
        return JsonResponse(res, safe=False)


class Ticket_State(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.article_stat_overview()
        return JsonResponse(res, safe=False)


class Fetch_State(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.fetch_stat()
        return JsonResponse(res, safe=False)


class Extracted_Article(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.extracted_article()
        return JsonResponse(res, safe=False)


class Processed_Article(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.processed_article()
        return JsonResponse(res, safe=False)


class Article_Trend(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = log_manager.article_trend()
        return JsonResponse(res, safe=False)


class Dispatcher(View):

    def get(self, request, *args, **kwargs):
        print(
            '...........................In Disipatcher...................................')
        GTR = kwargs['GTR']
        author_account = kwargs['author_account']

        send_event('notifications', 'notification', {
            'GTR': GTR, 'author_account': author_account})
        return HttpResponse('success')


# ...........................................View For Object Search(awais)

class Find_Object(View):

    def get(self, request, *args, **kwargs):

        print(request.GET)
        type = request.GET['type']
        query = request.GET['query']

        if (type == 'portfolio'):
            resp = Portfolio_PMS.find_object(query)
            return render(request, 'OSINT_System_Core/find_object.html', {'objects': resp})
        elif (type == 'keybase'):
            resp = Keybase_KMS.find_object(query)
            return render(request, 'OSINT_System_Core/find_object.html', {'objects': resp})
        elif (type == 'avatar'):
            resp = Avatar_AMS.find_object(query)
            return render(request, 'OSINT_System_Core/find_object.html', {'objects': resp})
        else:
            print('invalid choice')

        return HttpResponse('')


class Link_Object(View):
    def get(self, request):
        print(request.GET)
        alpha_id = ObjectId(request.GET['alpha_id'])
        beta_path_list = [ObjectId(request.GET['beta_id'])]

        type = request.GET['type']
        if (type == 'portfolio'):
            resp = pl.create(alpha_id, beta_path_list)
            if (resp is not None):
                return HttpResponse('resource linked sucessfully ')
        elif (type == 'keybase'):
            # resp = Keybase_KMS.find_object(query)
            return HttpResponse('resource linked sucessfully ')
        elif (type == 'avatar'):
            # resp = Avatar_AMS.find_object(query)
            return HttpResponse('resource linked sucessfully ')
        else:

            return HttpResponse('given type is either empty or invalid')
        return HttpResponse('this resource is already linked with this ' + type)


class Share_Resource(View):
    ml = Mongo_Lookup()

    def get(self, request):
        print(request.GET)
        group_typ = request.GET.get('user_group', None)
        message = request.GET.get('message', None)
        resource_id = request.GET.get('resource_id', None)

        if (group_typ and message and resource_id):
            resource_obj = self.ml.find_object_by_id(ObjectId(resource_id))
            if (resource_obj is not None):
                try:
                    obj = Share_Resource_M(user_id=request.user.id,
                                           username=request.user.username,
                                           share_with=[group_typ],
                                           message=message,
                                           resource_ref=resource_obj,

                                           )

                    obj.save()
                    return HttpResponse('resource shared successfully')
                except Exception as e:
                    print(e)
                    return HttpResponse(e)
            else:
                return HttpResponse('unable to locate object of given resource')
        else:
            return HttpResponse('input parameters are left empty or invalid')
        return HttpResponse('unable to share resource')


class Rabbit_Message(View):

    def get(self, request):
        #print(request.GET)
        objects = Rabbit_Messages.get_top_messages(10, request.GET.get('window_type', 'message'))
        print(objects)

        return render(request, 'OSINT_System_Core/message_loger.html', {'messages': objects})


class Update_Footer_Graphs():

    def get(self, request):
        internet = acq.crawler_internet_connection()
        mc_status = acq.mircocrawler_status()

        return None


# .........................................Normal Functions ............


def convert_expired_on_to_datetime(expired_on):
    expired_onn = expired_on + ' 13:55:26'
    expired_onnn = datetime.datetime.strptime(expired_onn, '%m/%d/%Y %H:%M:%S')
    return expired_onnn


def test_view(request):
    if request.method == 'GET':
        return render(request, 'OSINT_System_Core/project_base.html')


def test_view1(request):
    if request.method == 'GET':
        return render(request, 'OSINT_System_Core/tso_dashboard.html')


class TSO_Dashboard(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'OSINT_System_Core/tso_dashboard.html')


class TMO_Dashboard(RequireLoginMixin, IsTMO, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'OSINT_System_Core/tmo_dashboard.html')


class RDO_Dashboard(RequireLoginMixin, IsRDO, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'OSINT_System_Core/rdo_dashboard.html')


class PAO_Dashboard(RequireLoginMixin, IsPAO, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'OSINT_System_Core/pao_dashboard.html')


# ahmed start
class Dashboard(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        # calling core manager function

        # first time load data
        reddit_trends = Trends.objects.filter(trend_type='reddit_trends').order_by('-id').first()
        print("perinting reeddit trends ")
        print(len(reddit_trends))
        for i in reddit_trends:
            print(i)
        # {
        #     "trend_type": "reddit_trends",
        #     "trend_graph": [],
        #     "popular_hashtag": "",
        #     "top_trends": [
        #         {
        #             "author_fullname": "t2_2bfojune",
        #             "selftext": "We post dark, demented memes and we're looking for people to join our community. \n\nr/Dark_Demented_Memes",
        #             "title": "Join our new subreddit r/Dark_Demented_Memes !",
        #             "count": 5
        #         },
        #         {
        #             "author_fullname": "Jt2_4qqy8cha",
        #             "selftext": "We remodeled the subreddit",
        #             "title": "r/adults",
        #             "count": 3
        #         }
        #     ],
        #     "country": "",
        #     "common_words": [],
        #     "spelling_variants": []
        # }
        # youtube first time load data
        youtube_trends = Trends.objects.filter(trend_type='youtube_trends').order_by('-id').first()

        twitter_top_hastags = {}
        Target_Count_Chart = Global_Target_Reference.target_count_for_all_sites()
        print(type(Target_Count_Chart))
        # get top hashtags for first load
        try:
            twitter_country_hashtags = Trends.objects.filter(country='pakistan', trend_type='twitter_trends').order_by(
                '-id').first()
        # hashtag chart update
        except Trends.DoesNotExist:
            twitter_country_hashtags = None
        # first time load data end
        countries_list = [
            'world',
            'australia', 'russia', 'israel',
            'austria', 'saudi arabia', 'italy',
            'bahrain', 'singapore', 'japan',
            'Belarus', 'South', 'africa', 'Jordan',
            'Belgium', 'Spain', 'kenya',
            'Brazil', 'Sweden', 'korea',
            'Canada', 'Switzerland', 'kuwait',
            'Chile', 'Thailand', 'Latvia',
            'Colombia', 'Turkey', 'Lebanon',
            'Denmark', 'Ukraine', 'Malaysia',
            'Dominican', 'Republic', 'United Arab Emirates', 'Mexico',
            'Ecuador', 'United', 'Kingdom', 'Netherlands',
            'Egypt', 'United States', 'New Zealand',
            'France', 'Venezuela', 'Nigeria',
            'Germany', 'Vietnam', 'Norway',
            'Ghana', 'Philippines', 'Oman',
            'Greece', 'Poland', 'pakistan',
            'Guatemala', 'Portugal', 'Panama',
            'india',
            'Peru'
        ]

        return render(request, 'OSINT_System_Core/additional_templates/dashboard.html',
                      {'reddit_trends': reddit_trends, 'twitter_top_hastags': twitter_top_hastags,
                       'youtube_trends': youtube_trends, 'twitter_country_hashtags': twitter_country_hashtags,
                       'countries_list': countries_list, 'Target_Count_Chart': Target_Count_Chart})


def main(request):
    obj = Update_Bigview()
    obj.update_reddit_trends()
    obj.update_hashtag_trends()
    obj.update_youtube_toptrends()
    obj.update_hashtag_charts()
    obj.update_youtube_charts()
    return render(request, 'OSINT_System_Core/additional_templates/main.html', {})


def main_1(request):
    return render(request, 'OSINT_System_Core/additional_templates/main_1.html', {})


def mainHeatMap(request):
    return render(request, 'OSINT_System_Core/additional_templates/main_heatmap.html', {})


def newsMonitor(request):
    # with open('static/Target_Json/news_data1.json', 'r') as f:
    #     news_json = json.load(f)
    news_json = News.objects().limit(1)
    print(news_json)
    return render(request, 'OSINT_System_Core/additional_templates/news_monitoring.html', {'news_json': news_json})


def topNews(request):
    ary = News.objects(Q(channel='ARY')).order_by('-id').first()
    dawn = News.objects(Q(channel='DAWN')).order_by('-id').first()
    ndtv = News.objects(Q(channel='NDTV')).order_by('-id').first()
    india_today = News.objects(Q(channel='INDIATODAY')).order_by('-id').first()
    abp = News.objects(Q(channel='ABP')).order_by('-id').first()
    zee = News.objects(Q(channel='ZEE')).order_by('-id').first()
    list1 = [ary, dawn, ndtv, india_today, abp, zee]
    print(ndtv.channel)
    print(ndtv.most_emerging_news)
    return render(request, "OSINT_System_Core/additional_templates/top_news.html", {'top_news': list1})


# get worldwide hashtags function
def get_worldwide_hashtags():
    # text_data_json = json.loads(text_data)
    # message = text_data_json['message']
    url = 'https://trends24.in/';
    page = requests.get(url);
    status_code = page.status_code;
    dic = {};
    hashtag_name = [];
    hashtag_href = [];
    hashtag_count = [];
    if (status_code == 200):
        data = BeautifulSoup(page.text, 'lxml')
        new = data.find('ol', class_="trend-card__list");
        li = data.find_all('li')
        for i in li:
            hashtag_name.append(i.a.text)
            hashtag_href.append(i.a.attrs['href'])
            if (i.find('span')):
                hashtag_count.append(i.span.text)
            else:
                hashtag_count.append("N/A")
    dic = []
    for i in range(len(hashtag_name)):
        dic.append(
            {"name": hashtag_name[i],
             "count": hashtag_count[i],
             "href": hashtag_href[i]
             })

    return (dic)


def getTrendsByCountry(request):
    if request.method == 'GET':
        country_name = request.GET['country_name']
        print(country_name)
        # data=Trends.objects.get(country='pakistan',trend_type='twitter_trends')
        try:
            data = Trends.objects.filter(country=country_name, trend_type='twitter_trends').order_by('-id').first()
            json_data = data.to_json()
            return HttpResponse(json_data)
        except Trends.DoesNotExist:
            data = None
            return HttpResponse(data)


def getYoutubeTrends(request):
    if request.method == 'GET':
        try:
            data = Trends.objects.filter(trend_type='youtube_trends').order_by('-id').first()
            json_data = data.to_json()
            return HttpResponse(json_data)
        except Trends.DoesNotExist:
            data = None
            return HttpResponse(data)


def update_micro_crawler_stats(request):
    if request.method == 'GET':
        micro_cralwer_stats = acq.mircocrawler_status()
        json_data = json.dumps(micro_cralwer_stats)
        return HttpResponse(json_data)


def update_internet_stats(request):
    if request.method == 'GET':
        internet_stats = acq.crawler_internet_connection()
        print("called update internet stats fucntion ")
        print(internet_stats)
        json_data = json.dumps(internet_stats)
        print(json_data)
        return HttpResponse(json_data)


def update_dashboard_donutchart(request):
    if request.method == 'GET':
        Target_Count_Chart = Global_Target_Reference.target_count_for_all_sites()
        json_data = json.dumps(Target_Count_Chart)
        print(json_data)
        return HttpResponse(json_data)