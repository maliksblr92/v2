from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from bson import ObjectId
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse, HttpResponseRedirect
from OSINT_System_Core.Data_Sharing import Portfolio_Link, Portfolio_Include
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from Portfolio_Management_System.models import *

acq = Acquistion_Manager()
# ahmed imports
from django.views.generic import TemplateView

class Create_Portfolio(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request):
        pf = Portfolio_PMS()
        resp = pf.create('name', 'individual', religion='islam', sect='any')
        if(resp is not None):
            return HttpResponse('success')
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
        # return the form here
        # pass the extratype with the form to let user choose from
        pass

    def post(self, request):
        portfolio_id = ObjectId("5e6b3352b6d5b24ef35a01b7")  # id from request
        extra_type = 'social_target'
        prime_value = acq.get_gtr_by_id(ObjectId("5e9d781b6725fb528fdf35f4"))  # value to append to the list

        obj = Portfolio_PMS.get_object_by_id(portfolio_id)
        if extra_type == 'address':
            obj.add_address(prime_value)
        if extra_type == 'social_target':
            obj.add_social_target(prime_value)


        if extra_type == 'portfolio':
            obj.add_portfolios(prime_value)
        if extra_type == 'description':
            obj.add_description(prime_value)


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



class Archive(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_archive.html',{})
    def post(self, request, *args, **kwargs):

        return render(request, 'Portfolio_Management_System/tso_archive.html',{})






class Overview(TemplateView):
    def get(self, request, *args, **kwargs):
         return render(request, 'Portfolio_Management_System/tso_overview.html',{})
    def post(self, request, *args, **kwargs):

        return render(request, 'Portfolio_Management_System/tso_overview.html',{})
