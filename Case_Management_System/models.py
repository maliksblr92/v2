"""
contains all models for Case Management System
"""
from datetime import datetime

from mongoengine import disconnect, connect, Document
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import PointField, StringField, URLField
from mongoengine import BooleanField, EmailField
from mongoengine import ReferenceField, ListField, DateTimeField

from Case_Management_System.constants import LANGUAGES, GENDERS
from Case_Management_System.constants import SPOKEN_LANGUAGE_FLUENCY
from Case_Management_System.constants import CASE_STATES, POI_CATEGORY

from Portfolio_Management_System.models import Portfolio_PMS
# Create your models here.

disconnect('default')
connect(db='OSINT_System')

class LocationOfInterest(Document):
    """
    MongoEngine Document that contains the specifics of each location
    pertinent to a case. There will be multiple of these locations.
    Notes and important details of each location will be stored in
    `description`
    """
    location = PointField()
    address = StringField()
    description = StringField()

    @staticmethod
    def get_all_locations():
        """
        return all locations
        """
        return LocationOfInterest.objects().fields(address=1)

    @staticmethod
    def get_location_by_id(location_id):
        """
        return a location
        """
        return LocationOfInterest.objects(id=location_id).first()

class Investigator(Document):
    """
    Embedded Doc that contains details of each investigator
    associated with the case
    """
    first_name = StringField()
    last_name = StringField()
    employee_id = StringField() # unique police officer id
    cell_phone = StringField()
    email = EmailField()

class CaseFile(Document):
    """
    Embedded Doc that contains details of each file
    associated with the case
    """
    name = StringField(required=True)
    document_location = URLField()
    document_description = StringField()
    source = StringField()

class PictureEvidenceFile(Document):
    """
    details of pictures associated with the case
    """
    name = StringField(required=True)
    picture_location = URLField()
    picture_description = StringField()
    source = StringField()

    @staticmethod
    def get_all_pictures():
        return PictureEvidenceFile.objects().fields(name=1, picture_description=1)

    @staticmethod
    def get_picture_by_id(picture_id):
        """
        return a specific picture
        """
        return PictureEvidenceFile.objects(id=picture_id).first()

class VideoEvidenceFile(Document):
    """
    Embedded Doc that contains details of each video
    associated with the case, such as short description
    of what is contained in the video, its server location,
    source of the video
    """
    name = StringField(required=True)
    video_location = URLField()
    video_description = StringField()
    source = StringField()

    @staticmethod
    def get_all_videos():
        return VideoEvidenceFile.objects().fields(name=1, video_description=1)

    @staticmethod
    def get_video_by_id(video_id):
        """
        return a reference to specific video
        """
        return VideoEvidenceFile.objects(id=video_id).first()

class PhysicalEvidence(Document):
    """
    Characteristics of physical evidence obtained by police
    from the crime scene as well other sources
    """
    object_name = StringField()
    object_description = StringField()
    object_storage_location = StringField()
    datetime_of_evidence_collection = DateTimeField()
    object_collection_location = ReferenceField(LocationOfInterest)
    object_pictures = ListField(ReferenceField(PictureEvidenceFile))
    object_videos = ListField(ReferenceField(VideoEvidenceFile))

    def create_physical_evidence(self, object_name, object_description, object_storage_location,
                                 datetime_of_evidence_collection, object_collection_location,
                                 object_pictures, object_videos):
        """
        creates a physical evidence object
        """
        self.object_name = object_name
        self.object_description = object_description
        self.object_storage_location = object_storage_location
        self.datetime_of_evidence_collection = datetime_of_evidence_collection
        self.object_collection_location = object_collection_location
        self.object_pictures.extend(object_pictures)
        self.object_videos.extend(object_videos)
        self.save()

class Language(EmbeddedDocument):
    """
    Embedded Doc that contains details of a language
    spoken, read, and written by a person of interest.
    """
    name = StringField(required=True, choices=LANGUAGES)
    accent = StringField()
    can_read = BooleanField()
    can_write = BooleanField()
    can_speak = BooleanField()
    speaking_fluency = StringField(choices=SPOKEN_LANGUAGE_FLUENCY)

class PersonOfInterest(Document):
    """
    Embedded Doc that contains details of a person of interest.
    """
    first_name = StringField(required=True)
    middle_name = StringField()
    last_name = StringField(required=True)
    gender = StringField(required=True, choices=GENDERS)
    email = EmailField()
    phone = StringField()
    languages = EmbeddedDocumentListField(Language)
    portfolio = ReferenceField(Portfolio_PMS)
    poi_category = ListField(StringField(choices=POI_CATEGORY))

    def create_poi(self, first_name, middle_name, last_name, gender, email, phone, poi_category):
        """
        custom create function
        """
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.phone = phone
        self.poi_category.extend(poi_category)
        self.save()

    def append_language(self, language: Language):
        """
        append language to list of languages
        """
        self.languages.append(language)
        self.save()

    @staticmethod
    def get_all_poi():
        """
        return all person of interest
        """
        return PersonOfInterest.objects().fields(first_name=1, last_name=1)

    @staticmethod
    def get_poi_by_id(poi_id):
        """
        return a reference to a specific poi
        """
        return PersonOfInterest.objects(id=poi_id).first()

class CaseCMS(Document):
    """
    central model class which will contain further
    small and compound documents as Embedded Document
    """
    # unique case number assigned to the case
    case_number = StringField()
    case_title = StringField()
    # Case Creation Date and Time
    case_creation_datetime = DateTimeField(default=datetime.utcnow)
    # Incident Date and Time
    incident_datetime = DateTimeField()
    # case type, there are many types for which
    # domain knowledge is required, therefore
    # we make it a text field for now
    case_type = StringField()
    # state of the case i.e. pending, under_investigation,
    #  closed_resolved, closed_unresolved
    case_state = StringField(required=True, choices=CASE_STATES)
    investigators = ListField(ReferenceField(Investigator))
    # references portfolios of people from PMS
    people_of_interest = ListField(ReferenceField(PersonOfInterest))
    locations_of_interest = ListField(ReferenceField(LocationOfInterest))
    # police case files, server location (url)
    case_files = ListField(ReferenceField(CaseFile))
    pictures = ListField(ReferenceField(PictureEvidenceFile))
    videos = ListField(ReferenceField(VideoEvidenceFile))
    physical_evidence = ListField(ReferenceField(PhysicalEvidence))

    def create_case(self, case_number, case_title, incident_datetime, case_type, case_state):
        """
        creates a case
        """
        self.case_number = case_number
        self.case_title = case_title
        self.incident_datetime = incident_datetime
        self.case_type = case_type
        self.case_state = case_state
        self.save()

    def store_location(self, location, address, description):
        """
        store location to global location collection
        and store a reference to it in the Case Object
        """
        location_of_interest = LocationOfInterest(location, address, description)
        location_of_interest.save()
        self.locations_of_interest.append(location_of_interest)
        self.save()

    def store_case_file(self, case_file: CaseFile):
        """
        stores a reference to case document
        """
        self.case_files.append(case_file)
        self.save()
    
    def store_picture(self, picture: PictureEvidenceFile):
        """
        stores a reference to picture
        """
        self.pictures.append(picture)
        self.save()

    def store_video(self, video: VideoEvidenceFile):
        """
        stores a reference to video
        """
        self.videos.append(video)
        self.save()

    def store_physical_evidence(self, physical_evidence: PhysicalEvidence):
        """
        stores a reference to physical evidence
        """
        self.physical_evidence.append(physical_evidence)
        self.save()

    def store_person_of_interest(self, poi: PersonOfInterest):
        """
        store a reference to person of interest
        """
        self.people_of_interest.append(poi)
        self.save()

    def store_investigator(self, investigator: Investigator):
        """
        Stores a reference to an investigator
        """
        self.investigators.append(investigator)
        self.save()

    @staticmethod
    def get_all_cases_id_and_title():
        """
        get all cases for select menu
        """
        return CaseCMS.objects().fields(case_number=1, case_title=1)

    @staticmethod
    def get_object_by_id(document_id):
        """
        get a CaseCMS object by its document id
        """
        return CaseCMS.objects(id=document_id).first()
