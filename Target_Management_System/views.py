from django.shortcuts import render, redirect,reverse
import json
# Create your views here.
from django.http import JsonResponse
from django.views import View
from OSINT_System_Core.publisher import publish
from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager,Timeline_Manager
from Public_Data_Acquisition_Unit.mongo_models import PERIODIC_INTERVALS,Supported_Website

from bson import ObjectId
from django.http import HttpResponse, HttpResponseRedirect
from django_eventstream import send_event
from Keybase_Management_System.keybase_manager import Keybase_Manager
from System_Log_Management_Unit.system_log_manager import Data_Queries
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
dq = Data_Queries()
acq = Acquistion_Manager()
km = Keybase_Manager()
tl = Timeline_Manager()
from django.views.generic import TemplateView
from Data_Processing_Unit.models import Reddit_Profile_Response_TMS
from Data_Processing_Unit.models import Youtube_Response_TMS



class Bulk_Targets(View):
    
    def get(self,request,*args,**kwargs):
      
        if request.method=="GET":
            social_sites = acq.get_all_social_sites()
            intervals=PERIODIC_INTERVALS,
            print(social_sites)
            return render(request,'Target_Management_System/bulk_targets.html',{'social_sites':social_sites,'intervals':intervals})

    def post(self,request,*args,**kwargs):
       
        try:
            website=request.POST['website']
            target_type=int(request.POST['target_type'])
            interval=int(request.POST['interval'])
            expired_on= convert_expired_on_to_datetime(request.POST['expired_on'])
            screenshots=request.POST.get('screenshots',False)


            usernames=request.POST['usernames'].split(',')


            print(website,target_type,interval,expired_on, screenshots,usernames,type(usernames))

            resp = acq.add_bulk_targts(website_id=website,target_type_index=target_type,prime_argument_list=usernames,expired_on=expired_on,periodic_interval=interval)
            publish('bulk target successfull for '+str(usernames).strip('[]'))


        except Exception as e:
            print(e)
            publish(str(e),message_type='notification')

        return redirect('/tms/bulk_targets')








class Add_Target(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        # send all the supported sites objects with their target types

        social_sites = acq.get_all_social_sites()
        news_sites = acq.get_all_news_sites()
        blog_sites = acq.get_all_blog_sites()

        portfolio_id = ''
        prime_argument = ''
        target_site = ''

        if 'portfolio_id' in kwargs :portfolio_id = kwargs['portfolio_id']
        if 'prime_argument' in kwargs: prime_argument = kwargs['prime_argument']
        if 'target_site' in kwargs: target_site = kwargs['target_site']

        #print(kwargs['portfolio_id'])
        # print(social_sites.to_json())
        # data = serializers.serialize('json', social_sites.to_json(), fields=(
        #     'name', 'url', 'website_type', 'target_type'))
        data = {
            'social': json.loads(social_sites.to_json()),
            'news': json.loads(news_sites.to_json()),
            'blogs': json.loads(blog_sites.to_json()),
            'intervals':PERIODIC_INTERVALS,
            'portfolio_id':portfolio_id,
            'prime_argument':prime_argument,
            'target_site':target_site,
        }
        print(data)
        #publish('target created successfully', message_type='notification')
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


        try:

            print(request.POST)
            plateform = request.POST['platform']
            portfolio_id = request.POST.get('portfolio_id',None)
            if(not len(portfolio_id) >0): portfolio_id = None

            website_id = ObjectId(request.POST['website_id'])
            target_type_index = int(request.POST[plateform+'_authortype'])
            username = request.POST[plateform+'_autheruseraccount']
            user_id = request.POST[plateform+'_authoruserid']
            name = request.POST[plateform+'_authorusername']
            url = request.POST[plateform+'_authoruserurl']
            expire_on = request.POST[plateform+'_expirydate']
            interval = int(request.POST[plateform+'_interval'])
            screen_shot = bool(int(request.POST[plateform+'_screenshot']))
            print(screen_shot)

            print(portfolio_id)


            if (expire_on is not None):
                expire_on = convert_expired_on_to_datetime(expire_on)



            print(website_id,target_type_index,username,user_id)
            acq.add_target(website_id, target_type_index,portfolio_id=portfolio_id,username=username, user_id=user_id,name=name,url=url,expired_on=expire_on,periodic_interval=interval,need_screenshots=screen_shot)
            #publish('target created successfully', message_type='notification')

            if(portfolio_id is not None):
                return HttpResponseRedirect(reverse('Portfolio_Management_System:add_information',args=[portfolio_id]))

            return redirect('/tms/marktarget')
        except Exception as e:
            print(e)
            publish(str(e), message_type='error')
            return redirect('/tms/marktarget')


# ...................................................Views for SmartSearch

class Smart_Search(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        username = request.GET['author_account']
        search_site = request.GET['search_site']
        target_type_index = request.GET['target_type']

        entity_type = Supported_Website.get_target_type_by_index(search_site,target_type_index)




        print(username,search_site,entity_type)

        resp = acq.fetch_smart_search(username=username,search_site=search_site,entity_type=entity_type)
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

        target_site='facebook'
        if 'target_site' in kwargs:target_site = kwargs['target_site']

        resp = acq.get_fetched_targets(website=target_site)


        paginator = Paginator(resp, 6)
        page = request.GET.get('page')
        try:
            resp = paginator.page(page)
        except PageNotAnInteger:
            resp = paginator.page(1)
        except EmptyPage:
            resp = paginator.page(paginator.num_pages)
        return render(request,'Target_Management_System/tso_targetfetchview.html',{'targets':resp,'supported_sites':acq.get_all_supported_sites()})

    def post(self, request, *args, **kwargs):
        pass


class Identify_Target(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):
        return render(request,'Target_Management_System/tso_identifytarget.html',{})

class Identify_Target_Request(RequireLoginMixin, IsTSO, View):
    def get(self, request, *args, **kwargs):


        print(request.GET)
        query = request.GET['query']
        website = request.GET['website']

        print(query,website)
        resp = acq.identify_target(query,website)
        print(resp)

        users = []
        if(not 'response' in resp):

            if(not website == 'instagram'):
                data = resp['data']['data']
                print(data)
                for item in data:
                    #print(item)
                    user = {'target_site':website,'username': item['username'],'fullname': item['full_name'],'userid': item['id'],'profile_url':item['picture_url']}
                    users.append(user)
            elif (website == 'instagram'):
                data = resp['data']['users']
                print(data)
                for item in data:
                    # print(item)
                    user = {'target_site':website,'username': item['user']['username'], 'fullname': item['user']['full_name'], 'userid': '',
                            'profile_url': item['user']['profile_pic_url']}
                    users.append(user)

        print(users)
        return render(request,'Target_Management_System/identify_target_subtemplate.html',{'users':users})

class Target_Internet_Survey(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):
        print(request.GET)

        name = request.GET.get('name_lookup', None)
        email = request.GET.get('email_lookup', None)
        phone = request.GET.get('phone_lookup', None)
        address = request.GET.get('address_lookup', None)
        print(name, email, phone, address)

        if(name or email or phone or address ):

            # pass values to the user and wait for the response and show to the
            # same view
            #


            resp = acq.target_internet_survey(name, email, phone, address)
            print(resp)

            return render(request, 'Target_Management_System/tso_internetsurvey.html', {'results':resp})

        return render(request, 'Target_Management_System/tso_internetsurvey.html', {})



    def post(self, request, *args, **kwargs):

        print(request.POST)
        name = request.POST.get('name_lookup', '')
        email = request.POST.get('email_lookup', '')
        phone = request.POST.get('phone_lookup', '')
        address = request.POST.get('address_lookup','')
        print(name, email, phone, address)
        # pass values to the user and wait for the response and show to the
        # same view
        #resp = acq.target_internet_survey(name, email, phone, address)
        resp = {'data': [{'encoding': 'ascii', 'last_modified': 'Tue, 21 Apr 2020 09:51:30 GMT', 'meta_robots': '', 'meta_title': '.: Project in C/C++ : Password Protected Contact bookInformation technology Revolution', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 1, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p1.png', 'serp_domain': 'infotechrevol.blogspot.com', 'serp_rank': 1, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': "Aug 6, 2015 - ... need's to be correct or which might enhance the usability of the app you feel free to contact. awaisazam230@gmail.com. Please Comment !!", 'serp_title': '.: Project in C/C++ : Password Protected Contact bookinfotechrevol.blogspot.com › 2015/08 › project-in-cc-pas...', 'serp_type': 'results', 'serp_url': 'http://infotechrevol.blogspot.com/2015/08/project-in-cc-password-protected.html', 'serp_visible_link': 'infotechrevol.blogspot.com › 2015/08 › project-in-cc-pas...', 'status': 200, 'text_raw': 'Pages Home Books Thursday, August 2015 Project in C/C++ Password Protected Contact book Features 1.\nInstallation of the Application 2.\nPassword Protection 3.\nIntelligent Searching 4.\nAdd ,Remove Contact Description It is console based app the compiler used for the development is "Borland 5.02" this project can be used as semester project with any c/c++ course in schools/collages it is best for learning and enhancing your skills in c++ This application is programmed in C++ using "filestream" and some other basic libraries.\nFirst the user is asked to allow the installation of the app and while installing it ask user six character password and ask user to login for the first time.\nProjects in C++ Calendar display with add note and age finder in This project is coded in using CodeBlock compiler it has around 540 lines of code easy to understand for beginners in language and c...\nSonic Weapons To disperse crowds and prevent rioting, various forms of non-lethal weapons NLW are used.\nAmong these, interestingly, is sound.\nBlog Archive 2015 24 September August 15 Kepler-452b,The Most Similar Planet To Earth Till ...\nSome strange but true facts on our earth Projects in C++ Canteen Management System Projects in C++ Calendar display with add note a...\nbrilliant future technologies which will make li...\nProject in C/C++ Password Protected Contact book...\nVehicle Parking Management System in C++ Your fingerprints are remotely stolen by Hackers f...\nEdit your friends "Facebook Status" and take fake ...\nArduino Studio IDE launched latest gadgets that you must have How People Weld Under Water How The Skype Translator Works How Targeted Advertising Work Human v/s Robots July About Me Unknown View my complete profile What do you think about our blog posts ---|--- Picture Window theme.\nPowered by Blogger.\n', 'url': 'http://infotechrevol.blogspot.com/2015/08/project-in-cc-password-protected.html'}, {'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 1, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p1.png', 'serp_domain': 'apkpure.ai', 'serp_rank': 2, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': 'have 1 products. Developer link: Visit website , Email awaisazam230@gmail.com ,. FlyCopter APK · FlyCopter. Developer: Blutone · App Details. Popular Apps.', 'serp_title': 'Blutone APK list | APKPure.aiapkpure.ai › developer › blutone', 'serp_type': 'results', 'serp_url': 'https://apkpure.ai/developer/blutone/', 'serp_visible_link': 'apkpure.ai › developer › blutone'}, {'encoding': 'utf-8', 'last_modified': None, 'meta_robots': '', 'meta_title': ' Download Casual : Fly Copter 1.5 APK - Android Casual Games', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 1, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p1.png', 'serp_domain': 'apk-dl.com', 'serp_rank': 3, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': 'May 17, 2018 - Developer. Blutone. Installs. 50+. Price. Free. Category. Casual. Developer. awaisazam230@gmail.com. Google Play Link. Google Play Link\xa0...', 'serp_title': "Casual : Fly Copter 1.5 APK Download - Android Casual Gamesapk-dl.com › ... › {{trans('cats.' . cat_name(Casual))}}", 'serp_type': 'results', 'serp_url': 'https://apk-dl.com/casual-fly-copter/com.blutonegames.flycopter', 'serp_visible_link': "apk-dl.com › ... › {{trans('cats.' . cat_name(Casual))}}", 'status': 200, 'text_raw': "Hero is soldier and he is the only one left on hisbase.He has to fight against the enemies by using the optimumresourceshe has and also collect the power coins by which hisshootingcapability will be improved.\nHero has to fight till hislastbreadth, ammunition and health resources are dropped by therescueteam from above Show More...\nApp Information Casual Fly Copter App Name Casual Fly Copter Package Name com.blutonegames.flycopter Updated May 17, 2018 File Size Undefined Requires Android Android 4.0.3 and up Version 1.5 Developer Blutone Installs 50+ Price Free Category Casual Developer awaisazam230@gmail.com Google Play Link Google Play Link Blutone Show More...\nCasual Fly Copter 1.5 APK Blutone Free Flycopter is an intelligent flying enemy which attack on Hero'sbasestation.\nHero is soldier and he is the only one left on hisbase.He has to fight against the enemies by using the optimumresourceshe has and also collect the power coins by which hisshootingcapability will be improved.\nHero has to fight till hislastbreadth, ammunition and health resources are dropped by therescueteam from above Free Loading...\nAPK-DL APK Downloader Android Apps Android Games Contact Us Top Android Apps WIFI WPS WPA TESTER WPS Connect WordPress XPOSED IMEI Changer WhatsApp Messenger Top Android Games Clash of Clans Asphalt 8: Airborne Clash of Kings Case Clicker Mesgram Follow Us Facebook Twitter Apk-DL DMCA Disclaimer Privacy Policy Term of Use Contact Us\n", 'url': 'https://apk-dl.com/casual-fly-copter/com.blutonegames.flycopter'}, {'encoding': 'utf-8', 'last_modified': 'Mon, 27 Apr 2020 05:45:00 GMT', 'meta_robots': '', 'meta_title': '\n      Gmail: Secure Enterprise Email for Business | G Suite\n    ', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 1, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p1.png', 'serp_domain': 'gsuite.google.com', 'serp_rank': 1, 'serp_rating': None, 'serp_sitelinks': 'Email FeaturesContact Sales NowStart a Free Trial Now', 'serp_snippet': 'Google hosted email for @yourcompany.com. Try it free for 14 days. Make it your own domain with G Suite by Google Cloud. Get @yourbusiness.com. Draft Emails Offline. Google Email Hosting. Up To 30 Email Aliases. Automatic Reminders. Auto Suggest for Replies.', 'serp_title': 'Gmail For Business | Customise Your Gmail Address\u200eAd·gsuite.google.com/gmail\u200e', 'serp_type': 'ads_main', 'serp_url': 'https://gsuite.google.com/intl/en_sg/products/gmail/', 'serp_visible_link': 'gsuite.google.com/gmail', 'status': 200, 'text_raw': "See our tips for working from home with Suite, including video meetings.\nLearn more Gmail Secure, private, ad-free email for your business Gmail keeps you updated with real-time message notifications, and safely stores your important emails and data.\nIT admins can centrally manage accounts across your organization and devices.\nStart Free Trial Contact sales Get custom email @yourcompany Build customer trust by giving everyone in your company professional email address at your domain, like susan@yourcompany and joe@yourcompany.\nAlso create group mailing lists, like sales@yourcompany.\nWork without interruption Access your email anytime, anywhere, on any device—no Internet connection needed.\nRead and draft messages without connectivity, and they’ll be ready to send when you’re back online.\nElevate email conversations with chat and video For those moments when you need more than just email, join Meet video call or chat with colleague directly from your inbox.\nCompatible with your existing interface Gmail works great with desktop clients like Microsoft Outlook, Apple Mail and Mozilla Thunderbird.\nOutlook users can sync emails, events and contacts to and from Suite.\nEasy migration from Outlook and legacy services Migrate your email from Outlook, Exchange or Lotus easily with custom tools that help preserve your important messages.\n99.9% guaranteed uptime, 0% planned downtime Count on Google’s ultra-reliable servers to keep your lights on 24/7/365.\nAutomatic backups, spam protection and industry-leading security measures help protect your business data.\nSuite gave us reliable and convenient access to our emails and documents, regardless of our location.\nMr. Zhang Gixia Group Learn More Top questions about Gmail What's different about the paid version of Gmail?\nPaid Gmail features include: custom email @yourcompany.com unlimited group email addresses, 99.9% guaranteed uptime, twice the storage of personal Gmail, zero ads, 24/7 support, Suite Sync for Microsoft Outlook and more.\nCan user have more than one email address?\nuser can have several email addresses by creating email aliases.\nYou can add up to 30 email aliases for each user.\nCan migrate my existing email to Suite?\nSuite migration tools are available for importing your old emails from legacy environments, such as Microsoft®, IBM® Notes® and other email systems.\nFor more information on the tools available for data migrations into Suite, see Migrate your organisation’s data to Suite.\nStay in the loop Sign up for Google Cloud newsletters with product updates, event information, special offers and more.\nEmail Please enter valid email address.\nSelect one option.value Industry This is required Select one Number of Employees This is required Country Country country.countryName This is required Yes, sign me up for Google Cloud emails with news, product updates, event information, special offers and more.\nYou can unsubscribe at later time This is required Sign me up Thanks!\nWe’ll be in touch shortly.\n", 'url': 'https://gsuite.google.com/intl/en_sg/products/gmail/'}, {'encoding': 'ascii', 'last_modified': 'Tue, 21 Apr 2020 09:51:30 GMT', 'meta_robots': '', 'meta_title': '.: Project in C/C++ : Password Protected Contact bookInformation technology Revolution', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 2, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p2.png', 'serp_domain': 'infotechrevol.blogspot.com', 'serp_rank': 1, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': "Aug 6, 2015 - ... need's to be correct or which might enhance the usability of the app you feel free to contact. awaisazam230@gmail.com. Please Comment !!", 'serp_title': '.: Project in C/C++ : Password Protected Contact bookinfotechrevol.blogspot.com › 2015/08 › project-in-cc-password-protected', 'serp_type': 'results', 'serp_url': 'http://infotechrevol.blogspot.com/2015/08/project-in-cc-password-protected.html', 'serp_visible_link': 'infotechrevol.blogspot.com › 2015/08 › project-in-cc-password-protected', 'status': 200, 'text_raw': 'Pages Home Books Thursday, August 2015 Project in C/C++ Password Protected Contact book Features 1.\nInstallation of the Application 2.\nPassword Protection 3.\nIntelligent Searching 4.\nAdd ,Remove Contact Description It is console based app the compiler used for the development is "Borland 5.02" this project can be used as semester project with any c/c++ course in schools/collages it is best for learning and enhancing your skills in c++ This application is programmed in C++ using "filestream" and some other basic libraries.\nFirst the user is asked to allow the installation of the app and while installing it ask user six character password and ask user to login for the first time.\nProjects in C++ Calendar display with add note and age finder in This project is coded in using CodeBlock compiler it has around 540 lines of code easy to understand for beginners in language and c...\nSonic Weapons To disperse crowds and prevent rioting, various forms of non-lethal weapons NLW are used.\nAmong these, interestingly, is sound.\nBlog Archive 2015 24 September August 15 Kepler-452b,The Most Similar Planet To Earth Till ...\nSome strange but true facts on our earth Projects in C++ Canteen Management System Projects in C++ Calendar display with add note a...\nbrilliant future technologies which will make li...\nProject in C/C++ Password Protected Contact book...\nVehicle Parking Management System in C++ Your fingerprints are remotely stolen by Hackers f...\nEdit your friends "Facebook Status" and take fake ...\nArduino Studio IDE launched latest gadgets that you must have How People Weld Under Water How The Skype Translator Works How Targeted Advertising Work Human v/s Robots July About Me Unknown View my complete profile What do you think about our blog posts ---|--- Picture Window theme.\nPowered by Blogger.\n', 'url': 'http://infotechrevol.blogspot.com/2015/08/project-in-cc-password-protected.html'}, {'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 2, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p2.png', 'serp_domain': 'apkpure.ai', 'serp_rank': 2, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': 'have 1 products. Developer link: Visit website , Email awaisazam230@gmail.com ,. FlyCopter APK · FlyCopter. Developer: Blutone · App Details. Popular Apps.', 'serp_title': 'Blutone APK list | APKPure.aiapkpure.ai › developer › blutone', 'serp_type': 'results', 'serp_url': 'https://apkpure.ai/developer/blutone/', 'serp_visible_link': 'apkpure.ai › developer › blutone'}, {'encoding': 'utf-8', 'last_modified': None, 'meta_robots': '', 'meta_title': ' Download Casual : Fly Copter 1.5 APK - Android Casual Games', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 2, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p2.png', 'serp_domain': 'apk-dl.com', 'serp_rank': 3, 'serp_rating': None, 'serp_sitelinks': None, 'serp_snippet': 'May 17, 2018 - Developer. Blutone. Installs. 50+. Price. Free. Category. Casual. Developer. awaisazam230@gmail.com. Google Play Link. Google Play Link\xa0...', 'serp_title': "Casual : Fly Copter 1.5 APK Download - Android Casual Gamesapk-dl.com › Games › {{trans('cats.' . cat_name(Casual))}}", 'serp_type': 'results', 'serp_url': 'https://apk-dl.com/casual-fly-copter/com.blutonegames.flycopter', 'serp_visible_link': "apk-dl.com › Games › {{trans('cats.' . cat_name(Casual))}}", 'status': 200, 'text_raw': "Hero is soldier and he is the only one left on hisbase.He has to fight against the enemies by using the optimumresourceshe has and also collect the power coins by which hisshootingcapability will be improved.\nHero has to fight till hislastbreadth, ammunition and health resources are dropped by therescueteam from above Show More...\nApp Information Casual Fly Copter App Name Casual Fly Copter Package Name com.blutonegames.flycopter Updated May 17, 2018 File Size Undefined Requires Android Android 4.0.3 and up Version 1.5 Developer Blutone Installs 50+ Price Free Category Casual Developer awaisazam230@gmail.com Google Play Link Google Play Link Blutone Show More...\nCasual Fly Copter 1.5 APK Blutone Free Flycopter is an intelligent flying enemy which attack on Hero'sbasestation.\nHero is soldier and he is the only one left on hisbase.He has to fight against the enemies by using the optimumresourceshe has and also collect the power coins by which hisshootingcapability will be improved.\nHero has to fight till hislastbreadth, ammunition and health resources are dropped by therescueteam from above Free Loading...\nAPK-DL APK Downloader Android Apps Android Games Contact Us Top Android Apps WIFI WPS WPA TESTER WPS Connect WordPress XPOSED IMEI Changer WhatsApp Messenger Top Android Games Clash of Clans Asphalt 8: Airborne Clash of Kings Case Clicker Mesgram Follow Us Facebook Twitter Apk-DL DMCA Disclaimer Privacy Policy Term of Use Contact Us\n", 'url': 'https://apk-dl.com/casual-fly-copter/com.blutonegames.flycopter'}, {'encoding': 'utf-8', 'last_modified': 'Mon, 27 Apr 2020 05:45:00 GMT', 'meta_robots': '', 'meta_title': '\n      Gmail: Secure Enterprise Email for Business | G Suite\n    ', 'query': 'awaisazam230@gmail.com', 'query_num_results_page': 4, 'query_num_results_total': '0', 'query_page_number': 2, 'screenshot': './KBM/screenshots/2020-04-30/google_awaisazam230@gmail.com-p2.png', 'serp_domain': 'gsuite.google.com', 'serp_rank': 1, 'serp_rating': None, 'serp_sitelinks': 'Email FeaturesContact Sales NowStart a Free Trial Now', 'serp_snippet': 'Get Gmail for your domain with G Suite. Start your free 14-day trial now. Make it your own domain with G Suite by Google Cloud. Get @yourbusiness.com. Custom Business Email. Draft Emails Offline. Save Time w/ Smart Reply. Phishing Protection. Automatic Reminders.', 'serp_title': 'Gmail For Business | Get @yourbusiness.com Gmail\u200eAd·gsuite.google.com/gmail\u200e', 'serp_type': 'ads_main', 'serp_url': 'https://gsuite.google.com/intl/en_sg/products/gmail/', 'serp_visible_link': 'gsuite.google.com/gmail', 'status': 200, 'text_raw': "See our tips for working from home with Suite, including video meetings.\nLearn more Gmail Secure, private, ad-free email for your business Gmail keeps you updated with real-time message notifications, and safely stores your important emails and data.\nIT admins can centrally manage accounts across your organization and devices.\nStart Free Trial Contact sales Get custom email @yourcompany Build customer trust by giving everyone in your company professional email address at your domain, like susan@yourcompany and joe@yourcompany.\nAlso create group mailing lists, like sales@yourcompany.\nWork without interruption Access your email anytime, anywhere, on any device—no Internet connection needed.\nRead and draft messages without connectivity, and they’ll be ready to send when you’re back online.\nElevate email conversations with chat and video For those moments when you need more than just email, join Meet video call or chat with colleague directly from your inbox.\nCompatible with your existing interface Gmail works great with desktop clients like Microsoft Outlook, Apple Mail and Mozilla Thunderbird.\nOutlook users can sync emails, events and contacts to and from Suite.\nEasy migration from Outlook and legacy services Migrate your email from Outlook, Exchange or Lotus easily with custom tools that help preserve your important messages.\n99.9% guaranteed uptime, 0% planned downtime Count on Google’s ultra-reliable servers to keep your lights on 24/7/365.\nAutomatic backups, spam protection and industry-leading security measures help protect your business data.\nSuite gave us reliable and convenient access to our emails and documents, regardless of our location.\nMr. Zhang Gixia Group Learn More Top questions about Gmail What's different about the paid version of Gmail?\nPaid Gmail features include: custom email @yourcompany.com unlimited group email addresses, 99.9% guaranteed uptime, twice the storage of personal Gmail, zero ads, 24/7 support, Suite Sync for Microsoft Outlook and more.\nCan user have more than one email address?\nuser can have several email addresses by creating email aliases.\nYou can add up to 30 email aliases for each user.\nCan migrate my existing email to Suite?\nSuite migration tools are available for importing your old emails from legacy environments, such as Microsoft®, IBM® Notes® and other email systems.\nFor more information on the tools available for data migrations into Suite, see Migrate your organisation’s data to Suite.\nStay in the loop Sign up for Google Cloud newsletters with product updates, event information, special offers and more.\nEmail Please enter valid email address.\nSelect one option.value Industry This is required Select one Number of Employees This is required Country Country country.countryName This is required Yes, sign me up for Google Cloud emails with news, product updates, event information, special offers and more.\nYou can unsubscribe at later time This is required Sign me up Thanks!\nWe’ll be in touch shortly.\n", 'url': 'https://gsuite.google.com/intl/en_sg/products/gmail/'}]}

        print(resp)

        #pass the response to front end and show it to user
        # return JsonResponse(resp, safe=False)
        #return render(request,'Target_Management_System/tso_internetsurvey.html',{'result': resp})
        return HttpResponseRedirect(reverse('Target_Management_System:tms_internetsurvey',kwargs={'resp':resp}))

class Keybase_Crawling(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):

        keybases = km.get_all_keybases()
        return render(request,
                      'Target_Management_System/keybase_crawling.html',
                      {'keybases':keybases,'intervals':PERIODIC_INTERVALS,})


    def post(self,request):
        try:
           
           
            fb=False;
            instagram=False;
            linkedin=False;
            twitter=False;
            reddit=False;
            reddit=False;
            youtube=False;
            if 'fb' in request.POST:
                fb=True;
            else:
                fb=False;
                
            if 'instagram' in request.POST:
                instagram=True;
            else:
                instagram=False;
                
            if 'linkedin' in request.POST:
                linkedin=True;
            else:
                linkedin=False;
                
            if 'twitter' in request.POST:
                twitter=True;
            else:
                twitter=False;  
                 
            if 'reddit' in request.POST:
                reddit=True;
            else:
                reddit=False;
                
            if 'youtube' in request.POST:
                youtube=True;
            else:
                youtube=False;
            social_sites={ 
                            "fb":fb,
                            "instagram":instagram,
                            "linkedin":linkedin, 
                            "twitter":twitter, 
                            "reddit":reddit,
                            "youtube":youtube, }
            
            

           
            title = request.POST.get('title',None)
            website_id = acq.get_custom_webiste_id()
            target_type = 0

            keybase_id = request.POST.get('keybase',None)
            interval = int(request.POST.get('interval',None))
            expire_date = request.POST.get('expire_on',None)

            keybase_ref = km.get_keybase_object_by_id(keybase_id)

            if(expire_date is not None):
                expire_on = convert_expired_on_to_datetime(expire_date)


            acq.add_target(website_id,target_type,None,title=title,keybase_ref=keybase_ref,expired_on=expire_on,periodic_interval=interval,social_sites=social_sites)
            print("###################################")
            print(social_sites)
            return HttpResponseRedirect(reverse('Target_Management_System:tms_keybase_crawling'))
        except Exception as e:
            print(e)
            publish(str(e),module_name=__name__,message_type='error')
            return HttpResponseRedirect(reverse('Target_Management_System:tms_keybase_crawling'))

class Dyanamic_Crawling(RequireLoginMixin, IsTSO, View):

    def get(self, request, *args, **kwargs):

        url = None
        if('url' in kwargs): url = kwargs['url']
        if(url is not None):
            url = url.replace(' ','/')


        return render(request,
                      'Target_Management_System/tso_dynamiccrawling.html',
                      {'app': 'target','url':url})

    def post(self, request, *args, **kwargs):


        website_id = acq.get_custom_webiste_id()
        target_type_index = 1
        page_url = request.POST.get('page_url',False)

        links =bool(request.POST.get('links',False))
        headings =bool(request.POST.get('headings',False))
        paragraphs =bool(request.POST.get('paragraphs',False))
        pictures =bool(request.POST.get('pictures',False))
        videos =bool(request.POST.get('videos',False))
        ip =bool(request.POST.get('ip',False))


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


class Timeline(RequireLoginMixin, IsTSO, View):

    def get(self,request,*args,**kwargs):

        return render(request,'Target_Management_System/timeline.html',{})

class Timeline_Fetch(RequireLoginMixin,IsTSO,View):

    def get(self,request,*args,**kwargs):

        top = int(request.GET.get('top','10'))
        posts = tl.fetch_posts_for_timeline(top)
        #print(posts)

        return render(request,'Target_Management_System/timeline_subtemplate.html',{'posts':posts})


def convert_expired_on_to_datetime(expired_on):
    import datetime
    expired_onn = expired_on + ' 13:55:26'
    expired_onnn = datetime.datetime.strptime(expired_onn, '%Y-%m-%d %H:%M:%S')
    return expired_onnn



# ahmed code
# INSTAGRAM
class Instagram_Target_Response(TemplateView):
       template_name = "Target_Management_System/InstagramPerson_Target_Response.html"
       def get(self, request, *args, **kwargs):
            object_gtr_id = kwargs['object_gtr_id']
            profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
            print(profile.to_mongo())
            return render(request, 'Target_Management_System/InstagramPerson_Target_Response.html', {'profile': profile})

class Instagram_Target_Report(TemplateView):
       template_name = "Target_Management_System/InstagramPerson_Target_Report.html"
       def get(self, request, *args, **kwargs):
            object_gtr_id = kwargs['object_gtr_id']
            profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
            print(profile.to_mongo())
            return render(request, 'Target_Management_System/InstagramPerson_Target_Report.html', {'profile': profile})




# LINKEDIN
class LinkedinCompany_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())

        with open('static/Target_Json/linkedin_companyr_data.json', 'r') as f:
            company = json.load(f)

        return render(request, 'Target_Management_System/LinkedinCompany_Target_Response.html', {'company': data_object})


class LinkedinCompany_Target_Report(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())
        with open('static/Target_Json/linkedin_companyr_data.json', 'r') as f:
            company = json.load(f)
        return render(request, 'Target_Management_System/LinkedinCompany_Target_Report.html', {'company': data_object})
    
class LinkedinPerson_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())


        return render(request, 'Target_Management_System/LinkedinPerson_Target_Response.html', {'profile': data_object})

class LinkedinPerson_Target_Report(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())


        return render(request, 'Target_Management_System/LinkedinPerson_Target_Report.html', {'profile': data_object})

# FACEBOOK
class FacebookPerson_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.work)


        with open('static/Target_Json/facebook_person_data.json', 'r') as f:
            profile = json.load(f)
        return render(request, 'Target_Management_System/FacebookPerson_Target_Response.html',{'profile': data_object})

class FacebookPage_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())

        with open('static/Target_Json/facebook_page_data.json', 'r') as f:
            page = json.load(f)
        return render(request, 'Target_Management_System/FacebookPage_Target_Response.html',{'page': data_object})


class FacebookGroup_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())
        with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            group = json.load(f)
        return render(request, 'Target_Management_System/FacebookGroup_Target_Response.html',{'group': data_object})

class FacebookPersonReport(TemplateView):
    def get(self,request,*args,**kwargs):
         object_gtr_id = kwargs['object_gtr_id']
         data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
         print(data_object.to_mongo())

         with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            profile = json.load(f)
         return render(request,'Target_Management_System/FacebookPerson_Target_Report.html',{'profile':data_object})



class FacebookPageReport(TemplateView):
    def get(self,request,*args,**kwargs):
         object_gtr_id = kwargs['object_gtr_id']
         data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
         print(data_object.to_mongo())

         with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            page = json.load(f)
         return render(request,'Target_Management_System/FacebookPage_Target_Report.html',{'page':data_object})



class FacebookGroupReport(TemplateView):
    def get(self,request,*args,**kwargs):
         object_gtr_id = kwargs['object_gtr_id']
         data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
         print(data_object.to_mongo())

         with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            group = json.load(f)
         return render(request,'Target_Management_System/FacebookGroup_Target_Report.html',{'group':data_object})



# TWITTER

# this json wasnot according to format to formatted here
class Twitter_Target_Response(TemplateView):
    def get(self, request, *args, **kwargs):

        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(data_object.to_mongo())




        #print(tweets)
        return render(request, 'Target_Management_System/Twitter_Target_Response.html', {'tweets': data_object})




class Twitter_Target_Report(TemplateView):
    def get(self,request,*args,**kwargs):
         object_gtr_id = kwargs['object_gtr_id']
         data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
         print(data_object.to_mongo())

         return render(request,'Target_Management_System/Twitter_Target_Report.html',{'tweets':data_object})

    


# this json wasnot according to format to formatted here



#view for link analysis graph

class Link_Analysis(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id)).to_mongo()
        #print(data_object['linked_to'][1])
        #data = convert_facebook_indirect_links_to_graph(link_data)

        if(len(data_object['linked_to'][1]) > 0):

            resp = convert_facebook_indirect_links_to_graph(data_object['linked_to'][1])
            resp=json.loads(resp)    
            for i in resp:
                if i['image']==None:
                    i['image']='data:image/png;base64,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'
                
            resp=json.dumps(resp)
                
            
            return render(request,'Target_Management_System/link_analysis_amcharts.html',{'data':resp})
        else:
            return render(request, 'Target_Management_System/link_analysis_amcharts.html', {})


class Close_Associates_Tree_Graph(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id)).to_mongo()
        #print(data_object['linked_to'][1])
        #data = convert_facebook_indirect_links_to_graph(link_data)

        if(len(data_object['close_associates']) > 0):

            alpha_node,beta_node_list = dq.generalize_data_for_nodes('facebook','profile',data_object)
            resp =  dq.convert_nodes_to_graph_data(alpha_node,beta_node_list)

            print(resp)
            return render(request,'Target_Management_System/link_analysis.html',{'data':resp})
        else:
            return render(request, 'Target_Management_System/link_analysis.html', {})

class Instagram_Follower_Tree_Graph(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id)).to_mongo()
        #print(data_object['linked_to'][1])
        #data = convert_facebook_indirect_links_to_graph(link_data)

        if(len(data_object['followers']) > 0):

            alpha_node,beta_node_list = dq.generalize_data_for_nodes('instagram','profile',data_object)
            resp =  dq.convert_nodes_to_graph_data(alpha_node,beta_node_list)

            print(resp)
            return render(request,'Target_Management_System/link_analysis.html',{'data':resp})
        else:
            return render(request, 'Target_Management_System/link_analysis.html', {})

class Twitter_Follower_Tree_Graph(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id)).to_mongo()
        #print(data_object['linked_to'][1])
        #data = convert_facebook_indirect_links_to_graph(link_data)

        if(len(data_object['followers']) > 0):

            alpha_node,beta_node_list = dq.generalize_data_for_nodes('twitter','profile',data_object)
            resp =  dq.convert_nodes_to_graph_data(alpha_node,beta_node_list)

            print(resp)
            return render(request,'Target_Management_System/link_analysis.html',{'data':resp})
        else:
            return render(request, 'Target_Management_System/link_analysis.html', {})


# REDDIT 
class Reddit_Target_Response(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(profile.to_mongo())
        return render(request,'Target_Management_System/Reddit_Target_Response.html',{'profile':profile})
    
    
class Reddit_Target_Report(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(profile.to_mongo())
        return render(request,'Target_Management_System/Reddit_Target_Report.html',{'profile':profile})
    
   # YOUTUBE  
class Youtube_Target_Response(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        channel = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(channel.to_mongo())

        return render(request,'Target_Management_System/Youtube_Target_Response.html',{'channel':channel})
 
class Youtube_Target_Report(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        channel = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(channel.to_mongo())

        return render(request,'Target_Management_System/Youtube_Target_Report.html',{'channel':channel})
  
  # DYNAMIC CRAWLING   
class Dynamic_Crawling_Target(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        target = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(target.to_mongo())
        return render(request,'Target_Management_System/Dynamic_Crawling_Target.html',{'target':target})
    
class Dynamic_Crawling_Report(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        target = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(target.to_mongo())
        return render(request,'Target_Management_System/Dynamic_Crawling_Report.html',{'target':target})
    
# SUBREDDIT 

class Subreddit_Target_Resposne(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        subreddit_profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(subreddit_profile.to_mongo())
        return render(request,'Target_Management_System/Subreddit_Target_Resposne.html',{'subreddit_profile':subreddit_profile})




class Subreddit_Target_Report(View):
    def get(self,request,*args,**kwargs):
        object_gtr_id = kwargs['object_gtr_id']
        subreddit_profile = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
        print(subreddit_profile.to_mongo())
        return render(request,'Target_Management_System/Subreddit_Target_Report.html',{'subreddit_profile':subreddit_profile})




def convert_facebook_indirect_links_to_graph(data):

    n_data = []

    for i,item in enumerate(data):

        print(item)
        if(not username_exists(item['username'],n_data)):
            node = {'name': item['username'],
                    'value': 1,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": acq.get_picture_by_facebook_username(item['username']),
                    }
            linkwith = set()

            for y in data:
                if(item['username']==y['username']):
                    linkwith.add(y['mutual_close_associate'])

            node['linkWith'] = list(linkwith)

            n_data.append(node)

    for i,item in enumerate(data):

        #print(item)
        if(not username_exists(item['mutual_close_associate'],n_data)):
            node = {'name': item['mutual_close_associate'],
                    'value': 0.5,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": acq.get_picture_by_facebook_username(item['mutual_close_associate']),
                    }

            linkwith = set()

            for y in data:
                if(item['mutual_close_associate']==y['mutual_close_associate']):
                    linkwith.add(y['username'])
                    linkwith.add(y['username'])
                    linkwith.add(y['username'])
                    linkwith.add(y['username'])

            node['linkWith'] = list(linkwith)

            n_data.append(node)


    print(n_data)
    return json.dumps(n_data)


def username_exists(username,n_data):
    for item in n_data:
        if(username == item['name']):
            return True

    return False


class Graph(View):
    def get(self,request,*args,**kwargs):
        
         object_gtr_id = kwargs['object_gtr_id']
         data_object = acq.get_data_response_object_by_gtr_id(ObjectId(object_gtr_id))
         print(data_object.to_mongo())

         with open('static/Target_Json/facebook_group_data.json', 'r') as f:
            profile = json.load(f)
         return render(request,'Target_Management_System/Facebook_Target_Graph.html',{'profile':data_object})
