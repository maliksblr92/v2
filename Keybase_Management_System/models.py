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


class Keybase_Included_KMS(Document):
    """
    this model is to keep record that which portfolio or case has used or included
    this keybase document,

    """

    alpha_reference = ReferenceField(Keybase_KMS)
    beta_reference = DynamicField()
    beta_path = ListField()

    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.alpha_reference.title+' reference type'+str(type(self.beta_reference))

    def __repr__(self):
        return self.alpha_reference.title+' reference type'+str(type(self.beta_reference))


class Keybase_Matched_KMS(Document):
    """
    this model is to keep record of all the osint-intell matched with this keybase document

    """
    alpha_reference = ReferenceField(Keybase_KMS)
    beta_reference = DynamicField()
    beta_path = ListField()
    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.alpha_reference.title+' matched '+str(self.beta_reference)

    def __repr__(self):
        return self.alpha_reference.title+' matched '+str(self.beta_reference)

    def resolve_intell_reference(self,step_before=0):

        """
        this method is used to actually get the value of the intell reference placed in the collection
        :param km_object:
        :param step_before:
        :return:

        """

        try:

            km_json = self.beta_reference.to_mongo()
            path_list = self.beta_path
            #print(len(path_list)-step_before)

            for i in range(0,len(path_list)-step_before):
                km_json = km_json[path_list[i]]

            return km_json
        except Exception as e:
          print(e)
          return None