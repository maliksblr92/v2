from Keybase_Management_System.models import *

class Keybase_Manager(object):

    ml = Mongo_Lookup()

    """
    This class is a Keybase application handler used to access applications models and apply logic


    """



    def __init__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass



    #user defined methods bellow

    def create_keybase(self,login_user_id,title,topic,phrases,keywords,mentions,hashtags,**kwargs):
        try:

            kb = Keybase_KMS()
            kb.create(login_user_id,title,topic,phrases,keywords,mentions,hashtags,kwargs)
            return kb

        except Exception as e:
            print(e)


    def add_keybase_match(self,keybase_id,intell_path_list):
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

            intell_reff = self.find_object_by_id(intell_path_list[0])
            del(intell_path_list[0])
            kb = self.get_keybase_object_by_id(keybase_id)
            km = Keybase_Matched_KMS(kb,intell_reff,intell_path_list).save()
            return km
        except Exception as e:
            print(e)
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

    def resolve_intell_refference(self,km_object,step_before=0):

        """
        this method is used to actually get the value of the intell reference placed in the collection
        :param km_object:
        :param step_before:
        :return:

        """

        try:

            km_json = km_object.intell_reference.to_mongo()
            path_list = km_object.intell_path
            #print(len(path_list)-step_before)

            for i in range(0,len(path_list)-step_before):
                km_json = km_json[path_list[i]]

            return km_json
        except Exception as e:
          print(e)
          return None

    def get_matched_intell_all(self):
        objects = Keybase_Matched_KMS.objects()
        return objects

    def get_matched_intell_by_date(self):
        pass

    def get_matched_intell_by_intell_type(self):
        pass

    def delete_keybase(self,keybase_id):
        pass

    def get_keybase_object_by_id(self,keybase_id):
        return Keybase_KMS.objects(id=keybase_id)[0]

    def get_all_keybases(self):
        pass


