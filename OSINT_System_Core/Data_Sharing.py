import datetime
import sys
# Create your models here.
from mongoengine import *

from Portfolio_Management_System.models import *
from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.mongo_models import *
from Keybase_Management_System.models import *
from mongoengine import signals
disconnect('default')
#connect('OSINT_System')
#client = connect(db='OSINT_System',host='192.168.18.20', port=27017)



class Mongo_Lookup(object):

    """
    this class is to perform operations which are normally not supported by mongoengine packege

    """
    client = None

    def __init__(self):
        cli = connect(db='OSINT_System', host=MONGO_DB_IP, port=27017)
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


class Data_Share(object):

    """
    alpha is reference of class which is going to be linked/matched/included
    beta is reference of a resource which is going to be linked with alpha and have a path or reference
    gamma is reference of class where the link is going to be placed

    e.g

    km = Keybase_Match()
    from bson import ObjectId
    mat = Keybase_Match.create(ObjectId("5e5f527d4ee0e3808c8fc95d"),[ObjectId("5e60aa86259b006699179317"),'posts',2,'associated_links',0])





    """

    ml = Mongo_Lookup()

    alpha_class_ref = None
    gamma_class_ref = None


    def __init__(self,alpha_class_reff,gamma_class_reff):
        self.alpha_class_ref = alpha_class_reff
        self.gamma_class_ref = gamma_class_reff


    def __repr__(self):
        pass

    def create(self,alpha_object_id,beta_path_list):
        """
                this function takes id of keybase which is matched to the intell and intell_paths first occurrence
                should must be object_id and later can be keys or list indexs

                it returns the object created
                :param keybase_id:
                :param intell_path_tuple:
                :return:

                """

        # index 0 is always refer to the intell object id

        try:
            alpha_object = self.get_object_by_id(alpha_object_id)
            beta_object = self.find_object_by_id(beta_path_list[0])
            del (beta_path_list[0])
            if (self.resolve_intell_reference(beta_object, beta_path_list) is not None):
                if(not self.gamma_class_ref.objects(Q(alpha_reference=alpha_object) & Q(beta_reference=beta_object) & Q(beta_path=beta_path_list)).__len__() > 0):

                    print(alpha_object)
                    km = self.gamma_class_ref(alpha_object, beta_object, beta_path_list).save()
                    return km
                else:
                    print('found reference in gama collection')
            else:
                print('given intells path is not correct attachment unsuccessful ')
        except Exception as e:
            print('module : {0} , error : {1}'.format(__name__,e))
            return None

    def find_object_by_id(self,object_id):
        """
        this method takes the object_id and check from all the collections in db and find the object of this
        object_id

        :param object_id:
        :return:
        """
        try:
            return self.ml.find_object_by_id(object_id)

        except Exception as e:
            print(e)
            return None

    def get_object_by_id(self,object_id):
        return self.alpha_class_ref.objects(id=object_id).first()

    def resolve_intell_reference(self,beta_reference,beta_path,step_before=0):

        """
        this method is used to actually get the value of the intell reference placed in the collection
        :param km_object:
        :param step_before:
        :return:

        """

        try:

            km_json = beta_reference.to_mongo()
            path_list = beta_path
            #print(len(path_list)-step_before)

            for i in range(0,len(path_list)-step_before):
                km_json = km_json[path_list[i]]

            return km_json
        except Exception as e:
          print(e)
          return None

class Keybase_Match(object):

    alpha_class_ref = Keybase_KMS
    gamma_class_ref = Keybase_Matched_KMS
    ds = Data_Share(alpha_class_ref,gamma_class_ref)

    @staticmethod
    def create(alpha_object_id, beta_path_list):

        try:

            return Keybase_Match.ds.create(alpha_object_id,beta_path_list)

        except Exception as e:
            print(e)
            return None

class Keybase_Include(object):

    """
    just create a class same like this to create a new attatching resouce and update following tow fields

    alpha_class_ref and gamma_class_ref
    """

    alpha_class_ref = Keybase_KMS
    gamma_class_ref = Keybase_Included_KMS
    ds = Data_Share(alpha_class_ref,gamma_class_ref)

    @staticmethod
    def create(alpha_object_id, beta_path_list):

        try:

            return Keybase_Include.ds.create(alpha_object_id,beta_path_list)

        except Exception as e:
            print(e)
            return None

#extende below class to create support for case and portfolios


class Portfolio_Include(object):
    """
        just create a class same like this to create a new attatching resouce and update following tow fields

        alpha_class_ref and gamma_class_ref
        """

    alpha_class_ref = Portfolio_PMS
    gamma_class_ref = Portfolio_Included_PMS
    ds = Data_Share(alpha_class_ref, gamma_class_ref)

    @staticmethod
    def create(alpha_object_id, beta_path_list):

        try:

            return Portfolio_Include.ds.create(alpha_object_id, beta_path_list)

        except Exception as e:
            print('module : {0} , error : {1}'.format(__name__,e))
            return None

class Portfolio_Link(object):
    """
            just create a class same like this to create a new attatching resouce and update following tow fields

            alpha_class_ref and gamma_class_ref
            """

    alpha_class_ref = Portfolio_PMS
    gamma_class_ref = Portfolio_Linked_PMS
    ds = Data_Share(alpha_class_ref, gamma_class_ref)

    @staticmethod
    def create(alpha_object_id, beta_path_list):

        try:

            return Portfolio_Link.ds.create(alpha_object_id, beta_path_list)

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def resolve_intell_refference(beta_ref,beta_path):
        return Portfolio_Link.ds.resolve_intell_reference(beta_reference=beta_ref,beta_path=beta_path)

class Case_Include(object):
    pass

class Case_Link(object):
    pass
