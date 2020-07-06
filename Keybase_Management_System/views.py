import json

from django.shortcuts import render,reverse
from django.views import View
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from Public_Data_Acquisition_Unit.mongo_models import Blocked_Urls
from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO

# Create your views here.

km = Keybase_Manager()

# ahmed import 
from Data_Processing_Unit.models import Keybase_Response_TMS
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
acq=Acquistion_Manager()
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
            keywords=list(filter(lambda x:len(x)>0,request.POST.getlist('keywords[]'))),
            mentions=list(filter(lambda x:len(x)>0,request.POST.getlist('mentions[]'))),
            hashtags=list(filter(lambda x:len(x)>0,request.POST.getlist('tags[]'))),
            phrases=list(filter(lambda x:len(x)>0,request.POST.getlist('phrases[]')))
            )
        print(resp) 
        print(type(resp))
        return JsonResponse({'success':200})


class Block_URL(View):
    def get(self,request,*args,**kwargs):

        url = ''

        if 'url' in kwargs: url = kwargs['url']

        if(not url == ''):
            url = url.replace(' ','/')



        urls = Blocked_Urls.get_all_blocked_urls()

        return render(request,'Keybase_Management_System/block_url.html',{'urls':urls,'b_url':url})

    def post(self,request,*args,**kwargs):

        print(request.POST)



        title = request.POST.get('title',None)
        description = request.POST.get('description',None)
        url = request.POST.get('url',None)

        print(title,description,url)

        try:
            if(title and description and url):
                obj = Blocked_Urls(title=title,description=description,url=url)
                obj.save()


        except Exception as e:
            print(e)
            publish(str(e),message_type='notification')


        return HttpResponseRedirect(reverse('Keybase_Management_System:block_url'))

class Delete_URL(View):

    def get(self,request,*args,**kwargs):
        url_id = None
        try:
            if 'url_id' in kwargs: url_id = kwargs['url_id']

            obj = Blocked_Urls.get_object_by_id(url_id)
            obj.delete()


        except Exception as e:
            print(e)
            publish(str(e), message_type='notification')

        return HttpResponseRedirect(reverse('Keybase_Management_System:block_url'))

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
        return render(request, 'Keybase_Management_System/archive.html', {'ctx': objects,'gtx':objects1})


class View_Keybase(View):

    def get(self, request, **kwargs):

        keybase = km.get_keybase_object_by_id(kwargs['keybase_id'])

        return ''


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

class Keybase_Fetched_Responses(View):  
    def get(self,request,*args,**kwargs):
        resp=Keybase_Response_TMS.objects.all()
        GTR_id=kwargs['GTR_id']
        resp=acq.get_data_response_object_by_gtr_id(GTR_id)
        target_object=acq.get_dataobject_by_gtr(acq.get_gtr_by_id(GTR_id))
       
     
        # return HttpResponse('<div>asdas</div>')
        return render(request,'Keybase_Management_System/Keybase_Fetched_Responses.html',{'resp':resp,'target_object':target_object})
    
class Keybase_Fetched_Report(View):  
    def get(self,request,*args,**kwargs):
        resp=Keybase_Response_TMS.objects.all()
        GTR_id=kwargs['GTR_id']
        resp=acq.get_data_response_object_by_gtr_id(GTR_id)
        target_object=acq.get_dataobject_by_gtr(acq.get_gtr_by_id(GTR_id))
        print(resp)
        # return HttpResponse('<div>asdas</div>')
        return render(request,'Keybase_Management_System/Keybase_Fetched_Report.html',{'resp':resp,'target_object':target_object})
    def post(self,request,*args,**kwargs):
        pass