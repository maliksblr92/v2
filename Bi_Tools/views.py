from django.http import JsonResponse
from django.shortcuts import render
import json
#from dashboard.models import Order
from Public_Data_Acquisition_Unit.mongo_models import *

from django.core import serializers

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def dashboard_with_pivot(request):
    return render(request, 'Bi_Tools/dashboard_with_pivot.html', {})


def pivot_data(request):

    supported_sites = Supported_Website.objects()
    print(supported_sites)

    #data = [{'Title':'Awais','Value':50},{'Title':'Nouman','Value':67}] #JSONEncoder().encode(supported_sites[0].to_mongo()) #serializers.serialize('json', supported_sites)

    data = [{"model": "business_intelligence_tool.order", "pk": 1, "fields": {"product_category": "Books", "payment_method": "Credit Card", "shipping_cost": "59", "unit_price": "39.00"}},
            {"model": "business_intelligence_tool.order", "pk": 2, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "88", "unit_price": "200.00"}},
            {"model": "business_intelligence_tool.order", "pk": 3, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "75", "unit_price": "259.00"}},
            {"model": "business_intelligence_tool.production", "pk": 1, "fields": {"product_category": "Table", "production_method": "Automatic", "cost": "88","price": "259.00"}}
            ]
    data = json.dumps(data)

    return JsonResponse(data, safe=False)