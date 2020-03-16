from django.shortcuts import render
import json
# Create your views here.
from django.http import JsonResponse
from django.views import View
from OSINT_System_Core.publisher import publish
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager

from django.http import HttpResponse, HttpResponseRedirect


acq = Acquistion_Manager()


class Add_Target(View):

    def get(self, request, *args, **kwargs):
        # send all the supported sites objects with their target types

        social_sites = acq.get_all_social_sites()
        news_sites = acq.get_all_news_sites()
        blog_sites = acq.get_all_blog_sites()
        # print(social_sites.to_json())
        # data = serializers.serialize('json', social_sites.to_json(), fields=(
        #     'name', 'url', 'website_type', 'target_type'))
        data = {
            'social': json.loads(social_sites.to_json()),
            'news': json.loads(news_sites.to_json()),
            'blogs': json.loads(blog_sites.to_json())
        }
        print(data)
        return render(request,
                      'Target_Management_System/tso_marktarget.html',
                      {'app': 'target',
                       'data': data})
        # return JsonResponse(data,
        #                     content_type='application/json',
        #                     charset='utf8')

    def post(self, request, *args, **kwargs):

        # get the all the values for kwargs and pass the the add target function they can change
        # depending upon the target type

        website_id = kwargs['website_id']
        target_type_index = kwargs['target_type_index']

        acq.add_target(website_id, target_type_index,
                       username='username', user_id='user_id')
        publish('target created successfully', message_type='notification')


# ...................................................Views for SmartSearch

class Smart_Search(View):

    def get(self, request, *args, **kwargs):
        username = request.GET['author_account'][0]
        search_site = request.GET['search_site'][0]
        # print(kwargs)
        resp = acq.fetch_smart_search(
            username=username,
            search_site=search_site)
        return JsonResponse(resp, safe=False)


class Target_Fetched(View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_targetfetchview.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        pass


class Identify_Target(View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_identifytarget.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        pass


class Target_Internet_Survey(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_internetsurvey.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):

        name = kwargs['name']
        email = kwargs['email']
        phone = kwargs['phone']
        address = kwargs['address']

        # pass values to the user and wait for the response and show to the
        # same view
        resp = acq.target_internet_survey(name, email, phone, address)
        # can return httpresponse to same page and get a new query and do the
        # process again

        return JsonResponse(resp, safe=False)


class Dyanamic_Crawling(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_dynamiccrawling.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        url = None
        ip_address = None
        attribute_list = None

        # pass the above values to the ess api handler and submit
