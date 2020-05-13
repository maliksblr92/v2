from django.db import models

# Create your models here.
import datetime
import sys
# Create your models here.
from mongoengine import *


from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.mongo_models import *

from mongoengine import signals
#connect('OSINT_System')
client = connect(db='OSINT_System',host='192.168.18.20', port=27017)


PORTFOLIO_TYPES = (
    ('individual', ('One Person')),
    ('group', ('Group of Persons')),
    ('event', ('Event'))
)


class Photo(EmbeddedDocument):
    photo = FileField()


class Video(EmbeddedDocument):
    video = FileField()

class Visuals(EmbeddedDocument):

    title = StringField()
    description = StringField()

    photos = ListField(EmbeddedDocumentField(Photo))
    videos = ListField(EmbeddedDocumentField(Video))




class Portfolio_PMS(Document):

    portfolio_type = StringField(choices=PORTFOLIO_TYPES)
    name = StringField(required=True)
    dob = DateField(null=True)
    religion = StringField(default='')
    sect = StringField(default='')
    gender = StringField()

    addresses = ListField(default=[])
    phones = ListField(default=[])
    education = StringField()

    description = ListField(default=[])
    visuals = ListField(EmbeddedDocumentField(Visuals))

    # if portfolio type is group it should have list of individual portfolios
    portfolios = ListField(default=[])

    #it saves ref of TMS target in list bellow
    social_targets = ListField()



    created_on = DateTimeField(default=datetime.datetime.utcnow())
    updated_on = DateTimeField(default=datetime.datetime.utcnow())


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def create(self,name,p_type,**kwargs):

        try:
            self.name = name
            self.portfolio_type = p_type

            if 'dob' in kwargs: self.dob = kwargs['dob']
            if 'religion' in kwargs: self.religion = kwargs['religion']
            if 'sect' in kwargs: self.sect = kwargs['sect']
            if 'education' in kwargs: self.dob = kwargs['dob']


            self.save()
            return self

        except Exception as e:
            publish(str(e),module_name=__name__,message_type='alert')
            print(e)
            return None

    def add_address(self,address):
        self.addresses.append(address)
        self.save()

    def add_social_target(self,target_ref):
        self.social_targets.append(target_ref)
        self.save()

    def add_portfolios(self,portfolio_ref):
        self.portfolios.append(portfolio_ref)
        self.save()

    def add_description(self,description):
        self.description.append(description)
        self.save()

    def add_phone(self,phone):
        self.phones.append(phone)
        self.save()

    def add_visual(self,visual):
        self.visuals.append(visual)
        self.save()



    @staticmethod
    def get_object_by_id(obj_id):
        return Portfolio_PMS.objects(id=obj_id).first()

    @staticmethod
    def delete_portfolio(obj_id):
        try:
            obj = Portfolio_PMS.get_object_by_id(id=obj_id)
            obj.delete()
            return True
        except Exception as e:
            publish(str(e), module_name=__name__, message_type='alert')
            return False

    meta = {'indexes': [
        {'fields': ['$name', "$description"],
         'default_language': 'english',
         'weights': {'name': 10, 'description': 2}
         }
    ]}

    @staticmethod
    def get_all_portfolios():
        return Portfolio_PMS.objects()

    @staticmethod
    def find_object(query):
        return Portfolio_PMS.objects.search_text(query)

class Portfolio_Included_PMS(Document):
    """
        this model is to keep record that which portfolio or case has used or included
        this keybase document,

        """

    alpha_reference = ReferenceField(Portfolio_PMS, reverse_delete_rule=CASCADE)
    beta_reference = DynamicField()
    beta_path = ListField()

    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.alpha_reference.title + ' reference type' + str(type(self.beta_reference))

    def __repr__(self):
        return self.alpha_reference.title + ' reference type' + str(type(self.beta_reference))

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



class Portfolio_Linked_PMS(Document):
    """
        this model is to keep record that which portfolio or case has used or included
        this keybase document,

        """

    alpha_reference = ReferenceField(Portfolio_PMS, reverse_delete_rule=CASCADE)
    beta_reference = DynamicField()
    beta_path = ListField()

    created_on = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return self.alpha_reference.name + ' reference type' + str(type(self.beta_reference))

    def __repr__(self):
        return self.alpha_reference.name + ' reference type' + str(type(self.beta_reference))

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