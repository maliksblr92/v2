from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,reverse
import json
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
acq = Acquistion_Manager()

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
        #data = convert_facebook_indirect_links_to_graph(link_data)

        resp = convert_facebook_indirect_links_to_graph(link_data)
        print(resp)
        return render(request,'Case_Management_System/explore_data.html',{'data':resp})

def convert_facebook_indirect_links_to_graph(data):
    data = data[0]

    n_data = []

    for i,item in enumerate(data):

        print(item)
        if(not username_exists(item['username'],n_data)):
            node = {'name': item['username'],
                    'value': 1,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": acq.get_picture_by_facebook_username(item['username']),
                    }
            linkwith = set()

            for y in data:
                if(item['username']==y['username']):
                    linkwith.add(y['mutual_close_associate'])

            node['linkWith'] = list(linkwith)

            n_data.append(node)

    for i,item in enumerate(data):

        #print(item)
        if(not username_exists(item['mutual_close_associate'],n_data)):
            node = {'name': item['mutual_close_associate'],
                    'value': 0.5,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": acq.get_picture_by_facebook_username(item['mutual_close_associate']),
                    }

            linkwith = set()

            for y in data:
                if(item['mutual_close_associate']==y['mutual_close_associate']):
                    linkwith.add(y['username'])

            node['linkWith'] = list(linkwith)

            n_data.append(node)


    print(n_data)
    return json.dumps(n_data)


def username_exists(username,n_data):
    for item in n_data:
        if(username == item['name']):
            return True

    return False





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

link_data = [
    [
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "5re4",
            "mutual_close_associate" : "waqar.a.khan.125",
            "name" : "Hajra Ata"
        },
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "5re4",
            "mutual_close_associate" : "rz088",
            "name" : "Hajra Ata"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "mishal.zahra.583",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "itsrocketfuel",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "fabia056",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "zubda.shafi",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "rz088",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "ghana.nasir",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "huria.ali.75",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "misbahi2",
            "GTR" : "91ff4t",
            "mutual_close_associate" : "sedlyfaf",
            "name" : "Misbah Iqbal"
        },
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "88ff4t",
            "mutual_close_associate" : "waqar.a.khan.125",
            "name" : "Hajra Ata"
        },
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "88ff4t",
            "mutual_close_associate" : "rz088",
            "name" : "Hajra Ata"
        },
        {
            "entity_type" : "person",
            "username" : "mishal.zahra.583",
            "GTR" : "88ff4dfgt",
            "mutual_close_associate" : "rz088",
            "name" : "Mishal Zahra"
        },
        {
            "entity_type" : "person",
            "username" : "mishal.zahra.583",
            "GTR" : "88ff4dfgt",
            "mutual_close_associate" : "ghana.nasir",
            "name" : "Mishal Zahra"
        },
        {
            "entity_type" : "person",
            "username" : "mishal.zahra.583",
            "GTR" : "88ff4dfgt",
            "mutual_close_associate" : "itsrocketfuel",
            "name" : "Mishal Zahra"
        },
        {
            "entity_type" : "person",
            "username" : "mishal.zahra.583",
            "GTR" : "88ff4dfgt",
            "mutual_close_associate" : "fabia056",
            "name" : "Mishal Zahra"
        },
        {
            "entity_type" : "person",
            "username" : "mishal.zahra.583",
            "GTR" : "88ff4dfgt",
            "mutual_close_associate" : "zubda.shafi",
            "name" : "Mishal Zahra"
        },
        {
            "entity_type" : "person",
            "username" : "fabia056",
            "GTR" : "34fsddhjdf",
            "mutual_close_associate" : "mishal.zahra.583",
            "name" : "Fabia Nazar"
        },
        {
            "entity_type" : "person",
            "username" : "fabia056",
            "GTR" : "34fsddhjdf",
            "mutual_close_associate" : "rz088",
            "name" : "Fabia Nazar"
        },
        {
            "entity_type" : "person",
            "username" : "fabia056",
            "GTR" : "34fsddhjdf",
            "mutual_close_associate" : "sedlyfaf",
            "name" : "Fabia Nazar"
        },
        {
            "entity_type" : "person",
            "username" : "fabia056",
            "GTR" : "34fsddhjdf",
            "mutual_close_associate" : "itsrocketfuel",
            "name" : "Fabia Nazar"
        },
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "91fd",
            "mutual_close_associate" : "waqar.a.khan.125",
            "name" : "Hajra Ata"
        },
        {
            "entity_type" : "person",
            "username" : "hajra.ata",
            "GTR" : "91fd",
            "mutual_close_associate" : "rz088",
            "name" : "Hajra Ata"
        }
    ]
]







