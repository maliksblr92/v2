from django.shortcuts import render , reverse,redirect
from OSINT_System_Core.mixins import RequireLoginMixin, IsTSO
# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import json
import os
from bson import ObjectId
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse, HttpResponseRedirect
from OSINT_System_Core.Data_Sharing import Portfolio_Link, Portfolio_Include,Visuals,Photo,Video,Data_Share
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from Public_Data_Acquisition_Unit.mongo_models import Timeline_Posts as Timeline_Posts_Model
from Portfolio_Management_System.models import *
from System_Log_Management_Unit.system_log_manager import Data_Queries
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings as djangoSettings
from django.contrib import messages
from django.templatetags.static import static
acq = Acquistion_Manager()
dq = Data_Queries()

# ahmed imports
from django.views.generic import TemplateView
from Portfolio_Management_System.models import Portfolio_PMS
class Create_Portfolio(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'Portfolio_Management_System/tso_create.html',{})

    def post(self, request):

        form_name = request.POST.get('form_name',None)
        print(request.POST)

        name = request.POST.get('portfolio_name',None)
        dob = formate_date(request.POST.get('dob','2020-05-06'))
        gender = request.POST.get('gender',None)
        religion = request.POST.get('relegion',None)
        sect = request.POST.get('sect',None)
        portfolio_type = request.POST.get('portfolio_type')



        pf = Portfolio_PMS()
        resp = pf.create(name,portfolio_type,dob=dob,gender=gender,religion=religion,sect=sect)

        if(resp is not None):
            return HttpResponseRedirect(reverse('Portfolio_Management_System:create_portfolio'))
        else:
            publish(
                'unable to create a portfolio',
                module_name=__name__,
                message_type='alert')
            return HttpResponse('problem')


class Delete_Portfolio(View):

    def get(self, request, *args, **kwargs):
        portfolio_id = kwargs['p_id']

        if(Portfolio_PMS.delete_portfolio(portfolio_id)):
            return HttpResponse('sucess')
        else:
            #publish(str(e), module_name=__name__, message_type='alert')
            return HttpResponse('unsucessfull')


class Edit_Portfolio(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request):
        pass


class Add_Extras(View):
    """
    add extra includes add address,add social target, add description, add portfolio
    """
    extra_type = ['address', 'social_target', 'portfolio', 'description']

    def get(self, request, *args, **kwargs):

        if 'portfolio_id' in kwargs:
            portfolio_id = kwargs['portfolio_id']
            obj = Portfolio_PMS.get_object_by_id(portfolio_id)
            """
            visuals = []
            if(len(obj.visuals) >0):
                for visual in obj.visuals:
                    temp_dict = {'title':visual.title,'description':visual.description,'images':[],'videos':[]}

                    for i,image in enumerate(visual.photos):

                        print(str(os.path.join(djangoSettings.BASE_DIR,"static")+'/mongo_temp_files/img'+str(obj.id)+str(i)))

                        #img = open(str(os.path.join(djangoSettings.BASE_DIR,"static")+'Portfolio_Management_System/mongo_temp_files/img'+str(visual.title.replace(' ','_'))+str(i))+'.jpg','wb')
                        file = image.photo.read()
                        fs = FileSystemStorage()
                        filename = fs.save('img'+str(obj.id)+str(i),file)
                        print(fs.url(filename))

                        #temp_dict['images'].append(str(os.path.join(djangoSettings.BASE_DIR,"static")+'/mongo_temp_files/img'+str(visual.title.replace(' ','_'))+str(i))+'.jpg')

                        #img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(img)
                        #img_tags.append(img_tag)
                    visuals.append(temp_dict)

            print(visuals)
            """
            # return the form here
            # pass the extratype with the form to let user choose from
            return render(request,'Portfolio_Management_System/add_information.html',{'portfolio_id':portfolio_id,'addresses':obj.addresses,'descriptions':obj.description,'phones':obj.phones,'social_targets':obj.social_targets,'visuals':[]})

        return render(request, 'Portfolio_Management_System/add_information.html',{})

    def post(self, request):

        print(request.POST)
        portfolio_id = request.POST.get('portfolio_id',None)  #ObjectId("5e6b3352b6d5b24ef35a01b7")  # id from request
        extra_type = request.POST.get('extra_type',None) #'social_target'
        prime_value = request.POST.get('prime_value',None) #acq.get_gtr_by_id(ObjectId("5e9d781b6725fb528fdf35f4"))  # value to append to the list

        obj = Portfolio_PMS.get_object_by_id(portfolio_id)
        if(obj is not None):
            if extra_type == 'address':
                obj.add_address(prime_value)
            if extra_type == 'social_target':
                obj.add_social_target(prime_value)

            if extra_type == 'phones':
                obj.add_phone(prime_value)


            if extra_type == 'portfolio':
                obj.add_portfolios(prime_value)
            if extra_type == 'description':
                title = request.POST.get('title', None)

                obj.add_description({'title':title,'description':prime_value})

            if(extra_type =='visuals'):
                print(request.FILES)

                title = request.POST.get('title',None)
                description = request.POST.get('description',None)

                visual_obj = Visuals(title=title,description=description)

                image_files = request.FILES.getlist('photos_file_field[]')
                video_files = request.FILES.getlist('videos_file_field[]')

                print(image_files)
                if(len(image_files) > 0):
                    for file in image_files:
                        photo = Photo()

                        photo.photo.put(file,content_type='image/jpeg')
                        visual_obj.photos.append(photo)
                        print('i file saved')

                if (len(video_files) > 0):
                    for file in video_files:
                        video = Video()

                        video.video.put(file, content_type='video/mp4')
                        visual_obj.photos.append(video)
                        print('v file saved')

                obj.add_visual(visual_obj)

        return HttpResponseRedirect(reverse('Portfolio_Management_System:add_information',args=[portfolio_id]))

class Archive(View):

    def get(self, request, *args, **kwargs):

        portfolios = Portfolio_PMS.get_all_portfolios()
        print(portfolios)
        print("+++++++++++++++++++++++")
        return render(request,'Portfolio_Management_System/tso_archive.html',{'portfolios':portfolios})


class Portfolio_Link_Analysis(View):
    def get(self,request,*args,**kwargs):

        object_id = kwargs.get('portfolio_id',None)

        #print(data_object['linked_to'][1])
        #data = convert_facebook_indirect_links_to_graph(link_data)

        if(object_id is not None):

            resp = dq.portfolio_link_analysis(object_id)
            resp=json.loads(resp)
            name=resp['name']
            path=static('/images/anonymous_logo.jpg')
            resp['img']=path+""
            #make sure that we have two nodes to display else it will redirect back to archive page with message 
            if (len(resp['children']) and len(resp['children'][0]['children'])) <= 1 :
                messages.success(request, 'No link analysis found for '+name)
                return redirect('/pms/archive')
            else:
                resp=json.dumps(resp)
                return render(request,'Target_Management_System/link_analysis.html',{'data':resp})
        else:
            return render(request, 'Target_Management_System/link_analysis.html', {})


class Link_Portfolio(View):

    def get(self, request, *args, **kwargs):

        # get these two method , path of resource and portfolio object id

        alpha_obj = ObjectId("5e6b3352b6d5b24ef35a01b7")
        beta_path = [
            ObjectId("5e6b2ab3a071de651c404a7d"),
            'general_information']
        Portfolio_Link.create(ObjectId("5e6b3352b6d5b24ef35a01b7"), beta_path)

class Search_Portfolio(View):
    def get(self,request):

        print(request.GET['query'])
        data = Portfolio_PMS.find_object(request.GET['query'])
        resp = {'resp': list(data)}
        print(resp)

        return JsonResponse(resp, safe=False)
# ahmed class based views
class Create(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_create.html',{})
    def post(self, request, *args, **kwargs):
        form_name=request.POST['form_name']
        if(form_name=='portfolio_create_form'):
            author_id=request.POST['author_id']
            author_name=request.POST['author_name']
            author_url=request.POST['author_url']
            username=request.POST['username']
            options=request.POST['options']
            print('######'+author_id+'########')
            print('######'+author_name+'########')
            print('######'+author_url+'########')
            print('######'+username+'########')
            print('######'+options+'########')
            print(form_name)
        if(form_name=='social_info'):
            author_id=request.POST['author_id']
            author_name=request.POST['author_name']
            author_url=request.POST['author_url']
            username=request.POST['username']
            options=request.POST['options']
            print('######'+author_id+'########')
            print('######'+author_name+'########')
            print('######'+author_url+'########')
            print('######'+username+'########')
            print('######'+options+'########')
            print(form_name)



        if(form_name=='personal_info'):
            author_id=request.POST['author_id']
            author_name=request.POST['author_name']
            author_url=request.POST['author_url']
            username=request.POST['username']
            options=request.POST['options']
            print('######'+author_id+'########')
            print('######'+author_name+'########')
            print('######'+author_url+'########')
            print('######'+username+'########')
            print('######'+options+'########')
            print(form_name)

        if(form_name=='other_info'):
            author_id=request.POST['author_id']
            author_name=request.POST['author_name']
            author_url=request.POST['author_url']
            username=request.POST['username']
            options=request.POST['options']
            print('######'+author_id+'########')
            print('######'+author_name+'########')
            print('######'+author_url+'########')
            print('######'+username+'########')
            print('######'+options+'########')
            print(form_name)
        return render(request, 'Portfolio_Management_System/tso_create.html',{})





class Link(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_link.html',{})
    def post(self, request, *args, **kwargs):

        return render(request, 'Portfolio_Management_System/tso_link.html',{})



class Overview(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_overview.html',{})
    def post(self, request, *args, **kwargs):

        return render(request, 'Portfolio_Management_System/tso_overview.html',{})


def formate_date(date):
    import datetime
    return datetime.datetime.strptime(date, '%Y-%m-%d')




class Overview(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_overview.html',{})
    def post(self, request, *args, **kwargs):

        return render(request, 'Portfolio_Management_System/tso_overview.html',{})


class Explore(View):
    def get(self,request,*args,**kwargs):
        resp=Portfolio_PMS.objects().first()
        print("printitng portfolio pms object")
        return render(request,'Portfolio_Management_System/explore.html',{'resp':resp})


class Explore_By_GTR(View):
    def get(self,request,*args,**kwargs):
        portfolio_id = kwargs['porfolio_id']
        if portfolio_id is not None:
            resp=Portfolio_PMS.objects.get(id=portfolio_id)

        return render(request,'Portfolio_Management_System/explore.html',{'resp':resp})


class Portfolio_Links(RequireLoginMixin, IsTSO, View):

    SUPPORTED_LINK_TYPES = ()

    def get(self,request,*args,**kwargs):

        gtr_list = []
        posts = []
        portfolio_id = None
        #ds = Data_Share()

        if 'portfolio_id' in kwargs:portfolio_id=kwargs['portfolio_id']

        if(portfolio_id is not None):
            portfolio = Portfolio_PMS.get_object_by_id(portfolio_id)
            print(portfolio)
            if(portfolio):
                linked_objs = Portfolio_Linked_PMS.objects(alpha_reference=portfolio)
                if(linked_objs):
                    for obj in linked_objs:
                        try:
                            if(not isinstance(obj.beta_reference,Timeline_Posts_Model)):
                                gtr_list.append(obj.beta_reference.GTR)
                            else:
                                resource = Portfolio_Link.resolve_intell_refference(beta_ref=obj.beta_reference, beta_path=obj.beta_path)
                                if(resource):
                                    posts.append(resource)

                        except :
                            pass

                    resp = acq.get_linked_targets(link_type='portfolio',gtr_list=gtr_list)
                    print(posts)
                    return render(request, 'Portfolio_Management_System/portfolio_links.html',
                                  {'targets': resp, 'supported_sites': acq.get_all_supported_sites(),'posts':posts})


        return render(request,'Portfolio_Management_System/portfolio_links.html',{})
