from django.http import JsonResponse
from django.shortcuts import render
import json
#from dashboard.models import Order
from Public_Data_Acquisition_Unit.mongo_models import *
from Data_Processing_Unit.models import *
from Bi_Tools.mongo_serializer import Mongo_Serializer



from bokeh.resources import CDN
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components

from django.core import serializers

from bson import ObjectId

ms = Mongo_Serializer()


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
    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot)

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label="Temp.", line_width=2)

    # show the results
    #show(p)

    return render(request, "Bi_Tools/simple_chart.html", {"the_script": script, "the_div": div})