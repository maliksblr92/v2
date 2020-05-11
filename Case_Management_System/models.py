"""
contains all models for Case Management System
"""
from mongoengine import disconnect, connect, Document
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import PointField, StringField, URLField
# Create your models here.

disconnect('default')
connect(db='OSINT_System')


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
    # police case files, server location (url)
    case_files_location = URLField()
    locations_of_interest = EmbeddedDocumentListField(LocationOfInterest)
