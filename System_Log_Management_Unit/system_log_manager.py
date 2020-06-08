from django.http import JsonResponse
import random
import time
import json
from datetime import datetime,timedelta
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

    def targets_added_by_date(self,days=10):
        data_list = []
        for ss in Supported_Website.objects():
            res = Global_Target_Reference.targets_added_count_by_date_range_and_website_name(datetime.datetime.utcnow()-timedelta(days=days),datetime.datetime.utcnow(),ss.name)
            data_list.append({'name': ss.name, 'count': len(res)})

        return data_list

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
                try:
                    resp.to_mongo()
                    data_list.append({'name':resp.name,'count':int(re.search(r'\d+', resp[count_type]).group())})
                except:
                    pass
            return sorted(data_list, key = lambda i: i['count'])
        except Exception as e:
            print(e)
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

        supported_links = ['instagram','facebook','twitter']

        try:
            gtr_id = object.GTR
            GTR = acq.get_gtr_by_id(gtr_id)
            targ_obj = acq.get_dataobject_by_gtr(GTR)

            if(GTR.website.name.lower() in supported_links and targ_obj.target_type == 'profile'):
                return GTR.website.name.lower()

            return None
        except Exception as e:
            print(e)

            return None

    def portfolio_link_analysis(self,portfolio_id):
        n_data_full = []

        try:
            supported_links = [Instagram_Response_TMS,Facebook_Profile_Response_TMS]
            alpha_nodes_list = []


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

            print(portfolio_obj);
            p_node = {'name': portfolio_obj.name,
                      'hero': portfolio_obj.name,
                      'value': 1,
                      'children': [],
                      "linkWith": [],
                    #   'collapsed': 'true',
                    #   'fixed': 'false',
                      "img": '',
                      }

            for alpha in alpha_nodes_list:
                p_node['linkWith'].append(alpha['username'])

            # n_data_full.append(p_node)
            dic={
                "name":portfolio_obj.name,
                "hero":portfolio_obj.name,
                "img":"/static/images/anonymous_logo.jpg",
                "children":n_data_full,
            }
       
            print(dic)
            return json.dumps(dic)

        except Exception as e:
            print(e)
            return json.dumps(n_data_full)




    def generalize_data_for_nodes(self,website,target_type,data_object):

        max_node_limit = 100

        beta_nodes_list = []
        alpha_node = {}

        if(website == 'facebook'):

            alpha_node['username']  = data_object['username']
            alpha_node['picture_url']  = data_object['profile_picture_url']['profile_picture']

            for item in data_object['close_associates'][0:max_node_limit]:

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

            for item in data_object['followers'][0:max_node_limit]:
                temp_dic = {'username':item['username'],'picture_url':item['picture_image_url']}
                beta_nodes_list.append(temp_dic)

            return (alpha_node,beta_nodes_list)

        elif (website == 'twitter'):

            alpha_node['username'] = data_object['author_account']
            alpha_node['picture_url'] = data_object['profile_url']

            for item in data_object['followers'][0:max_node_limit]:
                temp_dic = {'username': item['username'], 'picture_url': item['avatar']}
                beta_nodes_list.append(temp_dic)
           

            return (alpha_node, beta_nodes_list)




    def convert_nodes_to_graph_data(self,alpha_node,beta_nodes_list):

        n_data = []

        try:
            a_node = {'hero': alpha_node['username'],
                        'value': 1,
                        'children': [],
                        "linkWith": [],
                        # 'collapsed': 'true',
                        # 'fixed': 'false',
                        "img": alpha_node['picture_url'],
                        }



            for i, item in enumerate(beta_nodes_list):

                print(item)

                node = {'hero': item['username'],
                        'value': 0.2,
                        'children': [],
                        "linkWith": [],
                        # 'collapsed': 'true',
                        # 'fixed': 'false',
                        "img": item['picture_url'],
                        }

                a_node['children'].append(node)

                #n_data.append(node)

            n_data.append(a_node)

            dic={
                "name":alpha_node['username'],
                "hero":alpha_node['username'],
                "img":"/static/images/anonymous_logo.jpg",
                "children":n_data,
            }

            return json.dumps(dic)
        except Exception as e:
            print(e)
            return json.dumps(n_data)

    def convert_nodes_to_graph_data_for_portfolio(self,alpha_node,beta_nodes_list):

        n_data = []

        a_node = {'hero': alpha_node['username'],
                    'value': 1,
                    'children': [],
                    "linkWith": [],
                    # 'collapsed': 'true',
                    # 'fixed': 'false',
                    "img": alpha_node['picture_url'],
                    }



        for i, item in enumerate(beta_nodes_list):

            print(item)

            node = {'hero': item['username'],
                    'value': 0.2,
                    'children': [],
                    "linkWith": [],
                    # 'collapsed': 'true',
                    # 'fixed': 'false',
                    "img": item['picture_url'],
                    }

            a_node['children'].append(node)

            #n_data.append(node)

        n_data.append(a_node)





        print(n_data)
        return n_data

class Data_Analysis():

    def __init__(self):
        pass


    def all_news_common_words(self,channel_list=['geo','india_today','ary','ndtv','dawn','zee','abp']):

        common_words = []

        for channel in channel_list:
            news = News.objects(Q(channel=channel.upper())).order_by('-created_on').first()
            if(news):
                print(news.common_words)
                common_words += news.common_words
        print(common_words)

