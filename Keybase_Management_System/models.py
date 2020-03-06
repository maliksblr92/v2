from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
# Create your models here.
from django.conf import settings

import datetime
import sys
# Create your models here.
from mongoengine import *


from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.mongo_models import *

from mongoengine import signals
#connect('OSINT_System')
client = connect(db='OSINT_System',host='192.168.18.20', port=27017)

class Mongo_Lookup(object):

    """
    this class is to perform operations which are normally not supported by mongoengine packege

    """
    client = None

    def __init__(self):
        cli = connect(db='OSINT_System', host='192.168.18.20', port=27017)
        self.client = cli['OSINT_System']
    def __repr__(self):
        return self.client.name

    def find_object_by_id(self,object_id):
        """
        this method will query the given id in all the collection currently exist in mongodb and return the
        object of that id or return None if match not found
        :param object_id:
        :return:
        """

        collection_names = self.client.collection_names()
        for collection in collection_names:


            #res = self.client.get_collection(collection).find({'_id': object_id})
            try:
                model_name = self.parse_collection_name_to_model_name(collection)
                model_class_ref = self.str_to_class(model_name)
                res = model_class_ref.objects(id=object_id)

                if (res.count() > 0):
                    return res[0]

            except Exception as e:
                print(e)

        return None

    def str_to_class(self,class_name):
        return getattr(sys.modules[__name__], class_name)

    def parse_collection_name_to_model_name(self,collection_name):

        stru = collection_name.split('_')
        new_stru = []

        for w in stru:
            t = w.capitalize()
            if(len(t)>1):
                t = t+'_'

            new_stru.append(t)

        return (''.join(new_stru)).strip('_')


class Keybase_KMS(Document):

    """
    this class contains the keyword base created by login_user

    """

    login_user_id = StringField(default='no user')
    title = StringField(default='')
    topic = StringField(default='')

    keywords = ListField()
    mentions = ListField()
    phrases = ListField()

    #matched_references = DynamicField()
    #linked_references = DynamicField()
    #include_references = DynamicField()

    is_expired = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    created_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())
    expire_on = DateTimeField(default=datetime.datetime.utcnow()+ datetime.timedelta(days=30))

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def create(self,login_user_id,title,topic,phrases,keywords,mentions,hashtags,kwargs):
        if 'is_expired' in kwargs: self.is_expired = kwargs['is_expired']
        if 'is_enabled' in kwargs: self.is_enabled = kwargs['is_enabled']
        if 'created_on' in kwargs: self.created_on = kwargs['created_on']
        if 'expire_on' in kwargs: self.expire_on = kwargs['expire_on']
        if 'updated_on' in kwargs: self.updated_on = kwargs['updated_on']

        self.login_user_id = login_user_id
        self.title = title
        self.topic = topic
        self.phrases = phrases
        self.keywords = keywords
        self.mentions = mentions
        self.hashtags = hashtags

        self.save()



class Keybase_Include_KMS(Document):
    """
    this model is to keep record that which portfolio or case has used or included
    this keybase document,

    """

    keybase = ReferenceField(Keybase_KMS)
    archive_reference = DynamicField()
    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.keybase.title+' reference type'+str(type(self.archive_reference))

    def __repr__(self):
        return self.keybase.title+' reference type'+str(type(self.archive_reference))


class Keybase_Matched_KMS(Document):
    """
    this model is to keep record of all the osint-intell matched with this keybase document

    """
    keybase = ReferenceField(Keybase_KMS)
    intell_reference = DynamicField()
    intell_path = ListField()
    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.keybase.title+' matched '+str(self.intell_reference)

    def __repr__(self):
        return self.keybase.title+' matched '+str(self.intell_reference)
