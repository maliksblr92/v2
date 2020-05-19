"""
django views
"""
import json
from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from Case_Management_System.models import CaseCMS, VideoEvidenceFile
from Case_Management_System.models import LocationOfInterest, PhysicalEvidence
from Case_Management_System.models import CaseFile, PictureEvidenceFile

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
    """
    case creation view
    """

    def get(self, request, *args, **kwargs):
        """
        renders the Case Creation Form
        """
        cases = json.loads(CaseCMS.get_all_cases_id_and_title().to_json())
        loi = json.loads(LocationOfInterest.get_all_locations().to_json())
        pictures = json.loads(PictureEvidenceFile.get_all_pictures().to_json())
        videos = json.loads(VideoEvidenceFile.get_all_videos().to_json())

        ctx = {}
        # store all cases to context
        ctx['cases'] = []
        for case in cases:
            ctx['cases'].append([
                case['_id']['$oid'],
                case['case_number'] + ' | ' + case['case_title']
            ])
        # store all locations to context
        ctx['loi'] = []
        for location in loi:
            ctx['loi'].append([
                location['_id']['$oid'],
                location['address']
            ])
        # store all pictures to context
        ctx['pictures'] = []
        for pic in pictures:
            ctx['pictures'].append([
                pic['_id']['$oid'],
                pic['name'] + ' | ' + pic['picture_description']
            ])
        # store all videos to context
        ctx['videos'] = []
        for vid in videos:
            ctx['videos'].append([
                vid['_id']['$oid'],
                vid['name'] + ' | ' + vid['video_description']
            ])
        print(ctx)
        return render(request, f'{APP_NAME}/case_create.html', ctx)

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

class StoreAndRetrieveLocation(View):
    """md
    stores location data and retrieves it
    """
    def get(self, request, *args, **kwargs):
        """
        get request
        """
        pass

    def post(self, request, *args, **kwargs):
        """
        post request
        """
        print(request.POST)
        if request.POST.get('ld-case') != '':
            case_doc_id = request.POST.get('ld-case')
        else:
            case_doc_id = None
        if request.POST.get('ld-coordinates'):
            location = request.POST.get('ld-coordinates')
            location = [float(x) for x in location.strip().split()]
            print(location)
        else:
            location = None
        if request.POST.get('ld-address'):
            address = request.POST.get('ld-address')
        else:
            address = None
        if request.POST.get('ld-description'):
            description = request.POST.get('ld-description')
        else:
            description = None
        try:
            # store location data to global collection and associate with case
            if case_doc_id:
                case_cms = CaseCMS().get_object_by_id(case_doc_id)
                case_cms.store_location(location, address, description)
            else:
                # store location data only to globat location collection
                location_of_interest = LocationOfInterest(location, address, description)
                location_of_interest.save()
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success':200})

class StoreAndRetrieveVirtualEvidence(View):
    """
    handles storing of documents, pictures
    and videos
    """
    def post(self, request, *args, **kwargs):
        """
        receives data from frontend
        """
        print(request.POST)
        category = request.POST.get('ve-category')
        case = request.POST.get('ve-case')
        if request.POST.get('ve-name'):
            name = request.POST.get('ve-name')
        else:
            name = None
        if request.POST.get('ve-location'):
            server_location = request.POST.get('ve-location')
        else:
            server_location = None
        if request.POST.get('ve-description'):
            description = request.POST.get('ve-description')
        else:
            description = None
        if request.POST.get('ve-source'):
            source = request.POST.get('ve-source')
        else:
            source = None
        try:
            case_cms = CaseCMS.get_object_by_id(case)
            if category == 'document':
                case_file = CaseFile(name, server_location, description, source)
                case_file.save()
                case_cms.store_case_file(case_file)
            elif category == 'picture':
                picture = PictureEvidenceFile(name, server_location, description, source)
                picture.save()
                case_cms.store_picture(picture)
            elif category == 'video':
                video = VideoEvidenceFile(name, server_location, description, source)
                video.save()
                case_cms.store_video(video)
            else:
                return JsonResponse({'error': 'unknown category of virtual evidence'})
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success': 200})

class StoreAndRetrievePhysicalEvidence(View):
    """
    handles storing of physical evidence
    objects
    """
    def post(self, request, *args, **kwargs):
        """
        receives data from frontend
        """
        print(request.POST)
        return JsonResponse({'success': 200})