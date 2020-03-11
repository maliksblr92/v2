from Keybase_Management_System.models import *
from OSINT_System_Core.publisher import publish


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
            publish('keybase created successfully', message_type='control', module_name=__name__)

            return kb

        except Exception as e:
            publish(str(e),message_type='error',module_name=__name__)


    def update_keybase(self,keybase_id,**kwargs):
        try:
            kb = self.get_keybase_object_by_id(keybase_id)

            if 'login_user_id' in kwargs: kb.login_user_id = kwargs['login_user_id']
            if 'title' in kwargs : kb.title = kwargs['title']
            if 'topic' in kwargs: kb.topic = kwargs['topic']
            if 'phrases' in kwargs: kb.phrases = kwargs['phrases']
            if 'keywords' in kwargs: kb.keywords = kwargs['keywords']
            if 'mentions' in kwargs: kb.mentions = kwargs['mentions']
            if 'hashtags' in kwargs: kb.hashtags = kwargs['hashtags']

            kb.save()
            publish('keybase created successfully', message_type='control', module_name=__name__)

            return kb

        except Exception as e:
            publish(str(e),message_type='error',module_name=__name__)

    def get_matched_intell_all(self):
        objects = Keybase_Matched_KMS.objects()
        return objects

    def get_matched_intell_by_date_range(self,start_datetime,end_datetime):
        return Keybase_Matched_KMS.objects(Q(created_on__gte=start_datetime) & Q(created_on__lte=end_datetime))

    def get_matched_intell_by_intell_type(self):
        pass

    def delete_keybase(self,keybase_id):
        try:
            Keybase_KMS.objects(id=keybase_id)[0].delete()
            publish('keybase deleted successfully',message_type='control',module_name=__name__)
        except Exception as e:
            publish(str(e),message_type='error',module_name=__name__)

    def delete_keybase_in_bulk(self,keybase_id_list):
        try:
            for kb_id in keybase_id_list:
                Keybase_KMS.objects(id=kb_id)[0].delete()

            publish('keybases deleted successfully',message_type='control',module_name=__name__)
        except Exception as e:
            publish(str(e),message_type='error',module_name=__name__)

    def get_keybase_object_by_id(self,keybase_id):
        return Keybase_KMS.objects(id=keybase_id)[0]

    def get_keybases_by_date_range(self,start_datetime,end_datetime):
        return Keybase_KMS.objects(Q(created_on__gte=start_datetime) & Q(created_on__lte=end_datetime))

    def get_all_keybases(self):
        return Keybase_KMS.objects()

    def get_keybase_included_all(self):
        return Keybase_Included_KMS.objects()

    def get_keybase_included_by_date_range(self,start_datetime,end_datetime):
        return Keybase_Included_KMS.objects(Q(created_on__gte=start_datetime) & Q(created_on__lte=end_datetime))
