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
from Case_Management_System.models import PersonOfInterest, Language
from Case_Management_System.constants import LANGUAGES
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager

APP_NAME = 'Case_Management_System'

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

class CreateCase(View):
    """
    case creation view
    """

    def get(self, request, *args, **kwargs):
        """
        renders the Case Creation
        and its sub tabs
        """
        cases = json.loads(CaseCMS.get_all_cases_id_and_title().to_json())
        loi = json.loads(LocationOfInterest.get_all_locations().to_json())
        pictures = json.loads(PictureEvidenceFile.get_all_pictures().to_json())
        videos = json.loads(VideoEvidenceFile.get_all_videos().to_json())
        pois = json.loads(PersonOfInterest.get_all_poi().to_json())

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
        # store all person of interest
        ctx['pois'] = []
        for poi in pois:
            ctx['pois'].append([
                poi['_id']['$oid'],
                f'{poi["first_name"]} {poi["last_name"]}'
            ])
        # store all languages to context
        ctx['languages'] = LANGUAGES
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
        case = request.POST.get('pe-case')
        if request.POST.get('pe-name'):
            object_name = request.POST.get('pe-name')
        else:
            object_name = None
        if request.POST.get('pe-description'):
            object_description = request.POST.get('pe-description')
        else:
            object_description = None
        if request.POST.get('pe-storage-location'):
            object_storage_location = request.POST.get('pe-storage-location')
        else:
            object_storage_location = None
        try:
            if request.POST.get('pe-collecton-dt'):
                object_collecton_dt = datetime.strptime(request.POST.get('pe-collecton-dt').strip(), '%m/%d/%Y %H:%M:%S')
            else:
                object_collecton_dt = None
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        if request.POST.get('pe-extraction-location'):
            object_collecton_location = LocationOfInterest.get_location_by_id(request.POST.get('pe-extraction-location'))
        else:
            object_collecton_location = None
        if request.POST.get('pe-pictures'):
            object_pictures = [PictureEvidenceFile.get_picture_by_id(picture_id) for picture_id in request.POST.getlist('pe-pictures')]
        else:
            object_pictures = None
        if request.POST.get('pe-videos'):
            object_videos = [VideoEvidenceFile.get_video_by_id(video_id) for video_id in request.POST.getlist('pe-videos')]
        else:
            object_videos = None
        try:
            physical_evidence = PhysicalEvidence()
            physical_evidence.create_physical_evidence(
                object_name,
                object_description,
                object_storage_location,
                object_collecton_dt,
                object_collecton_location,
                object_pictures,
                object_videos)
            case_cms = CaseCMS.get_object_by_id(case)
            case_cms.store_physical_evidence(physical_evidence)
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success': 200})

class StoreAndRetrievePersonOfInterest(View):
    """
    Stores and Presents a view of People of Interest
    """
    def post(self, request, *args, **kwargs):
        """
        receives data from frontend
        """
        print(request.POST)
        if request.POST.get('poi-case'):
            case = request.POST.get('poi-case')
        else:
            case = None
        if request.POST.get('poi-first-name'):
            first_name = request.POST.get('poi-first-name')
        else:
            first_name = None
        if request.POST.get('poi-middle-name'):
            middle_name = request.POST.get('poi-middle-name')
        else:
            middle_name = None
        if request.POST.get('poi-last-name'):
            last_name = request.POST.get('poi-last-name')
        else:
            last_name = None
        if request.POST.get('poi-phone'):
            phone = request.POST.get('poi-phone')
        else:
            phone = None
        if request.POST.get('poi-email'):
            email = request.POST.get('poi-email')
        else:
            email = None
        if request.POST.getlist('poi-category'):
            category = request.POST.getlist('poi-category')
        else:
            category = None
        if request.POST.get('poi-gender'):
            gender = request.POST.get('poi-gender')
        else:
            gender = None
        try:
            if case:
                person_of_interest = PersonOfInterest()
                person_of_interest.create_poi(
                    first_name, middle_name, last_name, gender, email, phone, category)
                case_cms = CaseCMS.get_object_by_id(case)
                case_cms.store_person_of_interest(person_of_interest)
            else:
                person_of_interest = PersonOfInterest()
                person_of_interest.create_poi(
                    first_name, middle_name, last_name, gender, email, phone, category)
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success': 200})

class AddLanguagesToPOI(View):
    """
    store an embedded language object
    to person of interest
    """
    def post(self, request, *args, **kwargs):
        """
        handles data received from frontend
        """
        print(request.POST)
        if request.POST.get('ls-poi'):
            poi = request.POST.get('ls-poi')
        else:
            poi = None
        if not poi:
            return JsonResponse({'error': 'select person of interest'})
        if request.POST.get('ls-language-name'):
            language_name = request.POST.get('ls-language-name')
        else:
            language_name = None
        if request.POST.get('ls-accent'):
            accent = request.POST.get('ls-accent')
        else:
            accent = None
        if request.POST.get('ls-can-read'):
            can_read = request.POST.get('ls-can-read')
        else:
            can_read = None
        if request.POST.get('ls-can-write'):
            can_write = request.POST.get('ls-can-write')
        else:
            can_write = None
        if request.POST.get('ls-can-speak'):
            can_speak = request.POST.get('ls-can-speak')
        else:
            can_speak = None
        if request.POST.get('ls-fluency'):
            fluency = request.POST.get('ls-fluency')
        else:
            fluency = None
        try:
            language = Language(
                language_name,
                accent,
                can_read,
                can_write,
                can_speak,
                fluency)
            person_of_interest = PersonOfInterest.get_poi_by_id(poi)
            person_of_interest.append_language(language)
        except Exception as exc:
            return JsonResponse({'error': str(exc)})
        return JsonResponse({'success': 200})
