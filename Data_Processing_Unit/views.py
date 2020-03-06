from django.shortcuts import render
from bson.objectid import ObjectId
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,reverse

from Data_Processing_Unit import tasks
from django.http import JsonResponse
from Data_Processing_Unit.processing_manager import Processing_Manager
from xhtml2pdf import pisa
# Create your views here.

from io import BytesIO

from django.template.loader import get_template
from django.template import Context

p_manager = Processing_Manager()


class Main(View):
    def get(self,request):
        return HttpResponse('in data processing unit')


class Target_Response(View):
    def get(self,request):
        responses = p_manager.get_all_target_responses()
        return render(request, 'Data_Processing_Unit/target_response.html', {'responses':responses})


class Facebook_Profile_View(View):
    def get(self,request,*args,**kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        profile_obj = p_manager.get_facebook_instance_by_id(ob_id)
        return render(request, 'Data_Processing_Unit/facebook_profile_view.html', {'person':profile_obj})

class Twitter_Profile_View(View):

    def get(self,request,*args,**kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        profile_obj = p_manager.get_twitter_instance_by_id(ob_id)
        return render(request, 'Data_Processing_Unit/twitter_profile_view.html', {'person':profile_obj})

class Instagram_Profile_View(View):
    def get(self,request,*args,**kwargs):

        ob_id = ObjectId(kwargs['m_id'])

        profile_obj = p_manager.get_instagram_instance_by_id(ob_id)
        analysis_obj = p_manager.get_profile_analysis_instance()

        return render(request, 'Data_Processing_Unit/instagram_profile_view.html', {'person':profile_obj,'analysis_instance':analysis_obj})

class Linkedin_Profile_Person_View(View):
    def get(self,request,*args,**kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        try:
            profile_obj = p_manager.get_linkedin_person_instance_by_id(ob_id)
            return render(request, 'Data_Processing_Unit/linkedin_profile_person_view.html', {'person': profile_obj})
        except:
            profile_obj = p_manager.get_linkedin_company_instance_by_id(ob_id)
            return render(request, 'Data_Processing_Unit/linkedin_profile_company_view.html', {'person': profile_obj})



class Linkedin_Profile_Company_View(View):
    def get(self,request):
        return render(request, 'Data_Processing_Unit/linkedin_profile_company_view.html', {})


class BigView(View):
    def get(self,request):
        fetched_by_date = p_manager.article_fetched_count_by_date()
        ess_time_usage = p_manager.ess_usage_average()
        return render(request, 'Data_Processing_Unit/big_view.html', {'fetched_by_category':p_manager.article_fetched_count_by_category(),'fetched_by_date':fetched_by_date,'ess_time_usage':ess_time_usage})

class Link_Analysis(View):
    def get(self,request):
        return render(request, 'Data_Processing_Unit/link_analysis.html', {})



#................................................News Response_Views....................................................

class News_Monitoring(View):

    def get(self, request, *args, **kwargs):
        resp = None
        response = p_manager.get_all_news_instances(['ary','bbc','geo','dawn','abp','ndtv','indiatoday','zee'])
        return render(request, 'Data_Processing_Unit/news_monitoring.html', {'news_response':response})



#................................................Twitter_Trend_Views....................................................
class Twitter_Trends_Country(View):

    def get(self, request, *args, **kwargs):
        print(kwargs['country'])
        resp = tasks.fetch_twitter_trends_country(kwargs['country'])
        return JsonResponse(resp, safe=False)

class Twitter_Trends_Worldwide(View):

    def get(self, request, *args, **kwargs):
        resp = tasks.fetch_twitter_trends_worldwide()
        return JsonResponse(resp, safe=False)


#................................................Reports Management Views....................................................
class Report_Management_View(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'Data_Processing_Unit/reports_management_view.html', {})



class Convert_Html_To_Pdf(View):
    def get(self,request):
        c = Generate_Reports()
        country_trends = tasks.fetch_twitter_trends_country('pakistan')
        world_trends = tasks.fetch_twitter_trends_worldwide()
        news_response = p_manager.get_all_news_instances(['ary', 'bbc','abp','indiatoday'])
        social_responses = p_manager.get_all_target_responses()
        return render(request, 'Data_Processing_Unit/report_template.html', {'country_trends':country_trends,'world_trends':world_trends,'news_response':news_response,'responses':social_responses})
        #c.render_to_pdf()






class Generate_Reports(object):

    def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None