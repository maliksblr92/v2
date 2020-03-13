from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from bson import ObjectId
from OSINT_System_Core.publisher import publish
from Keybase_Management_System.keybase_manager import Keybase_Manager
from django.http import HttpResponse,HttpResponseRedirect

from Portfolio_Management_System.models import *

class Create_Portfolio(View):

    def get(self,request,*args,**kwargs):
        pass

    def post(self,request):
        pf = Portfolio_PMS()
        resp = pf.create('name','individual',religion='islam',sect='any')
        if(resp is not None):
            return HttpResponse('success')
        else:
            publish('unable to create a portfolio', module_name=__name__, message_type='alert')
            return HttpResponse('problem')


class Delete_Portfolio(View):

    def get(self,request,*args,**kwargs):
        portfolio_id = kwargs['p_id']

        if(Portfolio_PMS.delete_portfolio(portfolio_id)):
            return HttpResponse('sucess')
        else:
            publish(str(e), module_name=__name__, message_type='alert')
            return HttpResponse('unsucessfull')

class Edit_Portfolio(View):

    def get(self,request,*args,**kwargs):
        pass

    def post(self,request):
        pass

class Add_Extras(View):
    """
    add extra includes add address,add social target, add description, add portfolio
    """
    extra_type = ['address','social_target','portfolio','description']

    def get(self,request,*args,**kwargs):
        #return the form here
        # pass the extratype with the form to let user choose from
        pass

    def post(self,request):
        portfolio_id = ObjectId("5e6b3352b6d5b24ef35a01b7") # id from request
        extra_type = 'address'
        prime_value = 'any value from form' # value to append to the list

        obj = Portfolio_PMS.get_object_by_id(portfolio_id)
        if extra_type == 'address': obj.add_address(prime_value)
        if extra_type == 'social_target': obj.add_social_target(prime_value)
        if extra_type == 'portfolio': obj.add_portfolios(prime_value)
        if extra_type == 'description': obj.add_description(prime_value)






