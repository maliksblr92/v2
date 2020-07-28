from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import reverse, render, redirect
from django.views import View
from django.conf import settings


# imports for djangorestframework
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


from django.contrib.auth import authenticate

UIS_IP = settings.UIS_IP
# Create your views here.
# ahmed
from User_Accounts_Management_Unit.models import User_Profile,User_Profile_Manager
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.core import serializers
from django.contrib import messages
import json
from django.http import JsonResponse
# ahmed

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def do_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    login(request, user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def do_logout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        print(e)

    return Response('logged out', status=HTTP_200_OK)


class User_Login(View):
    """
    USER Login View
    """

    def get(self, request,*args):
        """
        get handler for login view
        """
        if(request.user.is_authenticated):
            return HttpResponseRedirect(reverse('OSINT_System_Core:tso-dashboard'))


        return render(request, 'User_Accounts_Management_Unit/login.html', {'message':''})

    def post(self, request):
        """
        post handler for login view
        """
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if(username is not None and password is not None):
            user = authenticate(request, username=username, password=password)
            # if user is not authenticated
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                elif request.user.groups.filter(name='tso').exists():
                    return HttpResponseRedirect(
                        reverse('OSINT_System_Core:tso-dashboard'))
                elif request.user.groups.filter(name='tmo').exists():
                    return HttpResponseRedirect(
                        reverse('OSINT_System_Core:tmo-dashboard'))
                elif request.user.groups.filter(name='rdo').exists():
                    return HttpResponseRedirect(
                        reverse('OSINT_System_Core:rdo-dashboard'))
                elif request.user.groups.filter(name='pao').exists():
                    return HttpResponseRedirect(
                        reverse('OSINT_System_Core:pao-dashboard'))
            else:
                error_m = 'Invalid Credentials'
                return render(request, 'User_Accounts_Management_Unit/login.html', {'message':error_m})

        else:
            return HttpResponse('form field might left empty')


class User_Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(
            reverse('User_Accounts_Management_Unit:user_login'))



class Add_User_Profile(View):
    template_name='Add_User.html'
    def get (self,request,*args,**kwargs):
        User_Groups = Group.objects.all()
        User_Profile_Fetched={}
        return render (request,'User_Accounts_Management_Unit/Add_User_Profile.html',{'User_Profile_Fetched':User_Profile_Fetched,'User_Groups':User_Groups})
    def post (self,request,*args,**kwargs):
        first_name=request.POST.get('first-name')
        last_name=request.POST.get('last-name')
        current_address=request.POST.get('local-address')
        permanent_address=request.POST.get('permanent-address')
        profile_pic=request.POST.get('profile-pic')
        # 
        print(first_name);
        print(last_name);
        print(current_address);
        print(permanent_address);
        print(profile_pic);
        # 
        New_User_Profile =User_Profile.objects.create_user_profile(
                first_name=first_name,
                last_name=last_name,
                current_address=current_address,
                permanent_address=permanent_address,
                profile_pic=profile_pic
                
        )
        if New_User_Profile:
            messages.success(request,'User profile created successfully ')
            return redirect('/all_user_profile')
        else:
            return render(request,'User_Accounts_Management_Unit/Add_User_Profile.html')

        
       
class All_User_Profile(View):
    def get(self,request,*args,**kwargs):
        All_User_Profiles=User_Profile.objects.all()
        # print(All_User_Profiles.count())
        return render(request,'User_Accounts_Management_Unit/All_User_Profiles.html',{'All_User_Profiles':All_User_Profiles})
    

class Update_User_Profile(View):
    def get(self,request,*args,**kwargs):
      id= int(kwargs.get('id'))
      User_Profile_Fetched=User_Profile_Manager.getUserProfile(id)
      if(User_Profile_Fetched):
          return render(request,'User_Accounts_Management_Unit/Add_User_Profile.html',{'User_Profile_Fetched':User_Profile_Fetched})
      else:
          return render(request,'User_Accounts_Management_Unit/All_User_Profiles.html')
    
    def post(self,request,*args,**kwargs):
         id= int(kwargs.get('id'))
         first_name=request.POST.get('first-name')
         last_name=request.POST.get('last-name')
         current_address=request.POST.get('local-address')
         permanent_address=request.POST.get('permanent-address')
         profile_pic=request.POST.get('profile-pic')
         User_Profile_Updated=User_Profile_Manager.getUpdateProfile(id,first_name,last_name,current_address,permanent_address,profile_pic)
         if(User_Profile_Updated):
            messages.success(request,'User profile updated successfully ')
            return redirect('/all_user_profile')
         else:
             return render(request,'User_Accounts_Management_Unit/Add_User_Profile.html',{'User_Profile_Fetched':User_Profile_Updated})

class Delete_User_Profile(View):
    def get(self,request,*args,**kwargs):
        id= int(kwargs.get('id'))
        Delete_User_Profile=User_Profile_Manager.deleteUserProfile(id);
        if(Delete_User_Profile):
            messages.success(request,'User profile deleted successfully ')
            return redirect('/all_user_profile')
        else:
            messages.success(request,'Operation failed ! Try again ')
            return redirect('/all_user_profile')
        


class Add_User_Group(View):
    def get(self,request,*args,**kwargs):
        pass
    def post(self,request,*args,**kwargs):
        group_name=request.POST.get('group_name')
        Group_Created=Group.objects.create(name=group_name)
        if Group_Created:
            messages.success(request,'Group created successfully ')
            return redirect('/all_user_group')
        else:
            messages.success(request,'Operation failed ! Try again ')
            return redirect('/all_user_group')
    
class All_User_Group(View):
    def get(self,request,*args,**kwargs):
        All_Users_Groups=Group.objects.all()
        All_Users=User.objects.all()
        if( All_Users_Groups):
            return render(request,'User_Accounts_Management_Unit/All_Users_Groups.html',{'All_Users_Groups':All_Users_Groups,'All_Users':All_Users})
        
class Add_Users_To_Groups(View):
    def get(self,request,*args,**kwargs):
        pass
    def post(self,request,*args,**kwargs):
        exsist=False
        Page_Name=request.POST.get('page_name')
        user_name=request.POST.get('username_AddGroup')
        Get_User=User.objects.get(username=user_name)
        if Get_User:
            groupId=request.POST.get('groupIdForAdd')
            group = Group.objects.get(id=groupId)
            if group:
                exsist=Get_User.groups.filter(name=group).exists() 
                if exsist:
                    messages.error(request,'User already exsist in group')
                    if Page_Name == 'All_Users':
                        return redirect('/all_users')
                    else:
                        return redirect('/all_user_group')                        
                else: 
                    Get_User.groups.add(group)
                    messages.success(request,'User added to group successfully')
                    if Page_Name == 'All_Users':
                        return redirect('/all_users')
                    else:
                        return redirect('/all_user_group')   
        
class Remove_Users_To_Groups(View):
    def get(self,request,*args,**kwargs):
        pass
    def post(self,request,*args,**kwargs):
        exsist=False
        user_name=request.POST.get('username_RemoveGroup')
        Page_Name=request.POST.get('page_name')
        Get_User=User.objects.get(username=user_name)
        if Get_User:
            groupId=request.POST.get('groupIdForRemove')
            group = Group.objects.get(id=groupId)
            if group:
                exsist=Get_User.groups.filter(name=group).exists() 
                if exsist:
                    messages.success(request,'User removed succesfully')
                    Get_User.groups.clear()
                    if Page_Name == 'All_Users':
                        return redirect('/all_users')
                    else:
                        return redirect('/all_user_group') 
                else: 
                    messages.error(request,'Operation Failed ! User doesnot exsist in group ')
                    if Page_Name == 'All_Users':
                        return redirect('/all_users')
                    else:
                        return redirect('/all_user_group') 
                   
        else:
            messages.error(request,'Operation Failed ! User not found ')
            if Page_Name == 'All_Users':
                return redirect('/all_users')
            else:
                return redirect('/all_user_group')   
     

class Get_All_Group_Users(View):
    def get(self,request,*args,**kwargs):
        Group_Id= int(kwargs.get('id'))
        group = Group.objects.get(id=Group_Id)
        # users = group.user_set.all()
        users=User.objects.filter(groups__name=group.name)
        for user in users:
            All_Users=User.objects.exclude(username=user.username)
            qs_json = serializers.serialize('json', All_Users)
        return HttpResponse(qs_json, content_type='application/json')
           

class Add_User(View):
    def get(self,request,*args,**kwargs):
        return render (request,'User_Accounts_Management_Unit/Add_User.html')
    def post(self,request,*args,**kwargs):
        is_active=False
        is_superuser=False
        is_staff=False
        First_Name=request.POST.get('f-name');
        Last_Name=request.POST.get('l-name');
        Password=request.POST.get('password');
        Email=request.POST.get('email')
        User_Name=request.POST.get('user-name')
        if 'is_active' in request.POST:
            is_active=True
        if 'is_superuser' in request.POST:
            is_superuser=True
        if 'is_staff' in request.POST:
             is_staff=True
        print(First_Name,Last_Name,Email,Password,is_staff,is_active,is_superuser)
        New_User = User.objects.create_user(username=User_Name,
                                 email=Email,
                                 password=Password,
                                 is_active=is_active,
                                 is_staff=is_staff,
                                 is_superuser=is_superuser,
                                 first_name=First_Name,
                                 last_name=Last_Name)
        if New_User:
            messages.success(request,'User created successfully ')
            return redirect('/all_users')
        else:
            messages.success(request,'Operation failed ! Try again ')
            return redirect('all_users')
class All_Users(View):
    def get(self,request,*args,**kwargs):
        All_Users=User.objects.all()
        Groups=Group.objects.all()
        return render(request,'User_Accounts_Management_Unit/All_Users.html',{'All_Users':All_Users,'Groups':Groups})

class Update_User(View):
    def get(self,request,*args,**kwargs):
        id= int(kwargs.get('id'))
        Find_User=User.objects.get(id=id)
        if Find_User:
            return render(request,'User_Accounts_Management_Unit/Add_User.html',{'User':Find_User})
        else:
          messages.success(request,'Operation failed ! Try again ')  
          return  redirect('/all_users')
    def post(self,request,*args,**kwargs):    
        is_active=False
        is_superuser=False
        is_staff=False
        # Id=request.POST.get('id');
        id= int(kwargs.get('id'))
        First_Name=request.POST.get('f-name');
        Last_Name=request.POST.get('l-name');
        Password=request.POST.get('password');
        Email=request.POST.get('email')
        User_Name=request.POST.get('user-name')
        if 'is_active' in request.POST:
            is_active=True
        if 'is_superuser' in request.POST:
            is_superuser=True
        if 'is_staff' in request.POST:
             is_staff=True
        print(First_Name,Last_Name,Email,Password,is_staff,is_active,is_superuser)
        Updated_User = User.objects.filter(id=id).update(
        username=User_Name,
        email=Email,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
        first_name=First_Name,
        last_name=Last_Name)
        User.objects.get(id=id).set_password(Password)
        if Updated_User:
            messages.success(request,'User updated successfully ')
            return redirect('/all_users')
        else:
           messages.success(request,'Operation failed ! Try again ')
           return  redirect('/all_users')

class Delete_User(View):
    def get(self,request,*args,**kwargs):
         id= int(kwargs.get('id'))
         Find_User=User.objects.get(id=id)
         if Find_User:
             Deleted=Find_User.delete()
             if Deleted:
                 messages.success(request,"User deleted successfully ")
                 return redirect('/all_users')
             else:
                 messages.error(request,'Operation Failed ! Try again ')
                 return redirect('/all_users')
         else:
              messages.error(request,'Operation Failed ! Try again ')
              return redirect('/all_users')
