"""
django views
"""
import json
from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from Case_Management_System.models import CaseCMS

APP_NAME = 'Case_Management_System'

# Create your views here.
n_series_data = []

data = {
    "quiz": {
        "maths": {
            "q1": {
                "question": "5 + 7 = ?",
                "options": [
                    "10",
                    "11",
                    "12",
                    "13"
                ],
                "answer": "12"
            },
            "q2": {
                "question": "12 - 8 = ?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "answer": "4"
            }
        }
    }
}


data1 = {
    "fruit": "Apple",
    "size": "Large",
    "color": "Red"
}


class Explore_Data(View):
    def get(self,request,*args,**kwargs):

        global n_series_data
        n_series_data = []
        resp = convert_json_to_network_series(data)
        print(resp)
        return render(request,'Case_Management_System/explore_data.html',{'data':resp})



def convert_json_to_network_series(data,n=1):

    f = (n/100) * 100
    size = 5-f
    node = None
    for k,v in data.items():
        if(not isinstance(v,dict)):

            if(not isinstance(v,list)):
                node = {'name':k,'value':size,'children':[{'name':v,'value':size-1}],'collapsed':'true','fixed':'true'}
            else:
                temp_childs = []
                for val in v :
                    child = {'name':val,'value':size-1}
                    temp_childs.append(child)

                node = {'name': k, 'value': size, 'children': temp_childs}

            n_series_data.append(node)

        else:
            node = {'name':k,'value':size-1,'linkWith':list(v.keys())}
            n_series_data.append(node)
            resp = convert_json_to_network_series(v,n+0.5)


    #print(n_series_data)
    return json.dumps(n_series_data)

class CreateCase(View):
    """md
    case creation view
    """
    def get(self, request, *args, **kwargs):
        """md
        renders the Case Creation Form
        """
        return render(request, f'{APP_NAME}/case_create.html')

    def post(self, request, *args, **kwargs):
        """md
        handles the data received from case creation
        and stores it in the database
        """
        print(request.POST)
        case_number = request.POST.get('cc-case-number')
        if request.POST.get('cc-case-title'):
            case_title = request.POST.get('cc-case-title')
        else:
            case_title = None
        if request.POST.get('cc-incident-dt'):
            incident_datetime = datetime.strptime(request.POST.get('cc-incident-dt'), '%m/%d/%Y %H:%M:%S')
        else:
            incident_datetime = None
        if request.POST.get('cc-case-type'):
            case_type = request.POST.get('cc-case-type')
        else:
            case_type = None
        if request.POST.get('cc-case-state'):
            case_state = request.POST.get('cc-case-state')
        else:
            case_state = None

        try:
            case_cms = CaseCMS()
            case_cms.create_case(case_number, case_title, incident_datetime, case_type, case_state)
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success': 200})
