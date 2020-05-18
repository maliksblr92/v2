from django.http import JsonResponse
import random
import time
import json
from datetime import datetime,timezone
import re

from Public_Data_Acquisition_Unit.mongo_models import *
from Portfolio_Management_System.models import *
from Keybase_Management_System.models import *
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from Data_Processing_Unit.models import *


acq = Acquistion_Manager()

class System_Stats(object):

    def __init__(self):

        pass


    def total_targets_added(self):
        return len(Global_Target_Reference.targets_added_all_time())

    def total_targets_fetched(self):
        return len(acq.get_fetched_targets())

    def targets_added_by_date(self,start_date,end_date):
        return len(Global_Target_Reference.targets_added_count_by_date_range(start_date,end_date))

    def targets_fetched_by_date(self,start_date,end_date):
        pass

    def total_keybase_crawling_targets_added(self):
        return len(Keybase_Crawling.objects())

    def total_dynamic_crawling_targets_added(self):
        return len(Dynamic_Crawling.objects())

    def total_keybase_crawling_targets_fetched(self):
        return len(Keybase_Response_TMS.objects())

    def total_dynamic_crawling_targets_fetched(self):
        return len(Dynamic_Crawling_Response_TMS.objects())

    def top_profiles_with_negative_behavior(self,website='facebook',target_type='profile'):

        username_list = []
        if(website == 'facebook' and target_type =='profile'):
            responces = Facebook_Profile_Response_TMS.objects()
            for resp in responces:
                resp_j = resp.to_mongo()

                if(resp_j['behaviour'].lower() == 'negative'):

                    if(resp_j['username']):
                        username_list.append(resp.username)

            return username_list

        return None

    def top_twitter_profiles_with_highest_counts(self,top=20,count_type='likes_count'):
        data_list = []
        try:
            responces = Twitter_Response_TMS.objects().order_by(''+count_type)[:top]
            for resp in responces:
                resp.to_mongo()
                data_list.append({'name':resp.name,'count':int(re.search(r'\d+', resp[count_type]).group())})

            return data_list
        except Exception as e:
            return None


    def total_periodic_targets(self):
        return len(Periodic_Targets.objects())

    def total_expired_targets(self,website=None):

        expired_count = 0
        expired_count += Facebook_Profile.expired_targets_count()
        expired_count += Facebook_Page.expired_targets_count()
        expired_count += Facebook_Group.expired_targets_count()
        expired_count += Instagram_Profile.expired_targets_count()
        expired_count += Twitter_Profile.expired_targets_count()
        expired_count += Linkedin_Profile.expired_targets_count()
        expired_count += Linkedin_Company.expired_targets_count()
        expired_count += Reddit_Profile.expired_targets_count()
        expired_count += Youtube_Channel.expired_targets_count()
        expired_count += Keybase_Crawling.expired_targets_count()
        expired_count += Dynamic_Crawling.expired_targets_count()


        return expired_count



class Data_Queries(object):

    def __init__(self):
        pass


    def get_facebook_close_associates(self,response_id):
        pass

    def get_twitter_followers(self,response_id):
        pass

    def get_instagram_followers(self,responces_id):

        pass

    def check_if_responces_is_supported(self,resp_obj):
        supported_links = (('instagram',Instagram_Response_TMS),
                           ('facebook',Facebook_Profile_Response_TMS),
                           ('twitter',Twitter_Response_TMS)
                           )

        for title,cla in supported_links:
            print(title,cla)
            if(isinstance(resp_obj,cla)):
                return title

            return None

    def get_object_website(self,object):
        gtr_id = object.GTR
        GTR = acq.get_gtr_by_id(gtr_id)
        return GTR.website.name.lower()

    def portfolio_link_analysis(self,portfolio_id):

        supported_links = [Instagram_Response_TMS,Facebook_Profile_Response_TMS]
        alpha_nodes_list = []
        n_data_full = []

        portfolio_obj = Portfolio_PMS.objects(id=portfolio_id).first()
        linked_responses = Portfolio_Linked_PMS.objects(alpha_reference=portfolio_obj)
        for response in linked_responses:
                website =  self.get_object_website(response.beta_reference)
                print(website)   #self.check_if_responces_is_supported(response.beta_reference)
                if(website):
                    response_obj = response.beta_reference.to_mongo()
                    alpha_node,beta_node_list = self.generalize_data_for_nodes(website,'profile',response_obj)
                    alpha_nodes_list.append(alpha_node)
                    n_data = self.convert_nodes_to_graph_data_for_portfolio(alpha_node,beta_node_list)
                    print(len(linked_responses),website)
                    n_data_full = n_data_full + n_data

        p_node = {'name': portfolio_obj.name,
                  'value': 1,
                  'children': [],
                  "linkWith": [],
                  'collapsed': 'true',
                  'fixed': 'false',
                  "image": '',
                  }

        for alpha in alpha_nodes_list:
            p_node['linkWith'].append(alpha['username'])

        n_data_full.append(p_node)
        print(n_data_full)

        return json.dumps(n_data_full)






    def generalize_data_for_nodes(self,website,target_type,data_object):

        beta_nodes_list = []
        alpha_node = {}

        if(website == 'facebook'):

            alpha_node['username']  = data_object['username']
            alpha_node['picture_url']  = data_object['profile_picture_url']['profile_picture']

            for item in data_object['close_associates']:

                if(len(item['username'])>0):
                    temp_dic = {'username':item['username'],'picture_url':item['media_directory']}
                    beta_nodes_list.append(temp_dic)
                else:
                    temp_dic = {'username': item['id'], 'picture_url': item['media_directory']}
                    beta_nodes_list.append(temp_dic)
            return (alpha_node,beta_nodes_list)

        elif(website == 'instagram'):

            alpha_node['username']  = data_object['username']
            alpha_node['picture_url']  = data_object['profile_picture_url']

            for item in data_object['followers']:
                temp_dic = {'username':item['username'],'picture_url':item['picture_image_url']}
                beta_nodes_list.append(temp_dic)

            return (alpha_node,beta_nodes_list)

        elif (website == 'twitter'):

            alpha_node['username'] = data_object['author_account']
            alpha_node['picture_url'] = data_object['profile_url']

            for item in data_object['followers']:
                temp_dic = {'username': item['username'], 'picture_url': item['avatar']}
                beta_nodes_list.append(temp_dic)

            return (alpha_node, beta_nodes_list)




    def convert_nodes_to_graph_data(self,alpha_node,beta_nodes_list):

        n_data = []

        a_node = {'name': alpha_node['username'],
                    'value': 1,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": alpha_node['picture_url'],
                    }



        for i, item in enumerate(beta_nodes_list):

            print(item)

            node = {'name': item['username'],
                    'value': 0.2,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": item['picture_url'],
                    }

            a_node['children'].append(node)

            #n_data.append(node)

        n_data.append(a_node)





        print(n_data)
        return json.dumps(n_data)

    def convert_nodes_to_graph_data_for_portfolio(self,alpha_node,beta_nodes_list):

        n_data = []

        a_node = {'name': alpha_node['username'],
                    'value': 1,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": alpha_node['picture_url'],
                    }



        for i, item in enumerate(beta_nodes_list):

            print(item)

            node = {'name': item['username'],
                    'value': 0.2,
                    'children': [],
                    "linkWith": [],
                    'collapsed': 'true',
                    'fixed': 'false',
                    "image": item['picture_url'],
                    }

            a_node['children'].append(node)

            #n_data.append(node)

        n_data.append(a_node)





        print(n_data)
        return n_data





"""
TIME_FACTOR = int((datetime.now()-datetime(2019,12,17)).total_seconds())
ADDITION_FACTOR = random.randint(200, 400)
SUBTRACTION_FACTOR = 1000
MULTIPLICATION_FACTOR = random.randint(2, 4)

class System_Log_Manager(object):

    def __init__(self):
        pass



    def refresh_fake_prams(self):

        global ADDITION_FACTOR
        global SUBTRACTION_FACTOR
        global MULTIPLICATION_FACTOR

        ADDITION_FACTOR = random.randint(200, 400)
        SUBTRACTION_FACTOR = 100000
        MULTIPLICATION_FACTOR = random.randint(10, 20)

    def article_stat_for_slo(self):
        self.refresh_fake_prams()

        data = {
            'Article Select Count ':25+int(((TIME_FACTOR)*1+ADDITION_FACTOR)),
            'Article Reviewed Count':6+int(((TIME_FACTOR)*0.6+ADDITION_FACTOR)),
            'Requested By PCO Count':3+int(((TIME_FACTOR)*0.3+ADDITION_FACTOR)),
            'Rejected By RPO Count':2+int(((TIME_FACTOR)*0.2+ADDITION_FACTOR)),

            }

        return data

    def article_stat_overview(self):
        self.refresh_fake_prams()

        data = {
            'New Article Count': 50 + int(((TIME_FACTOR) * 3 + ADDITION_FACTOR)),
            'Author Count': 6 + int(((TIME_FACTOR) * 0.1 + ADDITION_FACTOR)),
            'Hashtag Count': 3 + int(((TIME_FACTOR) * 0.2 + ADDITION_FACTOR)),


        }

        return data


    def my_article_stat(self):
        self.refresh_fake_prams()

        data = {
            'Selected Count': 5 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Revised Count': 3 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To PCO ': 3 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To RPO ': 2 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To DSO': 4 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    def ticket_stat(self):
        self.refresh_fake_prams()

        data = {
            'Read Tickets': 50 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'New Coming Tickets': 34 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Total Inbox Count': 87 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Replied Tickets': 22 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Tickets With New Reply': 29 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }
        return data


    def fetch_stat(self):
        self.refresh_fake_prams()

        data = {
            'Fetched Author': 536 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Fetched Content': 985 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    #......................................STATS FOR WORKLOAD PAGE......................................................

    def extracted_article(self):
        self.refresh_fake_prams()

        data = {
            'Social': 506 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 300 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 99 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 46 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    def extracted_selected_all_sites(self):
        self.refresh_fake_prams()

        data = {
        'extracted':{
            'Social': 606 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Search': 400 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 199 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Blog': 146 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Image': 106 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 82 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 99 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        },
        'selected':{
            'Social': 352 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Search': 156 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Blog': 21 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Image': 22 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 88 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 45 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        }
        return data

    def extracted_selected_all_social_sites(self):
        self.refresh_fake_prams()

        data = {
            'extracted': {
                'Twitter': 609 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 400 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 199 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 146 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            },
            'selected': {
                'Twitter': 356 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 256 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 7 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            }

        }

        return data

    def processed_article(self):
        self.refresh_fake_prams()

        data = {
            'Image': 506 + int(((TIME_FACTOR) * 0.32 + ADDITION_FACTOR)),
            'Instagram': 300 + int(((TIME_FACTOR) * 0.68  + ADDITION_FACTOR)),

        }

        return data

    def article_trend(self):
        self.refresh_fake_prams()

        data = {
            '12-12-2019': 78 + int(((TIME_FACTOR) * 0.5 + ADDITION_FACTOR)),
            '13-12-2019': 34 + int(((TIME_FACTOR) * 0.6 + ADDITION_FACTOR)),
            '14-12-2019': 87 + int(((TIME_FACTOR) * 0.8 + ADDITION_FACTOR)),
            '15-12-2019': 22 + int(((TIME_FACTOR) * 0.6 + ADDITION_FACTOR)),
            '16-12-2019': 29 + int(((TIME_FACTOR) * 0.68 + ADDITION_FACTOR)),
            '17-12-2019': 22 + int(((TIME_FACTOR) * 0.52 + ADDITION_FACTOR)),
            '18-12-2019': 29 + int(((TIME_FACTOR) * 0.85 + ADDITION_FACTOR)),
        }

        return data

    def send_to_pco(self):
        self.refresh_fake_prams()

        data = {
            'Twitter': 356 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 256 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 7 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        return data

    def send_to_rpo(self):
        self.refresh_fake_prams()

        data = {
            'Twitter': 128 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Facebook': 102 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Instagram': 18 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Other': 19 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        return data
"""
