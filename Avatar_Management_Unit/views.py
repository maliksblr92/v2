from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse,render
from django.contrib import messages
from bson import ObjectId
from Avatar_Management_Unit.models import *
from Avatar_Management_Unit.avatar_action_manager import Avatar_Action
import datetime
import json

aa = Avatar_Action('majidahmed.123@outlook.com','someonesomeone','facebook')

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
        fname = request.POST.get('pinfo-fname')
        lname = request.POST.get('pinfo-lname')
        email = request.POST.get('pinfo-email')
        phone = request.POST.get('pinfo-phone')
        nationality = request.POST.get('pinfo-nationality')
        address = request.POST.get('pinfo-address')
        religious = request.POST.get('pinfo-religious')
        marital_status=request.POST.get('pinfo-marital-status')
        dob=request.POST.get('pinfo-dob')
        gender=request.POST.get('pinfo-gender')
       
    
        # saving to model
        a = Avatar_AMS()
        a.create(
          
            first_name=fname,
            last_name=lname,
            email=email,
            phone=phone,
            nationality=nationality,
            address=address,
            religious_views=religious,
            gender=gender,
            marital_status=marital_status,
            birthday=dob,
        )
        if(a):
           
            messages.success(request, 'Avatar created successfully')
            return redirect('/amu/archive')
        else:
            messages.error(request, 'Failed to cerate avatar .... please  try again')
            return redirect('/amu/avatar')


class Add_Work(View):

    def get(self, request, *args, **kwargs):
        details_type=kwargs.get('details_type')
        avatar_id=kwargs.get('avatar_id')
        avatar=Avatar_AMS.get_object_by_id(avatar_id)
        return render(request,'Avatar_Management_Unit/add_work.html',{'details_type':details_type,'avatar':avatar});
    def post(self, request, *args, **kwargs):
        # essential for redirects
        details_type=kwargs['details_type'] 
        avatar_id =kwargs['avatar_id'] 
        # form == work details form
        if(details_type == 'work_details'): 
            job_title = request.POST.get('wd-job-title')
            company = request.POST.get('wd-company')
            description = request.POST.get('wd-desc')
            address = request.POST.get('wd-address')
            start_date = request.POST.get('wd-start-date')
            end_date = request.POST.get('wd-end-date')
            current_job=request.POST.get('wd-current-job')
            if(current_job == 'true'):
                current_job=True
            else:
                current_job=False
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            db_status=amu_obj.add_work(
                title=job_title,
                company=company,
                location=address,
                description=description,
                start_date=start_date,
                end_date=end_date,
                is_current=current_job)
                    # details added == succesfull
            if(db_status):
                
                messages.success(request, 'Work Details added successfully ')
                return redirect('/amu/archive')
                    # details insertion == fail 
            else:
                messages.success(request, 'Work Details insertion failed ')
                return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        
        # if form  == intrest form
        if(details_type == 'intrest'):
            hobbies=request.POST.getlist('ihobbies')
            movies=request.POST.getlist('imovies')
            songs=request.POST.getlist('isongs')
            print(request.POST.getlist('ihobbies'))
            print(movies)
            print(songs)
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            db_status=amu_obj.add_interests(
                hobbies=hobbies,
                movies=movies,
                songs=songs,
              )
            # details added == succesfull
            if(db_status):
                messages.success(request, 'Avatar Intrests added successfully')
                return redirect('/amu/archive')
            # details insertion == fail 
            else:
                return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        
        if(details_type == 'biography'):
            print("+++++++++++++BIOGRAPHY FORM ++++++++++++++++++++")
            biography_text=request.POST.get('b-biography')
            print(biography_text)
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            db_status=amu_obj.add_biography(
                biography=biography_text,
              )
            # details added == succesfull
            if(db_status):
                messages.success(request, 'Avatar Biography  added successfully')
                return redirect('/amu/archive')
            # details insertion == fail 
            else:
                return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        
        
        if(details_type == 'social_account'):
            print("+++++++++++++SOCIAL ACCOUNT FORM ++++++++++++++++++++")
            platform_name=request.POST.get('sma-platform')
            first_name=request.POST.get('sma-first-name')
            last_name=request.POST.get('sma-last-name')
            email=request.POST.get('sma-email')
            password=request.POST.get('sma-password')
            phone=request.POST.get('sma-phone')
            username=request.POST.get('sma-username')
            dob=request.POST.get('sma-dob')
            gender=request.POST.get('sma-gender')
            
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            db_status=amu_obj.add_social_accounts(
            social_media_type=platform_name, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password, 
            phone_number=phone,
            user_name=username,
            dob=dob,
            gender=gender)
            # details added == succesfull
            if(db_status):
                messages.success(request, 'Avatar Social Account  added successfully')
                return redirect('/amu/archive')
            # details insertion == fail 
            else:
                return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        
        if(details_type == 'post'):
            print("+++++++++++++SOCIAL POST FORM ++++++++++++++++++++")
            platform_name=request.POST.get('smp-platform')
            post_text=request.POST.get('smp-text')
            post_date=request.POST.get('smp-date')

            
            amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
            db_status=amu_obj.add_social_post(social_media_type=platform_name, post=post_text, post_date=post_date)
            # details added == succesfull
            if(db_status):
                messages.success(request, 'Avatar Social Post  added successfully')
                return redirect('/amu/archive')
            # details insertion == fail 
            else:
                return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        
        # if form  == events form
        if(details_type == 'events'):
            # for education form--
            form_name=request.POST.get('form_name')
          
            if(form_name == "education_form" ):
                print('+++++++++++++++++++++++++++++++++++++')
                print("IN EDUCATION FORM ")
                print('+++++++++++++++++++++++++++++++++++++')
                institute=request.POST.get('le-ef-institute')
                degree=request.POST.get('le-ef-degree')
                grades=request.POST.get('le-ef-grade')
                field_of_study=request.POST.get('le-ef-fieldofstudy')
                start_date=request.POST.get('le-ef-start-date')
                end_date=request.POST.get('le-ef-end-date')
            #    add data to model object
                amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
                db_status=amu_obj.add_education(
                        institute=institute,
                        degree=degree,
                        grades=grades,
                        field_of_study=field_of_study,
                        start_date=start_date,
                        end_date=end_date)
               
                # details added == succesfull
                if(db_status):
                    messages.success(request, 'Avatar Education Details  added successfully')
                    return redirect('/amu/archive')
                # details insertion == fail 
                else:
                    return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
            if(form_name == "marriage_form"):
                # get form fields
                spouse=request.POST.get('le-m-spouse')
                location=request.POST.get('le-m-location')
                wedding_date=request.POST.get('le-m-wedding-date')
                divorce_date=request.POST.get('le-m-divorce-date')
                # 
                amu_obj = Avatar_AMS.get_object_by_id(avatar_id)
                db_status=amu_obj.add_marriage(
                spouse=spouse,
                location=location,
                wedding_date=wedding_date,
                divorce_date=divorce_date)
                if(db_status):
                    messages.success(request, 'Avatar Marriage Details  added successfully')
                    return redirect('/amu/archive')
                # details insertion == fail 
                else:
                    return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})
        return redirect('/amu/archive',{'details_type':details_type,'avatar_id':avatar_id})


class Explore (View):
    def get(self,request,*args,**kwargs):
        avatar_id=kwargs.get('avatar_id')
        a = Avatar_AMS()
        avatar=a.get_object_by_id(avatar_id)
        return render(request,'Avatar_Management_Unit/explore.html',{'resp':avatar})
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

        try:
            a = Avatar_AMS.get_object_by_id(avatar_id)
            if(a is not None):
                a.add_interests(hobbies, movies, songs)

            return JsonResponse({'success': 200})
        except Exception as e:
            print(e)
            return JsonResponse({'error':str(e)})

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

class Add_Biography(View):
    def post(self, request, *args, **kwargs):
        avatar_id = request.POST.get('b-avatar')
        if request.POST.get('b-biography') != '':
            biography = request.POST.get('b-biography')
        else:
            biography = None
        try:
            avatar_obj = Avatar_AMS.get_object_by_id(avatar_id)
            avatar_obj.add_biography(biography)
            return JsonResponse({'success': 200})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})


class Add_Social_Account(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('on Create avatar')

    def post(self, request):

        print(request.POST)
        avatar_id = request.POST.get('sma-avatar')
        if request.POST.get('sma-platform') != '':
            sma_platform = request.POST.get('sma-platform')
        else:
            sma_platform = None
        if request.POST.get('sma-first-name') != '':
            sma_first_name = request.POST.get('sma-first-name')
        else:
            sma_first_name = None
        if request.POST.get('sma-last-name') != '':
            sma_last_name = request.POST.get('sma-last-name')
        else:
            sma_last_name = None
        if request.POST.get('sma-email') != '':
            sma_email = request.POST.get('sma-email')
        else:
            sma_email = None
        if request.POST.get('sma-phone') != '':
            sma_phone = request.POST.get('sma-phone')
        else:
            sma_phone = None
        if request.POST.get('sma-username') != '':
            sma_username = request.POST.get('sma-username')
        else:
            sma_username = None
        if request.POST.get('sma-dob') != '':
            sma_dob = datetime.datetime.strptime(request.POST.get('sma-dob'), '%m/%d/%Y')
        else:
            sma_dob = None
        sma_gender = request.POST.get('sma-gender')

        try:
            avatar_obj = Avatar_AMS.get_object_by_id(avatar_id)
            avatar_obj.add_social_accounts(
                sma_platform,
                sma_first_name,
                sma_last_name,
                sma_email,
                sma_phone,
                sma_username,
                sma_dob,
                sma_gender)

            return JsonResponse({'success':200})
        except Exception as e:
            print(e)
            return JsonResponse({'error':str(e)})

class Add_Social_Post(View):
    def post(self, request, *args, **kwargs):
        avatar_id = request.POST.get('smp-avatar')
        if request.POST.get('smp-text') != '':
            post = request.POST.get('smp-text')
        social_media_type = request.POST.get('smp-platform')
        if request.POST.get('smp-date') != '':
            post_date = datetime.datetime.strptime(request.POST.get('smp-date'), '%m/%d/%Y')
        else:
            post_date = None
        try:
            avatar_obj = Avatar_AMS.get_object_by_id(avatar_id)
            avatar_obj.add_social_post(social_media_type, post, post_date)
            return JsonResponse({'success': 200})
        except Exception as e:
            print(e)
            return JsonResponse({'error':str(e)})

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

class Schedule_Action(View):

    def get(self, request, *args, **kwargs):

        # action_type = ACTION_TYPE
        # account_types_supported = None
        action_type=kwargs['action_type']
        avatar_id=kwargs['avatar_id']
        avatar=Avatar_AMS.get_object_by_id(avatar_id)
        return render(request,'Avatar_Management_Unit/scheduled_action.html',{'action_type':action_type,'avatar':avatar})

    def post(self, request,*args,**kwargs):
        # now avatar will come from archive page via parameters so no need static avatar
        # avatar_id = ObjectId("5e7b350f9eda802eb3e6b7fd")
        try:
            avatar_id=kwargs['avatar_id']
            action_type=kwargs['action_type']
            if(action_type =='post'):
                print("## ACTION TYPE POST ##")
                a = Avatar_AMS.get_object_by_id(avatar_id)
                account_type = request.POST.get('account-platform-type')
                title = request.POST.get('title')
                # description = request.POST.get('action-description')
                account_credentials = Avatar_AMS.get_social_account(a, account_type)
                type = action_type  
                text = request.POST.get('post-text')
                social_media = account_credentials.social_media_type
                username = account_credentials.username               
                password=account_credentials.password
                perform_on=request.POST.get('perform-on')
                data = {'text':text,'social_media':social_media,'username':username,'password':password}
                act_s = Action_Schedule_AMS(title=title,description=''  ,account_credentials=account_credentials,data=data,type=type,perform_on=perform_on)
                act_s.save()
                # imitiate object locally 
                # takes three params (usernam,password,social_meida)
                aa = Avatar_Action(username,password,social_media)
                # now send appropiate message
                aa.post(text,image='');

                print("+++++++success +++++++++++")
                return redirect('/amu/archive')
           
            elif(action_type == 'comment'):
                print("## ACTION TYPE COMMENT ##")
                a = Avatar_AMS.get_object_by_id(avatar_id)
              
                account_credentials = Avatar_AMS.get_social_account(a, account_type)
                type = action_type  
                text = request.POST.get('comment-text')
                post_url =request.POST.get('target-post-url')
                social_media = account_credentials.social_media_type
                username = account_credentials.username               
                password=account_credentials.password
              
                perform_on=request.POST.get('perform-on')
                data = {'text':text,'target_post':post_url,'social_media':social_media,'username':username,'password':password}
                act_s = Action_Schedule_AMS(account_credentials=account_credentials,data=data,type=type,perform_on=perform_on)
                act_s.save()
                 # imitiate object locally 
                # takes three params (usernam,password,social_meida)
                aa = Avatar_Action(username,password,social_media)
                # now send appropiate message
                aa.comment(text,post_url)
                return redirect('/amu/archive')
            
            
            
            elif(action_type == 'message'):
                print("## ACTION TYPE MESSAGE ##")
                a = Avatar_AMS.get_object_by_id(avatar_id)
                account_type = request.POST.get('account-platform-type')
                title = request.POST.get('title')
                description = request.POST.get('action-description')
                account_credentials = Avatar_AMS.get_social_account(a, account_type)
                type = action_type  
                text = request.POST.get('message-text')
                target_username=request.POST.get('target-username')
                social_media = account_credentials.social_media_type
                username = account_credentials.username               
                password=account_credentials.password
                perform_on=request.POST.get('perform-on')
                data = {'social_media':social_media,'target_username':target_username,'messgae':text,'username':username,'password':password}
                act_s = Action_Schedule_AMS(title=title,description=description,account_credentials=account_credentials,data=data,type=type,perform_on=perform_on)
                act_s.save()
                 # imitiate object locally 
                # takes three params (usernam,password,social_meida)
                aa = Avatar_Action(username,password,social_media)
                # now send appropiate message
                aa.message(target_username,text)
                return redirect('/amu/archive')
            
            
            elif(action_type == 'reaction'):
                print("## ACTION TYPE REACT ##")
                a = Avatar_AMS.get_object_by_id(avatar_id)
                account_type = request.POST.get('account-platform-type')
                
                account_credentials = Avatar_AMS.get_social_account(a, account_type)
                type = action_type  
                reaction =request.POST.get('reaction-type')
                post_url =request.POST.get('target-post-url')
                social_media = account_credentials.social_media_type
                username = account_credentials.username               
                password=account_credentials.password
                perform_on=request.POST.get('perform-on')
                data = {'reaction':reaction,'target_post':post_url,'social_media':social_media,'username':username,'password':password}
                act_s = Action_Schedule_AMS(account_credentials=account_credentials,data=data,type=type,perform_on=perform_on)
                act_s.save()
                 # imitiate object locally 
                # takes three params (usernam,password,social_meida)
                aa = Avatar_Action(username,password,social_media)
                # now send appropiate message
                aa.react(reaction,post_url)
                return redirect('/amu/archive')
            
            
            
            
            elif(action_type == 'share'):
                print("## ACTION TYPE SHARE ##")
                a = Avatar_AMS.get_object_by_id(avatar_id)
               
                description = ''
                account_credentials = Avatar_AMS.get_social_account(a, account_type)
                type = action_type  
                text = request.POST.get('post-text')
                post_url =request.POST.get('target-post-url')
                social_media = account_credentials.social_media_type
                username = account_credentials.username               
                password=account_credentials.password
                perform_on=request.POST.get('perform-on')
                data = {'text':text,'target_post':post_url,'social_media':social_media,'username':username,'password':password}

                act_s = Action_Schedule_AMS(account_credentials=account_credentials,data=data,type=type,perform_on=perform_on)
                act_s.save()
                 # imitiate object locally 
                # takes three params (usernam,password,social_meida)
                aa = Avatar_Action(username,password,social_media)
                # now send appropiate message
                aa.share(text,post_url)
                print("+++++++success +++++++++++")
                return redirect('/amu/archive')
            
            
            
                
        except Exception as e:
            print(e)
            return HttpResponse(e)
class Actions_Archive(View):

    def get(self,request):

        active_actions = Action_Schedule_AMS.get_all_active_actions()
        expired_actions = Action_Schedule_AMS.get_all_expired_actions()

        actions = Action_Schedule_AMS.get_all_actions()

        return None

class Action_Send_Message(View):

    def get(self,request,*args,**kwargs):

        target_username = None

        if('target_username' in kwargs):
            target_username = kwargs['target_username']
       
        print(target_username)
        return render(request,'Avatar_Management_Unit/send_message.html',{'target_username':target_username})

    def post(self,request):
        print(request.POST)

        target_username = request.POST.get('username',None)
        message = request.POST.get('message')
        aa.message(target_username,message)


        return HttpResponseRedirect(reverse('Avatar_Management_Unit:send_message'))
# by ahmed 
class Amu_Send_Message(View):
    
    def get(self,request,*args,**kwargs):

        avatar_id = None

        if('avatar_id' in kwargs):
            avatar_id = kwargs['avatar_id']
        avatar_obj = Avatar_AMS.get_object_by_id(avatar_id)
        print(avatar_id)
        return render(request,'Avatar_Management_Unit/send_message.html',{'avatar':avatar_obj})

    def post(self,request):
        print(request.POST)
        # this request.POST.get('user') will return email has AMU object has no username 
        # however if amu_object has social media accounts they have user names 
        target_username = request.POST.get('username',None)
        message = request.POST.get('message')
        aa.message(target_username,message)
        messages.success(request, 'Message Sent successfully  ')
        return redirect('/amu/archive')
        # return HttpResponseRedirect(reverse('Avatar_Management_Unit:send_message'))
class Archive(View):
    def get (self,request,*args,**kwargs):
        resp = Avatar_AMS.get_all_avatars()
        return render(request,'Avatar_Management_Unit/archive.html',{'resp':resp})
    