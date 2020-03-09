from django.shortcuts import render
from django.views import View
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse,HttpResponseRedirect


# Create your views here.

km = Keybase_Manager()


class Create_Keybase(View):

    def get(self,request):
        pass

    def post(self,request):

        #provide the following keward arguments to create a keybase
        km.create_keybase(login_user_id='',title='',topic='',phrases=[],keywords=[],mentions=[],hashtags=[])

        return None

class Delete_Keybase(View):

    def get(self, request,*args,**kwargs):

        #can delete keybase in bulk or using single id

        #for single keybase
        km.delete_keybase(kwargs['keybase_id'])

        #for multiple keybases
        #km.delete_keybase_in_bulk(keybase_id_list=[])

        return HttpResponseRedirect()

class Edit_Keybase(View):

    def get(self, request, *args, **kwargs):
        keybase = km.get_keybase_object_by_id(kwargs['keybase_id'])
        return HttpResponseRedirect()

    def post(self,request,*args,**kwargs):

        #to update a keybase provide the object_id as first positional argument and then pass the updated values as keyword arguments

        km.create_keybase(kwargs['keybase_id'],title='new title',keywords=[])

        return None

class Keybase_Archive(View):


    def get(self,request,**kwargs):
        if('start_date' in kwargs and 'end_date' in kwargs):
            objects = km.get_keybases_by_date_range(kwargs['start_date'],kwargs['end_date'])
        else:
            objects = km.get_all_keybases()

        return objects


class View_Keybase(View):

    def get(self, request, **kwargs):

        keybase = km.get_keybase_object_by_id(kwargs['keybase_id'])

        return objects
