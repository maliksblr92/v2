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
from Keybase_Management_System.keybase_manager import Keybase_Manager
acq = Acquistion_Manager()
km = Keybase_Manager()
from django.views.generic import TemplateView

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
        plateform = request.POST['platform']

        website_id = ObjectId(request.POST['website_id'])
        target_type_index = int(request.POST[plateform+'_authortype'])
        username = request.POST[plateform+'_autheruseraccount']
        user_id = request.POST[plateform+'_authoruserid']
        name = request.POST[plateform+'_authorusername']
        url = request.POST[plateform+'_authoruserurl']
        expire_on = request.POST[plateform+'_expirydate']
        interval = int(request.POST[plateform+'_interval'])
        screen_shot = False

        portfolio_id = None
        if 'selected_portfolio_id' in request.session :portfolio_id = request.session.get('selected_portfolio_id')
        print(portfolio_id)

        if (expire_on is not None):
            expire_on = convert_expired_on_to_datetime(expire_on)



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
        if (not 'response' in resp):
            print(resp)
            resp = {
                'author_userid': resp['data']['id'],
                'author_username': resp['data']['full_name'],
                'author_url': 'sharifahmad2061',
                'profile_url':resp['data']['profile_image_url']
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

class Identify_Target_Request(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):


        print(request.GET)
        query = request.GET['query']
        website = request.GET['website']

        print(query,website)
        resp = acq.identify_target(query,website)
        #print(resp)

        users = []
        if(not 'response' in resp):

            if(website == 'instagram'):
                data = resp['data']['users']
                for item in data:
                    #print(item)
                    user = {'username': item['user']['username'],'fullname': item['user']['full_name'],'userid': '','profile_url':item['user']['profile_pic_url']}
                    users.append(user)

        print(users)
        return render(request,'Target_Management_System/identify_target_subtemplate.html',{'users':users})

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


class Keybase_Crawling(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):

        keybases = km.get_all_keybases()
        return render(request,
                      'Target_Management_System/keybase_crawling.html',
                      {'keybases':keybases,'intervals':PERIODIC_INTERVALS,})


    def post(self,request):

        print(request.POST)
        title = request.POST.get('title',None)
        website_id = acq.get_custom_webiste_id()
        target_type = 0

        keybase_id = request.POST.get('keybase',None)
        interval = int(request.POST.get('interval',None))
        expire_date = request.POST.get('expire_on',None)

        keybase_ref = km.get_keybase_object_by_id(keybase_id)

        if(expire_date is not None):
            expire_on = convert_expired_on_to_datetime(expire_date)


        acq.add_target(website_id,target_type,None,title=title,keybase_ref=keybase_ref,expired_on=expire_on,periodic_interval=interval)

        return HttpResponseRedirect(reverse('Target_Management_System:tms_keybase_crawling'))


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


def convert_expired_on_to_datetime(expired_on):
    import datetime
    expired_onn = expired_on + ' 13:55:26'
    expired_onnn = datetime.datetime.strptime(expired_onn, '%Y-%m-%d %H:%M:%S')
    return expired_onnn



# ahmed code
class Instagram_Target_Response(TemplateView):
    template_name = "Target_Management_System/InstagramPerson_Target_Response.html"





class LinkedinCompany_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
         with open('static/Target_Json/linkedin_companyr_data.json', 'r') as f:
            company = json.load(f)
         return render(request, 'Target_Management_System/LinkedinCompany_Target_Response.html', {'company': company})





class FacebookPerson_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        with open('static/Target_Json/facebook_person_data.json', 'r') as f:
            profile = json.load(f)
        return render(request, 'Target_Management_System/FacebookPerson_Target_Response.html',{'profile': profile})

class FacebookPage_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        with open('static/Target_Json/facebook_page_data.json', 'r') as f:
            page = json.load(f)
        return render(request, 'Target_Management_System/FacebookPage_Target_Response.html',{'page': page})


class FacebookGroup_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            group = json.load(f)
        return render(request, 'Target_Management_System/FacebookGroup_Target_Response.html',{'group': group})






# this json wasnot according to format to formatted here
class Twitter_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        #  json_data = open('static/Target_Json/tweets.json')
        #  data1 = json.load(json_data) # deserialises it
        #  data2 = json.dumps(data1) # json formatted string
        #  json_data.close()
        tweets = {
            "GTR": "91",
            "author_account": 'null',
            "name": "Fabia Nazar",
            "location": "\n              Sargodha\n\n        ",
            "profile_url": "https://pbs.twimg.com/profile_images/970360541624651776/-3H5TyTo_400x400.jpg",
            "biodata": "All praises be to ALLAH, the Cherisher and Sustainer of the World. xx",
            "frequent_hashtags": [],
            "website": "https://fabia056.blogspot.com",
            "joined_twitter": "Joined June 2014",
            "tweets_count": "13 Tweets",
            "follower_count": "11 Followers",
            "following_count": "12 Following",
            "likes_count": "8 Likes",
            "moments": 'null',
            "profile_summary": "Fabia Nazar is a twitter user. Fabia Nazar have mentioned personal biography as All praises be to ALLAH, the Cherisher and Sustainer of the World. xx. This twitter handler also belongs to another website named as https://fabia056.blogspot.com. Fabia Nazar have joined Twitter in  June 2014. Up till now, Fabia Nazar have tweeted 13 Tweets in total. Currently, Fabia Nazar have 12 Following, 11 Followers and 8 Likes. ",
            "target_update_count": 0,
            "behaviour": "None",
            "common_words": [],
            "sentiments": ["0 Positive", "0 Negative"],
            "emotions": ["sad", "cry"],
            "posting_time_charts": [],
            "tweets": [{
                "id": 1151827719161896960,
                "conversation_id": "1151824477484912640",
                "created_at": 1563452102000,
                "date": "2019-07-18",
                "time": "05:15:02",
                "timezone": "Pacific Daylight Time",
                "user_id": 871226174550286336,
                "username": "maliksblr92",
                "name": "AwaRa.....",
                "place": "",
                "tweet": "Tell the Democrat Governors that “Mutiny On The Bounty” was one of my all time favorite movies. A good old fashioned mutiny every now and then is an exciting and invigorating thing to watch, especially when the mutineers need so much from the Captain. Too easy!",
                "mentions": [
                    "syntaxerrorhehe"
                ],
                "urls": [],
                "photos": [],
                "replies_count": 1,
                "retweets_count": 0,
                "likes_count": 1,
                "hashtags": [],
                "cashtags": [],
                "link": "https://twitter.com/maliksblr92/status/1151827719161896960",
                "retweet": 'false',
                "quote_url": "",
                "video": 0,
                "near": "",
                "geo": "",
                "source": "",
                "user_rt_id": "",
                "user_rt": "",
                "retweet_id": "",
                "reply_to": [
                    {
                        "user_id": "871226174550286336",
                        "username": "maliksblr92"
                    },
                    {
                        "user_id": "756747471691386880",
                        "username": "syntaxerrorhehe"
                    }
                ],
                "retweet_date": "",
                "translate": "",
                "trans_src": "",
                "trans_dest": ""
            },
                {
                "id": 1151827719161896960,
                "conversation_id": "1151824477484912640",
                "created_at": 1563452102000,
                "date": "2019-07-18",
                "time": "05:15:02",
                "timezone": "Pacific Daylight Time",
                "user_id": 871226174550286336,
                "username": "maliksblr92",
                "name": "AwaRa.....",
                "place": "",
                "tweet": "Tell the Democrat Governors that “Mutiny On The Bounty” was one of my all time favorite movies. A good old fashioned mutiny every now and then is an exciting and invigorating thing to watch, especially when the mutineers need so much from the Captain. Too easy!",
                "mentions": [
                    "syntaxerrorhehe"
                ],
                "urls": [],
                "photos": [],
                "replies_count": 1,
                "retweets_count": 0,
                "likes_count": 1,
                "hashtags": [],
                "cashtags": [],
                "link": "https://twitter.com/maliksblr92/status/1151827719161896960",
                "retweet": 'false',
                "quote_url": "",
                "video": 0,
                "near": "",
                "geo": "",
                "source": "",
                "user_rt_id": "",
                "user_rt": "",
                "retweet_id": "",
                "reply_to": [
                    {
                        "user_id": "871226174550286336",
                        "username": "maliksblr92"
                    },
                    {
                        "user_id": "756747471691386880",
                        "username": "syntaxerrorhehe"
                    }
                ],
                "retweet_date": "",
                "translate": "",
                "trans_src": "",
                "trans_dest": ""
            }, {
                "id": 1151827719161896960,
                "conversation_id": "1151824477484912640",
                "created_at": 1563452102000,
                "date": "2019-07-18",
                "time": "05:15:02",
                "timezone": "Pacific Daylight Time",
                "user_id": 871226174550286336,
                "username": "maliksblr92",
                "name": "AwaRa.....",
                "place": "",
                "tweet": "Tell the Democrat Governors that “Mutiny On The Bounty” was one of my all time favorite movies. A good old fashioned mutiny every now and then is an exciting and invigorating thing to watch, especially when the mutineers need so much from the Captain. Too easy!",
                "mentions": [
                    "syntaxerrorhehe"
                ],
                "urls": [],
                "photos": [],
                "replies_count": 1,
                "retweets_count": 0,
                "likes_count": 1,
                "hashtags": [],
                "cashtags": [],
                "link": "https://twitter.com/maliksblr92/status/1151827719161896960",
                "retweet": 'false',
                "quote_url": "",
                "video": 0,
                "near": "",
                "geo": "",
                "source": "",
                "user_rt_id": "",
                "user_rt": "",
                "retweet_id": "",
                "reply_to": [
                    {
                        "user_id": "871226174550286336",
                        "username": "maliksblr92"
                    },
                    {
                        "user_id": "756747471691386880",
                        "username": "syntaxerrorhehe"
                    }
                ],
                "retweet_date": "",
                "translate": "",
                "trans_src": "",
                "trans_dest": ""
            }



            ]
        }
        print(tweets)
        return render(request, 'Target_Management_System/Twitter_Target_Response.html', {'tweets': tweets})




# this json wasnot according to format to formatted here
class LinkedinPerson_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        profile = {
            "GTR": "91",
            "target_type": "profile",
            "name": "Asma Shakeel",
            "headline": "I am Electrical Engineer specialization in DSSP. My passion is centered on Digital Design and Image Processing.",
            "company": "Rapidev DMCC",
            "school": "National University of Sciences and Technology (NUST)",
            "location": "Islamabad Gpo, Federal Capial &AJK, Pakistan",
            "image_url": "./data/linkedin/asma-shakeel.png",
            "followers": "",
            "email": "asma9t7@gmail.com",
            "phone": 'null',
            "connected": 'null',
            "websites": [],
            "target_update_count": 0,
            "profile_summary": "Asma Shakeel is a Linkedin user. Rapidev DMCC is the company where this user works. Islamabad Gpo, Federal Capial &AJK, Pakistan is the location from where Asma Shakeel belongs.  This user profile's summary is Highly focused and motivated Electrical Engineer, able to work collaboratively in a variety of settings, conditions, and\n\n      environments.. Email: asma9t7@gmail.com.  User interests are: Bill Gates , Sony , Microsoft , LinkedIn , Jack Welch , JT O'Donnell.  User skills are: Matlab , Intel Quartus Prime , Alliance CAD Tool. ",
            "current_company_link": "https://www.linkedin.com/company/rapidev-dmcc-dubai/",
            "skills": [
                {
                    "name": "Matlab",
                    "endorsements": 0
                },
                {
                    "name": "Intel Quartus Prime",
                    "endorsements": 0
                },
                {
                    "name": "Alliance CAD Tool",
                    "endorsements": 0
                }
            ],
            "experience": {
                "jobs": [
                    {
                        "title": "Hardware Design Internee",
                        "company": "Rapidev DMCC\n        Internship",
                        "date_range": "Oct 2019 \u2013 Present",
                        "location": "National Science and Technology Park Islamabad",
                        "description": 'null',
                        "li_company_url": "https://www.linkedin.com/company/rapidev-dmcc-dubai/"
                    }

                ],
                "education": [
                    {
                        "name": "National University of Sciences and Technology (NUST)",
                        "degree": "Masters in Science",
                        "grades": 'null',
                        "field_of_study": "Electrical Engineering",
                        "date_range": "2018 \u2013 2020",
                        "activities": 'null'
                    },
                    {
                        "name": "Government  College University, Faisalabad",
                        "degree": "Electrical Engineering",
                        "grades": "3.73/4",
                        "field_of_study": "Electrical and Electronics Engineering",
                        "date_range": "2014 \u2013 2018",
                        "activities": 'null'
                    },
                    {
                        "name": "Govt college for women karkhana bazar, Faisalabad",
                        "degree": "HSSC (PRE-ENGINEERING)",
                        "grades": "80%",
                        "field_of_study": "Engineering",
                        "date_range": "2012 \u2013 2014",
                        "activities": 'null'
                    },
                    {
                        "name": "Govt girls High School bhowana bazar, Faisalabad",
                        "degree": "MATRICULATION",
                        "grades": "80%",
                        "field_of_study": "Science",
                        "date_range": "2010 \u2013 2012",
                        "activities": 'null'
                    }
                ],
                "volunteering": [
                    {
                        "title": "Cordinator",
                        "company": "IEEE student branch gcuf",
                        "date_range": "Dec 2014 \u2013 Aug 2015",
                        "location": 'null',
                        "cause": "Education",
                        "description": 'null'
                    },
                    {
                        "title": "Chairperson",
                        "company": "IEEE WIE GCUF Student Branch",
                        "date_range": "Sep 2017 \u2013 Aug 2018",
                        "location": 'null',
                        "cause": "Education",
                        "description": 'null'
                    }
                ]
            },
            "interests": [
                "Bill Gates",
                "Sony",
                "Microsoft",
                "LinkedIn",
                "Jack Welch",
                "JT O'Donnell"
            ],
            "accomplishments": {
                "publications": [],
                "certifications": [],
                "patents": [],
                "courses": [
                    "ASIC Design Methodology ",
                    "Advance Digital Image Processing ",
                    "Advance Digital Signal Processing ",
                    "Advance Digital System Design ",
                    "Artificial Neural Network ",
                    "Computer Vision",
                    "Digital Signal Processing",
                    "Stochastic system",
                    "System Validation "
                ],
                "projects": [
                    "Carry Look-Ahead Adder Design Using Alliance CAD Tools                                       ",
                    "Interesting Games for Data Collection",
                    "Modeling Online Shopping Smart Contract in NuSMV",
                    "Non Linear Camera Calibration",
                    "Autonomous Fire/Heat control Droid ",
                    "Burgler Alarm(home security system)",
                    "Digital Temperature Sensor",
                    "Sensor Alarm using Thyristor"
                ],
                "honors": [
                    "1st Postion in HSSC(Pre Engineering) in Govt college for women karkhana Bazar"
                ],
                "test_scores": [],
                "languages": [
                    "English",
                    "Punjabi",
                    "urdu"
                ],
                "organizations": []
            },
            "field_of_interest": [
                "Electrical Engineering",
                "Electrical and Electronics Engineering",
                "Engineering",
                "Science"
            ],
            "experience_education_graph": [
                [],
                []
            ],
            "linked_to": []
        }
        return render(request, 'Target_Management_System/LinkedinPerson_Target_Response.html', {'profile': profile})
class Index(TemplateView):
    def get(self, request, *args, **kwargs):
          with open('static/Target_Json/facebook_page_data.json', 'r') as f:
            page = json.load(f)
            return render(request, 'Target_Management_System/test.html',{'page':page})
