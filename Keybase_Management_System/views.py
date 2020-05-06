import json

from django.shortcuts import render
from django.views import View
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse

from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO

# Create your views here.

km = Keybase_Manager()


class Create_Keybase(RequireLoginMixin, View):

    def get(self,request, *args, **kwargs):
        return render(request, 'Keybase_Management_System/creation.html')

    def post(self,request, *args, **kwargs):
        # input_data = request.POST.dict()
        print(request.POST)
        # print(request.POST.getlist('mentions[]'))
        # for item in request.POST.lists():
        #     print(item)
        # print(input_data)
        #provide the following keward arguments to create a keybase
        print(f'keybase creation request received against user : {request.user.id}')
        resp = km.create_keybase(
            login_user_id=str(request.user.id),
            title=request.POST.get('title'),
            topic=request.POST.get('topic'),
            keywords=request.POST.getlist('keywords[]'),
            mentions=request.POST.getlist('mentions[]'),
            hashtags=request.POST.getlist('tags[]'),
            phrases=request.POST.getlist('phrases[]')
            )
        # print(resp)
        # print(type(resp))
        return JsonResponse({'success':200})

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
        document_id = request.GET.get('docId')
        # print(document_id)
        keybase = km.get_keybase_object_by_id(document_id)
        # print(keybase)
        ctx = json.loads(keybase.to_json())
        print(ctx)
        return render(request, 'Keybase_Management_System/creation.html', {'ctx':ctx})

    def post(self, request, *args, **kwargs):

        #to update a keybase provide the object_id as first positional argument and then pass the updated values as keyword arguments
        document_id = request.GET.get('docId')
        resp = km.update_keybase(
            document_id,
            title=request.POST.get('title'),
            topic=request.POST.get('topic'),
            keywords=request.POST.getlist('keywords[]'),
            mentions=request.POST.getlist('mentions[]'),
            hashtags=request.POST.getlist('tags[]'),
            phrases=request.POST.getlist('phrases[]')
        )

        return JsonResponse({'success':200})

class Keybase_Archive(RequireLoginMixin, View):


    def get(self, request, *args, **kwargs):
        if ('start_date' in kwargs and 'end_date' in kwargs):
            objects = km.get_keybases_by_date_range(kwargs['start_date'],kwargs['end_date'])
        else:
            objects = km.get_all_keybases_by_user(str(request.user.id))
        # print(type(objects))
        # print(objects)
        # print(type(objects[0]))
        # print(objects[0])
        objects = [json.loads(obj.to_json()) for obj in objects]
        # print(type(objects[0]))
        # print(objects[0])
        objects1 = {}
        # objects = {}
        # print(objects[0]['_id'])
        objects1['titles'] = [{obj['_id']['$oid']:[obj['title'], ]} for obj in objects if obj.get('title', False)]
        objects1['topics'] = [{obj['_id']['$oid']:[obj['topic'], ]} for obj in objects if obj.get('title', False)]
        objects1['keywords'] = [{obj['_id']['$oid']:obj['keywords']} for obj in objects if obj.get('keywords', False)]
        objects1['tags'] = [{obj['_id']['$oid']:obj['hashtags']} for obj in objects if obj.get('hashtags', False)]
        objects1['mentions'] = [{obj['_id']['$oid']:obj['mentions']} for obj in objects if obj.get('mentions', False)]
        objects1['phrases'] = [{obj['_id']['$oid']:obj['phrases']} for obj in objects if obj.get('phrases', False)]
        
        print(objects1)
        return render(request, 'Keybase_Management_System/archive.html', {'ctx': objects1})


class View_Keybase(View):

    def get(self, request, **kwargs):

        keybase = km.get_keybase_object_by_id(kwargs['keybase_id'])

        return objects


class DeleteKeybaseProperty(RequireLoginMixin, IsTSO, View):
    """
    deletes a property of keybase
    """

    def post(self, request, *args, **kwargs):
        """
        post handler
        """
        doc_id = request.POST.get('docId')
        prop_to_delete = request.POST.get('propToDelete')
        if prop_to_delete == 'titles':
            resp = km.update_keybase(doc_id, title=None)
        elif prop_to_delete == 'topics':
            resp = km.update_keybase(doc_id, topic=None)
        elif prop_to_delete == 'keywords':
            resp = km.update_keybase(doc_id, keywords=None)
        elif prop_to_delete == 'mentions':
            resp = km.update_keybase(doc_id, mentions=None)
        elif prop_to_delete == 'tags':
            resp = km.update_keybase(doc_id, hashtags=None)
        elif prop_to_delete == 'phrases':
            resp = km.update_keybase(doc_id, phrases=None)
        return JsonResponse({'success':200})