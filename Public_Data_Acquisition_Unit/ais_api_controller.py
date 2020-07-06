import requests
import logging
from django.conf import settings

AIS_IP = settings.AIS_IP

AIS_API_TOKEN = ''  #api token here
AIS_SERVER_PORT = '5000'
AIS_SERVER_USER = 'rapics'
AIS_SERVER_PASSWORD = 'rapics'
#AIS_SERVER_BASE_URL = 'http://192.168.18.13:5000/' #ip of the serve or its url
AIS_SERVER_BASE_URL = 'http://{0}:{1}/'.format(AIS_IP,AIS_SERVER_PORT) #ip of the serve or its url
Header = ''

logger = logging.getLogger(__name__)

class Ais_Api_Controller(object):

    def __init__(self):
        self.ess = None
        try :
            if(self.ais_connect()):
                pass
                #self.ess_add_instagram_target(target_category='post')
                #self.ess_add_instagram_search_target('islamabad')
        except Exception as e:
            print(e)
            logger.error('.......................................failed to connect to AIS..........................')

    def ais_connect(self):
        login_url = 'login'
        response = requests.post(AIS_SERVER_BASE_URL+login_url, data={},json = {'username':AIS_SERVER_USER,'password':AIS_SERVER_PASSWORD})
        if(response.status_code == 200):
            global AIS_API_TOKEN
            global Header
            AIS_API_TOKEN = response.content.decode('utf-8').split(':')[1].replace('"','').replace('}','').replace("\n",'')
            print(AIS_API_TOKEN)
            Header = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(AIS_API_TOKEN)}
            #logger.info('.............................connected to AIS server sucessfully ......................')
            print('.............................connected to AIS server sucessfully ......................')
            return True
        return False

    def ais_login(self):
        pass

    def ais_logout(self):
        pass

    def ais_is_accessable(self):
        pass

    def ais_is_conneted(self):
        pass

    def text_analytics(self,input_text,operation='common_words'):
        try:
            add_target_url = 'text_analytics'
            payload = {'text':input_text,'task':operation}
            response = requests.post(AIS_SERVER_BASE_URL+add_target_url,headers=Header,json=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ais replied null'}