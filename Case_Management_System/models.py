"""
contains all models for Case Management System
"""
from datetime import datetime

from mongoengine import disconnect, connect, Document
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import PointField, StringField, URLField
from mongoengine import BooleanField, EmailField, EmbeddedDocumentField
from mongoengine import ReferenceField, ListField, DateTimeField

from Case_Management_System.constants import LANGUAGES, GENDERS
from Case_Management_System.constants import SPOKEN_LANGUAGE_FLUENCY
from Case_Management_System.constants import CASE_STATES, POI_CATEGORY

from Portfolio_Management_System.models import Portfolio_PMS
# Create your models here.

disconnect('default')
connect(db='OSINT_System')

class LocationOfInterest(EmbeddedDocument):
    """
    Embedded Doc that contains the specifics of each location
    pertinent to a case. There will be multiple of these locations.
    Notes and important details of each location will be stored in
    `description`
    """
    location = PointField()
    address = StringField()
    description = StringField()

class Investigator(EmbeddedDocument):
    """
    Embedded Doc that contains details of each investigator
    associated with the case
    """
    first_name = StringField()
    last_name = StringField()
    employee_id = StringField() # unique police officer id
    cell_phone = StringField()
    email = EmailField()

class CaseFile(EmbeddedDocument):
    """
    Embedded Doc that contains details of each file
    associated with the case
    """
    name = StringField(required=True)
    document_location = URLField()
    document_description = StringField()
    source = StringField()

class PictureEvidenceFile(EmbeddedDocument):
    """
    details of pictures associated with the case
    """
    name = StringField()
    picture_location = URLField()
    picture_description = StringField()
    source = StringField()

class VideoEvidenceFile(EmbeddedDocument):
    """
    Embedded Doc that contains details of each video
    associated with the case, such as short description
    of what is contained in the video, its server location,
    source of the video
    """
    name = StringField()
    video_location = URLField()
    video_description = StringField()
    source = StringField()

class PhysicalEvidence(EmbeddedDocument):
    """
    Characteristics of physical evidence obtained by police
    from the crime scene as well other sources
    """
    object_name = StringField()
    object_description = StringField()
    object_storage_location = StringField()
    datetime_of_evidence_collection = DateTimeField()
    object_collection_location = EmbeddedDocumentField(LocationOfInterest)
    object_picture = EmbeddedDocumentField(PictureEvidenceFile)

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

class PersonOfInterest(EmbeddedDocument):
    """
    Embedded Doc that contains details of a person of interest.
    """
    first_name = StringField(required=True)
    middle_name = StringField()
    last_name = StringField(required=True)
    gender = StringField(required=True, choices=GENDERS)
    languages = EmbeddedDocumentListField(Language)
    portfolio = ReferenceField(Portfolio_PMS)
    poi_category = ListField(StringField(choices=POI_CATEGORY))

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
    investigators = EmbeddedDocumentListField(Investigator)
    # references portfolios of people from PMS
    people_of_interest = EmbeddedDocumentListField(PersonOfInterest)
    locations_of_interest = EmbeddedDocumentListField(LocationOfInterest)
    # police case files, server location (url)
    case_files = EmbeddedDocumentListField(CaseFile)
    pictures = EmbeddedDocumentListField(PictureEvidenceFile)
    videos = EmbeddedDocumentListField(VideoEvidenceFile)
    physical_evidence = EmbeddedDocumentListField(PhysicalEvidence)

    def create_case(self, case_number, case_title, incident_datetime, case_type, case_state):
        self.case_number = case_number
        self.case_title = case_title
        self.incident_datetime = incident_datetime
        self.case_type = case_type
        self.case_state = case_state
        self.save()
    
    def store_location(self, location, address, description):
        location_of_interest = LocationOfInterest(location, address, description)
        self.locations_of_interest.append(location_of_interest)
        self.save()

    @staticmethod
    def get_all_cases_id_and_title():
        return CaseCMS.objects().fields(case_number=1, case_title=1)

    @staticmethod
    def get_object_by_id(document_id):
        return CaseCMS.objects(id=document_id).first()

class AllLocationsOfInterest(Document):
    """md
    All Locations ever added to the police database
    """
    locations = EmbeddedDocumentListField(LocationOfInterest)

    def store_location(self, location, address, description):
        location_of_interest = LocationOfInterest(location, address, description)
        self.locations.append(location_of_interest)
        self.save()

class AllPeopleOfInterest(Document):
    """md
    All people ever stored in the police database
    """
    people = EmbeddedDocumentListField(PersonOfInterest)
