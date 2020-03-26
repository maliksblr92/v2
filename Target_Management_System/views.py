from django.shortcuts import render, redirect
import json
# Create your views here.
from django.http import JsonResponse
from django.views import View
from OSINT_System_Core.publisher import publish
from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager


from django.http import HttpResponse, HttpResponseRedirect
from django_eventstream import send_event

acq = Acquistion_Manager()


class Add_Target(RequireLoginMixin, IsTSO, View):

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
        print(request.POST)
        # website_id = kwargs['website_id']
        # target_type_index = kwargs['target_type_index']

        # acq.add_target(website_id, target_type_index,
        #                username='username', user_id='user_id')
        # publish('target created successfully', message_type='notification')
        return redirect('/tms/marktarget')


# ...................................................Views for SmartSearch

class Smart_Search(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        username = request.GET['author_account'][0]
        search_site = request.GET['search_site'][0]
        # print(kwargs)
        resp = {
            'author_userid': 'abcdef123',
            'author_username': 'sharif ahmad',
            'author_url': 'sharifahmad2061'
        }
        # resp = acq.fetch_smart_search(
        #     username=username,
        #     search_site=search_site)
        return JsonResponse(resp, safe=False)


class Target_Fetched(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_targetfetchview.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        pass


class Identify_Target(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_identifytarget.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        pass


class Target_Internet_Survey(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_internetsurvey.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):

        print(request.POST)
        name = request.POST.get('name_lookup', None)
        email = request.POST.get('email_lookup', None)
        phone = request.POST.get('phone_lookup', None)
        address = request.POST.get('address_lookup', None)
        print(name, email, phone, address)
        # pass values to the user and wait for the response and show to the
        # same view
        # resp = acq.target_internet_survey(name, email, phone, address)
        # can return httpresponse to same page and get a new query and do the
        # process again
        # print(resp)

        # return JsonResponse(resp, safe=False)
        return render(request,
                      'Target_Management_System/tso_internetsurvey.html',
                      {'app': 'target'})


class Dyanamic_Crawling(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_dynamiccrawling.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):
        url = None
        ip_address = None
        attribute_list = None

        # pass the above values to the ess api handler and submit


class Test_View(View):
    def get(self, request, *args, **kwargs):
        print('send event about to be called')
        send_event('notifications', 'notification', {
                   'a': 1, 'text': 'this is 2nd notification'})
        return JsonResponse({'event_called': 1})


class Test_View1(View):
    def get(self, request, *args, **kwargs):
        print('send event about to be called')
        send_event('notifications', 'alert', {
            'new': 'alert1', 'prev1': 'alert2', 'prev2': 'alert3'})
        return JsonResponse({'alert_event_called': 1})
