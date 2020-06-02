from django.http import JsonResponse
from django.shortcuts import render
import json
#from dashboard.models import Order
from Public_Data_Acquisition_Unit.mongo_models import *
from Data_Processing_Unit.models import *
from Bi_Tools.mongo_serializer import Mongo_Serializer
from Bi_Tools.visualizations import Visualisation_Mangager
from Bi_Tools.response_visualizations import *


from bokeh.resources import CDN
from bokeh.layouts import row
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components

from django.core import serializers

from bson import ObjectId

ms = Mongo_Serializer()
vm = Visualisation_Mangager()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def dashboard_with_pivot(request):
    return render(request, 'Bi_Tools/dashboard_with_pivot.html', {})


def pivot_data(request):

    objects_list = Keybase_Response_TMS.objects()
    print(objects_list)

    #data = [{'Title':'Awais','Value':50},{'Title':'Nouman','Value':67}] #JSONEncoder().encode(supported_sites[0].to_mongo()) #serializers.serialize('json', supported_sites)

    data = [{"model": "business_intelligence_tool.order", "pk": 1, "fields": {"product_category": "Books", "payment_method": "Credit Card", "shipping_cost": "59", "unit_price": "39.00"}},
            {"model": "business_intelligence_tool.order", "pk": 2, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "88", "unit_price": "200.00"}},
            {"model": "business_intelligence_tool.order", "pk": 3, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "75", "unit_price": "259.00"}},
            {"model": "business_intelligence_tool.production", "pk": 1, "fields": {"product_category": "Table", "production_method": "Automatic", "cost": "88","price": "259.00"}}
            ]
    data = ms.keybase_responce_tms_serializer(objects_list)

    data = json.dumps(data)

    return JsonResponse(data, safe=False)



def simple_chart(request):

    script,div = vm.simple_chart()
    print('...............visual sent ..................')
    return render(request, "Bi_Tools/simple_chart.html", {"the_script": script, "the_div": div})

def keybase_visualization(request):


    a_script,a_div = Keybase_Response_TMS_visualization.content_categorization_piechart()
    b_script, b_div = Keybase_Response_TMS_visualization.keywords_results()
    c_script, c_div = Keybase_Response_TMS_visualization.keywords_status_chart()
    d_script, d_div = Keybase_Response_TMS_visualization.no_of_keywords()

    #show(row(s1,s2,s3))
    return render(request,'Bi_Tools/keybase_visualization.html',{"a_script": a_script, "a_div": a_div,
                                                                 "b_script": b_script, "b_div": b_div,
                                                                 "c_script": c_script,"c_div": c_div,
                                                                 "d_script": d_script,"d_div": d_div,
                                                                 })
