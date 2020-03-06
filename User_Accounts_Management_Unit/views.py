from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import reverse,render
from django.views import View
from django.conf import settings


#imports for djangorestframework
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

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def do_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    login(request,user)
    return Response({'token': token.key}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def do_logout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        print(e)

    return Response('logged out',status=HTTP_200_OK)



class User_Login(View):
    #function to handle the get request
    def get(self,request):
        return render(request,'User_Accounts_Management_Unit/login.html',{})

    def post(self,request):
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        if(username is not None or password is not None):
            user = authenticate(request, username=username, password=password)
            # if user is not authenticated
            if (user is not None):
                login(request, user)
                return HttpResponseRedirect(reverse('OSINT_System_Core:dashboard'))
            else:
                return HttpResponse('invalid credintial')

        else:
            return HttpResponse('form field might left empty')


class User_Logout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('User_Accounts_Management_Unit:user_login'))


