from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse,render
from bson import ObjectId
from Avatar_Management_Unit.models import *
import datetime
import json

class Create_Avatar(View):

    def get(self, request, *args, **kwargs):
        a = Avatar_AMS()
        avatars = json.loads(a.get_all_avatars_id_and_names().to_json())
        ctx = {}
        ctx['avatars'] = []
        for avatar in avatars:
            ctx['avatars'].append([
                avatar['_id']['$oid'],
                avatar['first_name'] + ' ' + avatar['last_name']
            ])
        print(ctx)
        return render(
            request, 'Avatar_Management_Unit/avatar.html', ctx)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        email = request.POST.get('pinfo-email')
        if not request.POST.get('pinfo-fname') == '':
            fname = request.POST.get('pinfo-fname')
        else:
            fname = None
        if not request.POST.get('pinfo-lname') == '':
            lname = request.POST.get('pinfo-lname')
        else:
            lname = None
        if not request.POST.get('pinfo-phone') == '':
            phone = request.POST.get('pinfo-phone')
        else:
            phone = None
        if not request.POST.get('pinfo-nationality') == '':
            nationality = request.POST.get('pinfo-nationality')
        else:
            nationality = None
        if not request.POST.get('pinfo-address') == '':
            address = request.POST.get('pinfo-address')
        else:
            address = None
        if not request.POST.get('pinfo-religious') == '':
            religious = request.POST.get('pinfo-religious')
        else:
            religious = None
        if not request.POST.get('pinfo-marital-status') == '':
            marital_status = request.POST.get('pinfo-marital-status')
        else:
            marital_status = None
        if not request.POST.get('pinfo-dob') == '':
            dob = request.POST.get('pinfo-dob')
        else:
            dob = None
        gender = request.POST.get('pinfo-gender')

        print(
            email,
            fname,
            lname,
            phone,
            nationality,
            address,
            religious,
            marital_status,
            dob,
            gender)
        a = Avatar_AMS()
        a.create(
            email,
            first_name=fname,
            last_name=lname,
            phone=phone,
            nationality=nationality,
            address=address,
            religious_views=religious,
            gender=gender,
            marital_status=marital_status,
            birthday=dob
        )

        return JsonResponse({'success': 200})


class Add_Work(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request, *args, **kwargs):

        avatar_id = request.POST.get('wd-avatar')
        job_title = request.POST.get('wd-job-title')
        company = request.POST.get('wd-company')
        if request.POST.get('wd-desc') != '':
            description = request.POST.get('wd-desc')
        else:
            description = None
        if request.POST.get('wd-address') != '':
            address = request.POST.get('wd-address')
        else:
            address = None
        if request.POST.get('wd-start-date') != '':
            start_date = datetime.datetime.strptime(request.POST.get('wd-start-date'), '%m/%d/%Y')
        else:
            start_date = None
        if request.POST.get('wd-end-date') != '':
            end_date = datetime.datetime.strptime(request.POST.get('wd-end-date'), '%m/%d/%Y')
        else:
            end_date = None
        if request.POST.get('wd-current-job') == 'true':
            current_job = True
        else:
            current_job = False
        try:
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            amu_obj.add_work(
                job_title,
                company,
                address,
                description,
                start_date,
                end_date,
                current_job)
            return JsonResponse({'success': 200})
        except Exception as e:
            print(e)
            return JsonResponse({'error': e})


class Add_Education(View):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        avatar_id = request.POST.get('le-ef-avatar')
        degree = request.POST.get('le-ef-degree')
        institute = request.POST.get('le-ef-institute')
        if request.POST.get('le-ef-grade') != '':
            grade = request.POST.get('le-ef-grade')
        else:
            grade = None
        if request.POST.get('le-ef-fieldofstudy') != '':
            field_of_study = request.POST.get('le-ef-fieldofstudy')
        else:
            field_of_study = None
        start_date = datetime.datetime.strptime(
            request.POST.get('le-ef-start-date'), '%m/%d/%Y')
        if request.POST.get('le-ef-end-date') != '':
            end_date = datetime.datetime.strptime(
                request.POST.get('le-ef-end-date'), '%m/%d/%Y')
        else:
            end_date = None
        print(avatar_id, degree, institute, grade, field_of_study, start_date, end_date)
        try:
            print('pre error')
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            print('no error')
            if(amu_obj is not None):
                amu_obj.add_education(
                    institute,
                    degree,
                    grade,
                    field_of_study,
                    start_date,
                    end_date)
            return JsonResponse({'success': 200})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})

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

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        avatar_id = request.POST.get('i-avatar')
        hobbies = request.POST.getlist('hobbies[]')
        movies = request.POST.getlist('movies[]')
        songs = request.POST.getlist('songs[]')

        # print(avatar_id, hobbies, movies, songs)

        # try:
        #     a = Avatar_AMS.get_object_by_id(avatar_id)
        #     if(a is not None):
        #         a.add_interests(hobbies, movies, songs)

        #     return JsonResponse({'success': 200})
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({'error':str(e)})

class Add_Life_Event(View):


    def post(self, request, *args, **kwargs):

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


class Avatar_Archive(View):

    def get(self,request):
        avatars = Avatar_AMS.get_all_avatars()
        return None


class Add_Marriage(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        avatar_id = request.POST.get('le-m-avatar')
        spouse = request.POST.get('le-m-spouse')
        if request.POST.get('le-m-location') != '':
            location = request.POST.get('le-m-location')
        else:
            location = None
        wedding_date = datetime.datetime.strptime(request.POST.get('le-m-wedding-date'), '%m/%d/%Y')
        if request.POST.get('le-m-divorce-date') != '':
            divorce_date = datetime.datetime.strptime(request.POST.get('le-m-divorce-date'), '%m/%d/%Y')
        else:
            divorce_date = None
        try:
            avatar_obj = Avatar_AMS.get_object_by_id(avatar_id)
            avatar_obj.add_marriage(spouse, location, wedding_date, divorce_date)
            return JsonResponse({'success': 200})
        except Exception as e:
            return JsonResponse({'error': str(e)})
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