from Keybase_Management_System.models import *

class Keybase_Manager(object):


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


