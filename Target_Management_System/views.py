from django.shortcuts import render, redirect,reverse
import json
# Create your views here.
from django.http import JsonResponse
from django.views import View
from OSINT_System_Core.publisher import publish
from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from Public_Data_Acquisition_Unit.mongo_models import PERIODIC_INTERVALS
from bson import ObjectId
from django.http import HttpResponse, HttpResponseRedirect
from django_eventstream import send_event

acq = Acquistion_Manager()


class Add_Target(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        # send all the supported sites objects with their target types

        social_sites = acq.get_all_social_sites()
        news_sites = acq.get_all_news_sites()
        blog_sites = acq.get_all_blog_sites()

        if 'portfolio_id' in kwargs :request.session['selected_portfolio_id'] = kwargs['portfolio_id']
        #print(kwargs['portfolio_id'])
        # print(social_sites.to_json())
        # data = serializers.serialize('json', social_sites.to_json(), fields=(
        #     'name', 'url', 'website_type', 'target_type'))
        data = {
            'social': json.loads(social_sites.to_json()),
            'news': json.loads(news_sites.to_json()),
            'blogs': json.loads(blog_sites.to_json()),
            'intervals':PERIODIC_INTERVALS,
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
        #<QueryDict: {'csrfmiddlewaretoken': ['Egw4i8ivl698nS7BzlKQkGGUue93nN6jEWHKEOwnRI5bsrp329nu2sCwAiDlGUi0'], 'facebook_autheruseraccount': ['awais'], 'facebook_authortype': ['0'], 'facebook_authoruserid': ['abcdef123'], 'facebook_authorusername': ['sharif ahmad'], 'facebook_authoruserurl': ['http://www.facebook.com/sharifahmad2061'], 'date': [''], 'facebook_interval': ['15'], 'facebook_screenshot': ['1']}



        print(request.POST)
        website_id = ObjectId(request.POST['website_id'])
        target_type_index = int(request.POST['facebook_authortype'])
        username = request.POST['facebook_autheruseraccount']
        user_id = request.POST['facebook_authoruserid']
        name = request.POST['facebook_authorusername']
        url = request.POST['facebook_authoruserurl']
        expire_on = request.POST['facebook_expirydate']
        interval = int(request.POST['facebook_interval'])
        screen_shot = False

        portfolio_id = None
        if 'selected_portfolio_id' in request.session :portfolio_id = request.session.get('selected_portfolio_id')
        print(portfolio_id)
        if ('facebook_screenshot' in request.POST):
            screen_shot = request.POST['facebook_screenshot']
            if(screen_shot == '1'):
                screen_shot = True

        print(website_id,target_type_index,username,user_id)
        acq.add_target(website_id, target_type_index,portfolio_id=portfolio_id,username=username, user_id=user_id,name=name,url=url,expired_on=expire_on,periodic_interval=interval,need_screenshots=screen_shot)
        #publish('target created successfully', message_type='notification')
        return redirect('/tms/marktarget')


# ...................................................Views for SmartSearch

class Smart_Search(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        username = request.GET['author_account']
        search_site = request.GET['search_site']

        print(username,search_site)
        resp = acq.fetch_smart_search(username=username,search_site=search_site)
        # print(kwargs)
        resp = {
            'author_userid': 'abcdef123',
            'author_username': 'sharif ahmad',
            'author_url': 'sharifahmad2061'
        }
        return JsonResponse(resp, safe=False)


class Target_Fetched(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):

        resp = acq.get_fetched_targets()
        print(resp)
        return render(request,'Target_Management_System/tso_targetfetchview.html',{'targets':resp})

    def post(self, request, *args, **kwargs):
        pass


class Identify_Target(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_identifytarget.html',{})

    def post(self, request, *args, **kwargs):
        pass

class Identify_Target_Request(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):


        print(request.GET)
        query = request.GET['query']
        website = request.GET['website']

        print(query,website)
        resp = acq.identify_target(query,website)
        #check here if resp is not none and remove the dummy reponse
        resp = {
            'author_userid': 'abcdef123',
            'author_username': 'sharif ahmad',
            'author_url': 'sharifahmad2061'
        }
        return JsonResponse(resp, safe=False)

class Target_Internet_Survey(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_internetsurvey.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):

        print(request.POST)
        name = request.POST.get('name_lookup', '')
        email = request.POST.get('email_lookup', '')
        phone = request.POST.get('phone_lookup', '')
        address = request.POST.get('address_lookup','')
        print(name, email, phone, address)
        # pass values to the user and wait for the response and show to the
        # same view
        resp = acq.target_internet_survey(name, email, phone, address)

        print(resp)

        #pass the response to front end and show it to user
        # return JsonResponse(resp, safe=False)
        return render(request,'Target_Management_System/tso_internetsurvey.html',{})


class Dyanamic_Crawling(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'Target_Management_System/tso_dynamiccrawling.html',
                      {'app': 'target'})

    def post(self, request, *args, **kwargs):


        website_id = acq.get_custom_webiste_id()
        target_type_index = 1
        page_url = request.POST.get('page_url',False)

        links =bool(request.POST.get('links',False))
        headings =bool(request.POST.get('headings',False))
        paragraphs =bool(request.POST.get('paragraphs',False))
        pictures =bool(request.POST.get('pictures',False))
        videos =bool(request.POST.get('videos',False))
        ip =bool(request.POST.get('page_url',False))


        print(request.POST)
        #print(links,headings,paragraphs,pictures,videos,ip)
        # pass the above values to the ess api handler and submit

        acq.add_target(
            website_id=website_id,
            target_type_index=target_type_index,
            title='Crawling Target',
            url=page_url,
            links=links,
            headings=headings,
            paragraphs=paragraphs,
            pictures=pictures,
            videos=videos,
            ip=ip
        )
        return HttpResponseRedirect(reverse('Target_Management_System:tms_dynamiccrawling'))


class Created_Targets(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):


        resp,_ = acq.targets_added_all_time()

        return render(request,'Target_Management_System/tso_targetscreated.html',{'targets':resp})


class Facebook_Target_Response(RequireLoginMixin,IsTSO,View):

    def get(self,request,*args,**kwargs):

        gtr_id = ObjectId('5e6f1b447da8f74c619f703a')
        data_object = acq.get_data_response_object_by_gtr_id(gtr_id)

        print(data_object)
        data_object = data_object.to_mongo()


        return render(request,'Target_Management_System/facebook_target_response.html',{'person':data_object})



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
