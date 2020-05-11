"""
contains all models for Case Management System
"""
from mongoengine import disconnect, connect, Document
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import PointField, StringField, URLField
from mongoengine import BooleanField, EmailField

from Case_Management_System.languages import LANGUAGES
# Create your models here.

disconnect('default')
connect(db='OSINT_System')

GENDERS = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('transgender', 'Transgender'),
    ('other', 'Other')
)

SPOKEN_FLUENCY = (
    ('beginner', 'Beginner'),
    ('elementary', 'Elementary'),
    ('intermediate', 'Intermediate'),
    ('upper intermediate', 'Upper Intermediate'),
    ('advanced', 'Advanced'),
    ('proficient', 'Proficient')
)

class Investigator(EmbeddedDocument):
    first_name = StringField()
    last_name = StringField()
    cell_phone = StringField()
    email = EmailField()

class CaseFile(EmbeddedDocument):
    """
    Embedded Doc that contains details of each file
    associated with the case
    """
    name = StringField(required=True)
    file_location = URLField()
    description = StringField()


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
    speaking_fluency = StringField(choices=SPOKEN_FLUENCY)

class PersonOfInterest(EmbeddedDocument):
    """
    Embedded Doc that contains details of a person of interest.
    """
    first_name = StringField(required=True)
    middle_name = StringField()
    last_name = StringField(required=True)
    gender = StringField(required=True, choices=GENDERS)
    languages = EmbeddedDocumentListField(Language)

class LocationOfInterest(EmbeddedDocument):
    """
    Embedded Doc that contains the specifics of each location
    pertinent to a case. There will be multiple of these locations.
    Notes and important details of each location will be stored in
    **`description`**
    """
    location = PointField()
    address = StringField()
    description = StringField()

class CaseCMS(Document):
    """
    central model class which will contain further
    small and compound documents as Embedded Document
    """
    # unique case number assigned to the case
    case_number = StringField()
    investigators = EmbeddedDocumentListField(Investigator)
    # police case files, server location (url)
    case_files_location = URLField()
    people_of_interest = EmbeddedDocumentListField(PersonOfInterest)
    locations_of_interest = EmbeddedDocumentListField(LocationOfInterest)

