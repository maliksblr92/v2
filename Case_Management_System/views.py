from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,reverse
import json

# Create your views here.
n_series_data = []

data = {
    "quiz": {
        "sport": {
            "q1": {
                "question": "Which one is correct team name in NBA?",
                "options": [
                    "New York Bulls",
                    "Los Angeles Kings",
                    "Golden State Warriros",
                    "Huston Rocket"
                ],
                "answer": "Huston Rocket"
            }
        },

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
                node = {'name':k,'value':size,'children':[{'name':v,'value':size-1}]}
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






