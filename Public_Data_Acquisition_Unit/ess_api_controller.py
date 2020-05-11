import requests
import logging
from django.conf import settings

#ESS_IP = settings.ESS_IP
ESS_SERVER_BASE_URL = 'http://192.168.18.19:8000/' #ip of the serve or its url
ESS_API_TOKEN = ''  #api token here
ESS_SERVER_PORT = '8000'
ESS_SERVER_USER = 'rapidev'
ESS_SERVER_PASSWORD = 'rapidev'

Header = ''

logger = logging.getLogger(__name__)

class Ess_Api_Controller(object):

    def __init__(self):
        self.ess = None
        try :
            if(self.ess_connect()):
                pass
                #self.ess_add_instagram_target(target_category='post')
                #self.ess_add_instagram_search_target('islamabad')
        except Exception as e:
            logger.error('.......................................failed to connect to ESS..........................')

    def ess_connect(self):
        login_url = 'login/'
        response = requests.post(ESS_SERVER_BASE_URL+login_url, data = {'username':ESS_SERVER_USER,'password':ESS_SERVER_PASSWORD})
        if(response.status_code == 200):
            global ESS_API_TOKEN
            global Header
            ESS_API_TOKEN = response.content.decode('utf-8').split(':')[1].strip('"}')
            Header = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Token {0}'.format(ESS_API_TOKEN)}
            #logger.info('.............................connected to ESS server sucessfully ......................')
            print('.............................connected to ESS server sucessfully ......................')
            return True
        return False

    def ess_login(self):
        pass

    def ess_logout(self):
        pass

    def ess_is_accessable(self):
        pass

    def ess_is_conneted(self):
        pass

    def ess_add_news_target(self,top = 10,news_site='bbc'):
        try:
            add_target_url = 'news/'
            payload = {'number_of_headlines':top,'news_paper':news_site}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def ess_add_instagram_person_target(self,target_category = 'overview',author='atifaslam'):

        try:
            if(target_category == 'overview'):
                add_target_url = 'social/instagram/'
                payload = {'category': 'author', 'author': author}
                response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
                print(response.json())
                return response.json()
            if(target_category == 'post'):
                add_target_url = 'social/instagram/'
                payload = {'category': 'post', 'author': author}
                response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
                print(response.json())
                return response.json()

        except Exception as e:
            print(e)
            return {'response':'ess replied null'}

    def ess_add_instagram_search_target(self,search_string):
        try:

            add_target_url = 'social/instagram/search?'
            payload = {'search':search_string}
            response = requests.get(ESS_SERVER_BASE_URL + add_target_url,headers=Header, params=payload )
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response':'ess replied null'}

    def ess_add_facebook_person_target(self, author_account = 'prince.nuada.16', pattern_type = 'overview',number_of_posts=20):
        try:
            supported_content_types = ['completeProfile',
                                       'videos',
                                       'pictures',
                                       'posts',
                                       'overview',
                                       'closeAssociates',
                                       'checkIns',
                                       'interests'
                                       ]

            add_target_url = 'social/facebook/'
            payload = {'username': author_account,'number_of_posts':number_of_posts}

            if(pattern_type in supported_content_types):

                response = requests.post(ESS_SERVER_BASE_URL + add_target_url+pattern_type+'/', headers=Header, data=payload)
                print(response.json())
                return response.json()
            else:
                print('given content type is not supported')
                return {'error':'invalid pattern type'}
        except Exception as e:
            print(e)
            return {'error':e}

    def ess_add_facebook_page_target(self):
        pass

    def ess_add_facebook_group_target(self):
        pass

    def ess_add_facebook_hashtag_target(self):
        pass

    def ess_add_facebook_search_target(self):
        pass

    def ess_add_twitter_person_target(self,username,pattern_type='overview'):
        pass

    def ess_add_twitter_search_target(self):
        pass


    def ess_add_linkedin_person_target(self,user_id ='awais-azam-3a795b14a'):
        try:

            add_target_url = 'social/linkedin/profile/'
            payload = {'userid':user_id}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}


    def ess_add_linkedin_company_target(self,author_account='facebook'):
        try:

            add_target_url = 'social/linkedin/company/'
            payload = {'company': author_account }
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_phrase_target(self,phrase):
        try:
            add_target_url = 'social/twitter/phrase/'
            payload = {'phrase': phrase }
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_hashtags_target(self,tag):
        try:
            add_target_url = 'social/twitter/hashtag/'
            payload = {'tag': tag}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_location_target(self,location,distance):
        try:
            add_target_url = 'social/twitter/near_location_within_miles/'
            payload = {'location': location, 'distance':distance}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_since_date_target(self, pharase, date):
        try:
            add_target_url = 'social/twitter/keyword_since_date/'
            payload = {'pharse': pharase,'date':date}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_untill_date_target(self, phrase, date):
        try:
            add_target_url = 'social/twitter/keyword_until_date/'
            payload = {'pharse': phrase,'date':date}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_positive_phrase_target(self,phrase):
        try:
            add_target_url = 'social/twitter/positive_attitude/'
            payload = {'keyword': phrase }
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_negative_phrase_target(self,phrase):
        try:
            add_target_url = 'social/twitter/negative_attitude/'
            payload = {'keyword': phrase}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_refferencing_target(self,username):
        try:
            add_target_url = 'social/twitter/referencing/'
            payload = {'username': username}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_to_user_target(self,username):
        try:
            add_target_url = 'social/twitter/to/'
            payload = {'username': username}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_from_user_target(self,username):
        try:
            add_target_url = 'social/twitter/from/'
            payload = {'username': username}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_profile_target(self, username):
        try:
            add_target_url = 'social/twitter/profile/'
            payload = {'username': username}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}


    def ess_add_smart_serach_target(self,username='arooma.shah',search_site='facebook',entity_type='profile'):
        try:
            add_target_url = 'smart_search/'
            payload = {'username': username,'category':search_site,'entity_type':entity_type}
            print(payload)
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}


    def ess_add_twitter_trends_country_target(self,country):
        try:
            add_target_url = 'social/twitter/countrytrends/'
            payload = {'country': country}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def ess_add_twitter_trends_worldwide_target(self):
        try:
            add_target_url = 'social/twitter/worldtrends/'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}


    def target_internet_survey(self,name,email,phone,address):
        try:
            add_target_url = 'target_internet_survey/'
            payload = {'name': name,'email':email,'phone':phone,'address':address}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def dynamic_crawling(self,url,ip_address,domain,pictures,videos,heading,paragraphs,links,GTR,CTR):
        try:
            add_target_url = 'generic/'
            payload = {'url': url,'ip_address':ip_address,'domain':domain,'pictures':pictures,'videos':videos,'heading':heading,'paragraphs':paragraphs,'links':links,'GTR':GTR,'CTR':CTR}
            print(payload)
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def add_target(self,username,category,entity_type,GTR,CTR):
        try:
            add_target_url = 'target/'
            payload = {'username':username,'category':category,'entity_type':entity_type,'GTR':GTR,'CTR':CTR}
            response = requests.post(ESS_SERVER_BASE_URL + add_target_url, headers=Header, data=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            return {'response': 'ess replied null'}

    def news_crawling(self,top = 10,news_site='bbc'):
        try:
            add_target_url = 'news_crawler/'
            payload = {'number_of_headlines':top,'channel_name':news_site}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def instagram_target_identification(self,query):
        try:
            add_target_url = 'instagram_target_identifier/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def facebook_target_identification(self,query):
        try:
            add_target_url = 'facebook_target_identifier/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def linkedin_target_identification(self,query):
        try:
            add_target_url = 'linkedin_target_identifier/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def twitter_target_identification(self,query):
        try:
            add_target_url = 'twitter_target_identifier/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def reddit_target_identification(self,query):
        try:
            add_target_url = 'reddit_target_identifier/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def microcrawler_status(self):
        try:
            add_target_url = 'crawler_status/'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}


    def crawler_internet_connection(self):
        try:
            add_target_url = 'crawler_internet/'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def add_keybase_target(self,keywords,GTR,CTR):

        try:
            add_target_url = 'keybase/'

            payload = {'keywords':keywords,'GTR':str(GTR),'CTR':str(CTR)}
            print(type(keywords),keywords)
            print(payload)
            Header = {'Content-Type': 'application/json',
                      'Authorization': 'Token {0}'.format(ESS_API_TOKEN)}
            import json
            payload_json = json.dumps(payload)
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,json=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}


    def test_api(self,keywords,GTR,CTR):

        try:
            add_target_url = 'http://127.0.0.1:8000/core/test_api/'

            payload = {'keywords':keywords,'GTR':GTR,'CTR':CTR}
            print(payload)
            Header = {'Content-Type': 'application/json'}
            import json
            payload_json = json.dumps(payload)
            response = requests.get(add_target_url,headers=Header,json=payload_json)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}
#................................................API For Avatar Actions................................................

    def action_post(self,text,social_media,username,password):
        try:
            add_target_url = 'avatar/post/'
            payload = {'text':text,'social_media':social_media,'email':username,'password':password}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def action_comment(self,text,post_url,social_media,username,password):
        try:
            add_target_url = 'avatar/comment/'
            payload = {'text':text,'social_media':social_media,'target_post':post_url,'email':username,'password':password}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def action_reaction(self,reaction,post_url,social_media,username,password):
        try:
            add_target_url = 'avatar/reaction/'
            payload = {'Reaction':reaction,'social_media':social_media,'target_post':post_url,'email':username,'password':password}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}


    def action_share(self,text,post_url,social_media,username,password):
        try:
            add_target_url = 'avatar/comment/'
            payload = {'text':text,'social_media':social_media,'target_post':post_url,'email':username,'password':password}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def twitter_trends(self,country='pakistan'):
        try:
            add_target_url = 'twitter/trends'
            payload = {'country':country}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def twitter_world_trends(self):
        try:
            add_target_url = 'twitter/trends'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def youtube_trends(self):
        try:
            add_target_url = 'youtube/trends'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def reddit_trends(self):
        try:
            add_target_url = 'reddit/trends'
            payload = {}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def google_trends(self,country='pakistan',realtime=False):
        try:
            add_target_url = 'google/trends'
            payload = {'country':country,'realtime':realtime}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    #...................................Tools Api's.................................

    def fake_identitity_generator(self,nationality,gender,age):
        try:
            add_target_url = 'identitygenerator/'
            payload = {'nationality':nationality,'gender':gender,'age':age}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def dark_web_search(self,query):
        try:
            add_target_url = 'darksearch'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def amazon_data_scraper(self,query):
        try:
            add_target_url = 'amazon'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def daraz_data_scraper(self,query):
        try:
            add_target_url = 'daraz'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def google_scholar_data_scraper(self,query):
        try:
            add_target_url = 'scholar'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def google_patents_data_scraper(self,query):
        try:
            add_target_url = 'patents'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def tweets_near_location(self,query,location):
        try:
            add_target_url = 'twitter/phrase_near_location/'
            payload = {'phrase':query,'location':location}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def tweets_near_location_within_miles(self,location,distance):
        try:
            add_target_url = 'twitter/near_location_within_miles/'
            payload = {'location':location,'distance':str(distance)+' mil'}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def tweets_positive(self,query):
        try:
            add_target_url = 'twitter/positive/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def tweets_negative(self,query):
        try:
            add_target_url = 'twitter/negative/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

    def tweets(self,query):
        try:
            add_target_url = 'twitter/search/'
            payload = {'query':query}
            response = requests.post(ESS_SERVER_BASE_URL+add_target_url,headers=Header,data=payload)
            print(response.json())
            return response.json()

        except Exception as e:
            print(e)
        return {'response': 'ess replied null'}

if __name__== "__main__":
    pass
    #print('i have been called')
