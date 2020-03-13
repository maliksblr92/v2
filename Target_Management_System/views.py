from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from OSINT_System_Core.publisher import publish
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager

from django.http import HttpResponse,HttpResponseRedirect


acq = Acquistion_Manager()


class Add_Target(View):

    def get(self,request,*args,**kwargs):
        #send all the supported sites objects with their target types

        social_sites = acq.get_all_social_sites()
        news_sites = acq.get_all_news_sites()
        blog_sites = acq.get_all_blog_sites()
        pass

    def post(self,request,*args,**kwargs):

        #get the all the values for kwargs and pass the the add target function they can change
        #depending upon the target type

        website_id = kwargs['website_id']
        target_type_index = kwargs['target_type_index']

        #different target types has different kwargs pass the depending on the target_type with basic arguemtns


        acq.add_target(website_id,target_type_index,username='username',user_id='user_id')
        publish('target created successfully',message_type='notification')


#...................................................Views for SmartSearches ...................................................

class Smart_Search(View):

    def get(self, request,*args,**kwargs):

        resp = acq.fetch_smart_search(username=kwargs['author_account'],search_site=kwargs['search_site'])
        return JsonResponse(resp,safe=False)


class Target_Internet_Survey(View):

    def get(self, request,*args,**kwargs):

        name = kwargs['name']
        email = kwargs['email']
        phone = kwargs['phone']
        address = kwargs['address']

        #pass values to the user and wait for the response and show to the same view
        resp = acq.target_internet_survey(name,email,phone,address)
        #can return httpresponse to same page and get a new query and do the process again

        return JsonResponse(resp,safe=False)

class Dyanamic_Crawling(View):

    def post(self, request,*args,**kwargs):
        url = None
        ip_address = None
        attribute_list = None

        #pass the above values to the ess api handler and submit


class Target_Fetched(View):
    def get(self,request):
        obj = acq.get_fetched_targets(30)
        print(obj)

