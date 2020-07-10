
import datetime
#connect this class to the avatar ess apis to perform these actions
from Public_Data_Acquisition_Unit.ess_api_controller import Ess_Api_Controller
from Avatar_Management_Unit.models import Action_Schedule_AMS
from OSINT_System_Core.publisher import publish

ess = Ess_Api_Controller()



class Avatar_Action(object):

    username = None
    password = None
    social_media = None

    def __init__(self,username,password,social_media='facebook'):
        self.username = username
        self.password = password
        self.social_media = social_media


    def post(self,text,image=''):
        resp = ess.action_post(text,self.social_media,self.username,self.password)
        if (resp is not None):
            publish('message sent successfully', message_type='notification')
            return True
        else:
            publish('message send failed', message_type='notification')
            return False

    def comment(self,text,target_post_url):
        resp = ess.action_comment(text,target_post_url,self.social_media,self.username,self.password)
        if (resp is not None):
            publish('message sent successfully', message_type='notification')
            return True
        else:
            publish('message send failed', message_type='notification')
            return False

    def react(self,reaction,target_post_url):
        resp = ess.action_reaction(reaction,target_post_url,self.social_media,self.username,self.password)
        if (resp is not None):
            publish('message sent successfully', message_type='notification')
            return True
        else:
            publish('message send failed', message_type='notification')
            return False

    def share(self,text,target_post_url):
        resp = ess.action_share(text,target_post_url,self.social_media,self.username,self.password)
        if (resp is not None):
            publish('message sent successfully', message_type='notification')
            return True
        else:
            publish('message send failed', message_type='notification')
            return False

    def message(self,target_username,message):
        resp = ess.action_send_message(self.social_media,target_username,message,self.username,self.password)
        if(resp is not None):
            publish('message sent successfully',message_type='notification')
            return True
        else:
            publish('message send failed', message_type='notification')
            return False


#beta class for perforing or processing the actions instaed of into the task

class Perform_Action(object):

    av_action = None

    def __init__(self):
        pass

    # expire the action depending upon the response from the server ESS

    def action_polling(self):
        actions = Action_Schedule_AMS.get_all_active_actions()
        for action in actions:
            if(datetime.datetime.utcnow() > action.perform_on ):
                self.av_action = Avatar_Action(action.account_credentials.username,
                                               action.account_credentials.password,
                                               action.account_credentials.social_media_type

                                               )
                if (action.type == 'post'):
                    if(self.av_action.post(action.data['text'])):
                        action.expire_me()
                elif (action.type == 'comment'):
                    if(self.av_action.comment(action.data['text'],action.data['target_post'])):
                        action.expire_me()
                elif (action.type == 'reaction'):
                    if(self.av_action.react(action.data['reaction'],action.data['target_post'])):
                        action.expire_me()
                elif (action.type == 'share'):
                    if(self.av_action.share(action.data['text'],action.data['target_post'])):
                        action.expire_me()
                else:
                    print('un defined action')
                publish('scheduled action {0} submitted to successfully ', message_type='notification')
            else:
                print('not the time ')

