from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.ess_api_controller import Ess_Api_Controller
from Public_Data_Acquisition_Unit.ais_api_controller import Ais_Api_Controller
from OSINT_System_Core.publisher import publish
from Public_Data_Acquisition_Unit.ess_api_controller import *
from Public_Data_Acquisition_Unit.mongo_models import *
from OSINT_System_Core.Data_Sharing import Mongo_Lookup
from Portfolio_Management_System.models import Portfolio_PMS
from bson import ObjectId

import logging

import datetime
ess = Ess_Api_Controller()
ais = Ais_Api_Controller()
class Acquistion_Manager(object):

    """
    this class is responsible to communicate with mongomodels and interact with the Ess API

    """

    def __init__(self):
        pass

    def get_gtr(self,website_reff,target_type_index):
        gtr =  Global_Target_Reference()
        gtr.create(website_reff,target_type_index)
        return gtr

    def add_target(self,website_id,target_type_index,portfolio_id=None,**kwargs):

        try:
            gtr = self.get_gtr(self.get_website_by_id(website_id),target_type_index)
            appropriate_class, _ , _ = self.get_appropriate_method(gtr)
            print(appropriate_class)
            ac_object = appropriate_class()
            target = ac_object.create(gtr,kwargs)

            print(portfolio_id)
            if(portfolio_id is not None):
                obj = Portfolio_PMS.objects(id=ObjectId(portfolio_id)).first()
                obj.add_social_target(target)

            if('periodic_interval' in kwargs):
                interval = kwargs['periodic_interval']
                print('............interval '+str(interval))
                if(interval > 0):
                    #print('in here')
                    pt = Periodic_Targets()
                    pt.GTR = gtr
                    pt.target_reff = target
                    pt.re_invoke_time =  datetime.datetime.utcnow() + datetime.timedelta(minutes=interval)
                    pt.save()
                    #publish(' {0} is added to periodic targets'.format(target), message_type='info', module_name=__name__)

                else:
                    target.make_me_expire()
            else:
                target.make_me_expire()

            self.add_crawling_target(gtr,0)
            return target
        except Exception as e:
            print(e)
            publish(e, message_type='error', module_name=__name__)
            return False

    def add_bulk_targts(self,website_id,target_type_index,prime_argument_list,expired_on,periodic_interval,**kwargs):
        """
        this method is to create multiple crawling targets in one go , it first creates a gtr and then call
        add targets and pass the minimum parameters required to submit a target
        it accept periodic interval and expired_on date to pass it to add_target functuion as kwargs as single target
        rest of the procedure will be same

        ** this functions has a special argument called prime argumet list its the argument which each type of target must required atleast **
        like username of the social profile


        :param website_id:
        :param target_type_index:
        :param prime_argument_list:
        :return Boolian:
        """
        if(website_id and len(prime_argument_list)):

            recursive = False
            hop = 0
            breadth = 0

            if 'recursive' in kwargs: recursive = kwargs['recursive']
            if 'hop' in kwargs: hop = kwargs['hop']
            if 'breadth' in kwargs: breadth = kwargs['breadth']

            for prime_argument in prime_argument_list:
                #gtr = self.get_gtr(website_id, target_type_index)




                if(not self.add_target(website_id,target_type_index,username=prime_argument,expired_on=expired_on,periodic_interval=periodic_interval,recursive=recursive,hop=hop,breadth=breadth)):
                    print('unable to add bulk target for '+prime_argument)
                    publish('unable to add bulk target for '+prime_argument,message_type='notification')

            return True

        else:

            publish('unable to add bulk target few arguments are missing ', message_type='notification', module_name=__name__)
            return False


    def add_crawling_target(self, gtr,ctr):

        """
        this is simplified method to add a task to crawler , user only need to pass the gtr of the target rest is been taken care of .
        this method is used by the celery periodic worker to add the periodic task to crawler.
        appropriate function is a function pointer later used to submit a task to ess using a specific function returned by the methond
        :param gtr:
        :return:
        """
        try:
            appropriate_class, appropriate_ess_method, _ = self.get_appropriate_method(gtr)


            kwargs = appropriate_class.objects(GTR=gtr.id)[0].to_mongo()
            print(kwargs)
            """
            user needs to pass this kwargs and gtr to submit a task to ess,
            kwargs is taken from the database and gtr is the only thing which periodic database need to provide
            """
            print(gtr.target_type)

            if(gtr.target_type == 'keybase_crawling'):
                keybase = appropriate_class.objects(GTR=gtr.id)[0]
                keywords = keybase.keybase_ref.keywords + keybase.keybase_ref.mentions+keybase.keybase_ref.phrases+keybase.keybase_ref.hashtags

                print('..............................adding keybase target ................................')
                print(keywords)
                response = appropriate_ess_method(keywords,gtr.id,ctr)
                if(response is not None):
                    print(response)
                    publish(' '+keybase.keybase_ref.title+' target added successfully', message_type='notification', module_name=__name__)
                else:
                    publish(' ' + keybase.keybase_ref.title + ' not queued on ESS ',
                            message_type='notification', module_name=__name__)

            elif (gtr.target_type == 'dynamic_crawling'):


                ip=domain=pictures=videos=headings=paragraphs=links = False



                #if 'url' in kwargs: url = kwargs['url']
                if 'ip' in kwargs: ip = kwargs['ip']
                if 'domain' in kwargs: domain = kwargs['domain']
                if 'pictures' in kwargs: pictures = kwargs['pictures']
                if 'videos' in kwargs: videos = kwargs['videos']
                if 'headings' in kwargs: headings = kwargs['headings']
                if 'paragraphs' in kwargs: paragraphs = kwargs['paragraphs']
                if 'links' in kwargs: links = kwargs['links']



                response = appropriate_ess_method(kwargs['url'],ip,domain,pictures,videos,headings,paragraphs,links,gtr.id,ctr)


                if (response is not None):
                    print(response)
                    publish(' ' + kwargs['url'] + ' target added successfully', message_type='notification',
                            module_name=__name__)
                else:
                    publish(' ' + kwargs['url'] + ' not queued on ESS ',
                            message_type='notification', module_name=__name__)

            else:
                #for normal profile targets
                #ess_api needs basic arguments for adding a target

                username = kwargs['username']
                category = gtr.website.name.lower()
                entity_type = gtr.target_type

                GTR = gtr.id
                CTR = ctr

                print(username,category,entity_type,GTR,CTR)

                response = appropriate_ess_method(username,category,entity_type,GTR,CTR)
                print(response)


                if (response is not None):
                    print(response)
                    publish(' '+username+' added successfully', message_type='notification', module_name=__name__)
                else:
                    publish(' '+username+' not queued on ESS ', message_type='notification', module_name=__name__)


            return True
        except Exception as e:
            publish(str(e), message_type='alert', module_name=__name__)
            return False
        pass

    def get_tasks_kwargs(self,gtr):
        pass


    def get_target_type_index_by_type_name(self,website_id,type_name):
        target_types = Supported_Website.objects(id=website_id).first().target_type
        for index,type in enumerate(target_types):
            if(type == type_name):
                return index



    def is_recursive_supported(self,website_name):
        recursive_supported = ['facebook','twitter','instagram']

        return website_name.lower() in recursive_supported

    def add_recursive_crawling_target(self,gtr_id):
        gtr = self.get_gtr_by_id(gtr_id)
        if(gtr):
            targ_obj = self.get_dataobject_by_gtr(gtr)
            if(targ_obj):
                print('target object found ' + str(targ_obj))
                if(self.is_recursive_supported(targ_obj.GTR.website.name)):
                    if(targ_obj.is_recursive()):
                        hop = targ_obj.hop
                        if(hop > 0):
                            print('hop is '+str(hop))
                            breadth = targ_obj.breadth
                            resp_obj = self.get_data_response_object_by_gtr_id(gtr.id)
                            if(resp_obj):
                                print('response object found '+ str(resp_obj))
                                user_list = resp_obj.get_top_associates(breadth)
                                if(len(user_list)>0):
                                    print('got user list ')
                                    resp = self.add_bulk_targts(targ_obj.GTR.website.id,self.get_target_type_index_by_type_name(targ_obj.GTR.website.id,targ_obj.target_type),user_list,targ_obj.expired_on,targ_obj.periodic_interval,recursive=True,hop=hop-1,breadth=breadth)
                                    if(resp):
                                        targ_obj.hop = targ_obj.hop - 1
                                        targ_obj.save()
                                        publish('recursive crawling targets added for '+str(targ_obj),message_type='notification')

                                    else:
                                        print('failed to submit recursive crawling target')
                                else:
                                    print('userlist is empty')
                            else:
                                print('response object not found ')



                        else:
                            print('hop is satisfied')
                    else:
                        print('target does not support recursive crawling')
                else:
                    print('target website does not support recursive crawling')
            else:
                print('target object not found')








    def get_website_by_id(self,website_id):
        return Supported_Website.objects(id=website_id)[0]

    def get_appropriate_method(self,gtr):
        """
        this is a high-order method whcic takes gtr as an argument and return the function object
        depending on the website and website-type and target-type
        it returns a tuple of two objects one is a mongo model class's and other is a ess method's object
        :param gtr:
        :return function_object:
        """

        #gtr = Global_Target_Reference.objects(id=gtr)
        if(gtr.website.name == 'Facebook'):
            if(gtr.target_type == 'profile'):
                return (Facebook_Profile,ess.add_target,Facebook_Profile_Response_TMS)
            elif (gtr.target_type == 'page'):
                return (Facebook_Page,ess.add_target,Facebook_Page_Response_TMS)
            elif (gtr.target_type == 'group'):
                return (Facebook_Group,ess.add_target,Facebook_Group_Response_TMS)
            elif (gtr.target_type == 'search'):
                pass
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)

        elif (gtr.website.name == 'Twitter'):
            if (gtr.target_type == 'profile'):
                return (Twitter_Profile,ess.add_target,Twitter_Response_TMS)
            elif (gtr.target_type == 'search'):
                pass
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)

        elif (gtr.website.name == 'Instagram'):
            if (gtr.target_type == 'profile'):
                return (Instagram_Profile,ess.add_target,Instagram_Response_TMS)
            elif (gtr.target_type == 'search'):
                pass
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)

        elif (gtr.website.name == 'Linkedin'):
            if (gtr.target_type == 'profile'):
                return (Linkedin_Profile, ess.add_target,Linkedin_Profile_Response_TMS)
            elif (gtr.target_type == 'company'):
                return (Linkedin_Company, ess.add_target,Linkedin_Company_Response_TMS)
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)
        elif (gtr.website.name == 'custom'):
            if (gtr.target_type == 'dynamic_crawling'):
                return (Dynamic_Crawling, ess.dynamic_crawling,Dynamic_Crawling_Response_TMS)
            elif (gtr.target_type == 'keybase_crawling'):
                return (Keybase_Crawling,ess.add_keybase_target ,Keybase_Response_TMS)
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)
        elif (gtr.website.name == 'Reddit'):
            if (gtr.target_type == 'profile'):
                return (Reddit_Profile,ess.add_target,Reddit_Profile_Response_TMS)
            elif (gtr.target_type == 'subreddit'):
                return (Reddit_Subreddit, ess.add_target ,Reddit_Subreddit_Response_TMS)
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)
        elif (gtr.website.name == 'Youtube'):
            if (gtr.target_type == 'channel'):
                return (Youtube_Channel, ess.add_target, Youtube_Response_TMS)
            else:
                publish('target type not defined', message_type='alert', module_name=__name__)


        else:
            publish('website type not defined',message_type='alert',module_name=__name__)

    def get_data_response_object_by_gtr_id(self,gtr_id):

        gtr = self.get_gtr_by_id(gtr_id)
        _, _,appropriate_class = self.get_appropriate_method(gtr)

        print(gtr.id)
        dataobject = appropriate_class.objects(GTR=str(gtr_id)).first()
        return dataobject




    def get_dataobject_by_gtr(self,gtr):
        appropriate_class,_,_= self.get_appropriate_method(gtr)
        # now we have the actual method
        #now find the gtr id in this method to get the object

        dataobject = appropriate_class.objects(GTR=gtr.id).first()
        return dataobject

    def get_dataobjects_by_gtr_list(self,gtr_list):
        object_list = []
        for gtr in gtr_list:
            obj = self.get_dataobject_by_gtr(gtr)
            if(obj is not None):
                object_list.append(obj)

        return object_list

    def add_facebook_target(self,gtr,kwargs):
        pass

    def add_twitter_target(self):
        pass

    def get_picture_by_facebook_username(self,username):
        try:
            obj =  Facebook_Profile.find_object(username).first()
            if(obj):
                res_obj = Facebook_Profile_Response_TMS.objects(Q(username=obj.username) | Q(author_id=int(bool(obj.user_id)))).first()
                if(res_obj is not None):
                    res_obj_json = res_obj.to_mongo()
                    print(res_obj_json)
                    return res_obj_json['profile_picture_url']['profile_picture']
        except:
            return ''


    def get_gtr_by_id(self,gtr_id):
        return Global_Target_Reference.objects(id=gtr_id)[0]

    def get_periodic_target_list(self):
        return Periodic_Targets.objects()

    def do_invoke_target(self,gtr,ctr):
        self.add_crawling_target(gtr,ctr)

    def target_polling(self):

        tasks_list = self.get_periodic_target_list()

        for task in tasks_list:
            time_now = datetime.datetime.utcnow()
            invoke_time = task.re_invoke_time

            if (time_now > invoke_time):
                # then invoke the task
                #ap_cls,_ = self.get_appropriate_method(task.GTR)
                #target = ap_cls.objects(GTR=task.GTR.id)[0]
                task.re_invoke_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=task.target_reff.periodic_interval)
                task.CTR = task.CTR+1
                task.save()
                self.do_invoke_target(task.GTR,task.CTR)
                print('*************************************Task Reinvoked {0}*****************************'.format(task.target_reff))

            self.remove_expired_targets(task)
        print('..................................Task Polling Survey Completed..................................')

    def remove_expired_targets(self,task):
        time_now = datetime.datetime.utcnow()
        expiry_time = task.target_reff.expired_on

        if (time_now > expiry_time):
            task.target_reff.make_me_expire()
            task.delete()


            publish({'server_name': 'OCS', 'node_id': 1, 'messege_type': 'control, awais'})
            print('######################################### expired task deleted #####################################')

    def get_custom_webiste_id(self):
        return Supported_Website.objects(name='custom').first().id
#.........................................................Query Functions...............................................

    def get_all_supported_sites(self):
        return Supported_Website.get_all_supported_sites()
    def get_all_social_sites(self):
        return Supported_Website.get_all_social_websites()
    def get_all_blog_sites(self):
        return Supported_Website.get_all_blog_websites()
    def get_all_news_sites(self):
        return Supported_Website.get_all_news_websites()
    def get_all_periodic_targets(self):
        return Periodic_Targets.get_all_periodic_task()

#.........................................................Staticsticall Functions.......................................

    """
    functions bellow return a tuple which contains actual object returned by the query and count
    """

    def targets_added_all_time(self):
        res = Global_Target_Reference.targets_added_all_time()
        res = self.get_dataobjects_by_gtr_list(res)
        return (res,len(res))

    def targets_added_today(self):
        res = Global_Target_Reference.targets_added_today()
        res = self.get_dataobjects_by_gtr_list(res)
        return (res, len(res))

    def targets_added_count_by_date_range(self,start_datetime,end_datetime):
        res = Global_Target_Reference.targets_added_count_by_date_range(start_datetime,end_datetime)
        res = self.get_dataobjects_by_gtr_list(res)
        return (res, len(res))

    def target_added_count_by_website_type(self,website_type):
        res = Global_Target_Reference.target_added_count_by_website_type(website_type)
        res = self.get_dataobjects_by_gtr_list(res)
        return (res, len(res))

    def target_added_count_by_website(self,website_id):
        res = Global_Target_Reference.target_added_count_by_website(website_id)
        res = self.get_dataobjects_by_gtr_list(res)
        return (res, len(res))

    def get_all_expired_targets(self):
        objects,_ = self.targets_added_all_time()
        all_expired_objects_list = []

        for obj in objects:
            if(obj is not None):
                if(obj.am_i_expired()):
                    all_expired_objects_list.append(obj)

        return all_expired_objects_list

    def fetch_smart_search(self,username,search_site,entity_type):
        try:
            response = ess.ess_add_smart_serach_target(username,search_site,entity_type)

            return response
        except Exception as e:
            print(e)

    def target_internet_survey(self,name,email,phone,address):
        return ess.target_internet_survey(name,email,phone,address)

    def dynamic_crawling(self,url,ip_address,domain,pictures,videos,heading,paragraphs,links,GTR,CTR):
        return ess.dynamic_crawling(url,ip_address,domain,pictures,videos,heading,paragraphs,links,GTR,CTR)

    def get_all_fetched_targets(self):
        pass
        """
        responses = []

        GTRs = Global_Target_Reference.objects.all().order_by('-id')

        for gtr in GTRs:
            obj = Facebook_Profile.objects(GTR=gtr.id)
            if(len(obj) <= 0):
                obj = Twitter_Profile.objects(GTR=gtr.id)
                if (len(obj) <= 0):
                    obj = Instagram_Person.objects(GTR=gtr.id)
                    if (len(obj) <= 0):
                        obj = Linkedin_Person.objects(GTR=gtr.id)
                        if (len(obj) <= 0):
                            obj = Linkedin_Company.objects(GTR=gtr.id)
                            if (len(obj) <= 0):
                                pass
                            else:
                                responses.append([obj[0],self.get_target_instance_by_GTR(gtr.id),self.get_social_site_instance_by_GTR(gtr.id)])
                        else:
                            responses.append([obj[0],self.get_target_instance_by_GTR(gtr.id),self.get_social_site_instance_by_GTR(gtr.id)])
                    else:
                        responses.append([obj[0],self.get_target_instance_by_GTR(gtr.id),self.get_social_site_instance_by_GTR(gtr.id)])
                else:
                    responses.append([obj[0],self.get_target_instance_by_GTR(gtr.id),self.get_social_site_instance_by_GTR(gtr.id)])
            else:
                responses.append([obj[0],self.get_target_instance_by_GTR(gtr.id),self.get_social_site_instance_by_GTR(gtr.id)])


        return responses
        """

    def get_fetched_targets(self,website=None,top=50):
        responses = []

        ml = Mongo_Lookup()
        GTRs = Global_Target_Reference.objects.all().order_by('-id')

        for gtr in GTRs:

            if(gtr.website.name.lower() == website or website == None):
                appropriate_model_targ,_ ,appropriate_model_resp = self.get_appropriate_method(gtr)
                #obj_amt = appropriate_model_targ()
                #obj_amr = appropriate_model_resp()

                if(appropriate_model_resp is not None):

                    #print(appropriate_model_targ,appropriate_model_resp,gtr.id)

                    resp = appropriate_model_resp.objects(GTR=str(gtr.id)).first()
                    if(resp is not None):
                        targ = appropriate_model_targ.objects(GTR=gtr.id).first()

                        responses.append([resp, targ])


                #resp = Facebook_Profile.objects(GTR=gtr.id)
                #targ = Facebook_Profile.objects(GTR=gtr.id)






        return responses

    def get_linked_targets(self,link_type='portfolio',gtr_list=[]):

        if(len(gtr_list)>0 and link_type =='portfolio'):

            responses = []

            #ml = Mongo_Lookup()
            GTRs = []
            for gtr_id in gtr_list:
                 GTRs.append(Global_Target_Reference.objects(id=gtr_id).first())


            #GTRs = Global_Target_Reference.objects.all().order_by('-id')

            for gtr in GTRs:


                appropriate_model_targ, _, appropriate_model_resp = self.get_appropriate_method(gtr)
                # obj_amt = appropriate_model_targ()
                # obj_amr = appropriate_model_resp()

                if (appropriate_model_resp is not None):

                    # print(appropriate_model_targ,appropriate_model_resp,gtr.id)

                    resp = appropriate_model_resp.objects(GTR=str(gtr.id)).first()
                    if (resp is not None):
                        targ = appropriate_model_targ.objects(GTR=gtr.id).first()

                        responses.append([resp, targ])

                # resp = Facebook_Profile.objects(GTR=gtr.id)
                # targ = Facebook_Profile.objects(GTR=gtr.id)

            return responses




    def get_fetched_keybases(self,top=50):
        responses = []

        #ml = Mongo_Lookup()
        GTRs = Global_Target_Reference.objects.all().order_by('-id')

        for gtr in GTRs:

            if(gtr.website.name == 'custom'):
                appropriate_model_targ,_ ,appropriate_model_resp = self.get_appropriate_method(gtr)

                print(appropriate_model_targ,appropriate_model_resp)

                if(appropriate_model_targ.target_type =='keybase_crawling'):
                    #obj_amt = appropriate_model_targ()
                    #obj_amr = appropriate_model_resp()

                    if(appropriate_model_resp is not None):

                        #print(appropriate_model_targ,appropriate_model_resp,gtr.id)

                        resp = appropriate_model_resp.objects(GTR=str(gtr.id)).first()
                        if(resp is not None):
                            targ = appropriate_model_targ.objects(GTR=gtr.id).first()

                            responses.append([resp, targ])


                #resp = Facebook_Profile.objects(GTR=gtr.id)
                #targ = Facebook_Profile.objects(GTR=gtr.id)






        return responses


    def crawler_internet_connection(self):

        resp = ess.crawler_internet_connection()
        #print(resp[0]['internet']['download'],resp[0]['internet']['upload'],resp[0]['internet']['timestamp'])
        return {'download':resp[0]['internet']['download'],'upload':resp[0]['internet']['upload'],'stamp':resp[0]['internet']['timestamp']}

    def mircocrawler_status(self):


       return ess.microcrawler_status()



    def fetch_news(self,top=10, GTR_ID=1):
        # fetch data from ess server

        news_sites = ['ary', 'bbc', 'geo', 'dawn', 'abp', 'ndtv', 'indiatoday', 'zee']

        try:
            for news in news_sites:
                print('.......................................fetching News now working on  {0}...........................'.format(news))
                response = ess.news_crawling(top, news)
                print(response)
        except Exception as e:
            print(e)

    def fetch_top_trends(self):
        ess.google_trends(country='india')
        ess.youtube_trends()
        ess.twitter_trends()
        ess.reddit_trends()
        ess.twitter_world_trends()


    def identify_target(self,query,website):

        resp = None

        if website =='facebook': resp = ess.facebook_target_identification(query)
        if website == 'instagram': resp = ess.instagram_target_identification(query)
        if website == 'twitter': resp = ess.twitter_target_identification(query)
        if website == 'linkedin': resp = ess.linkedin_target_identification(query)
        if website == 'reddit': resp = ess.reddit_target_identification(query)
        if website == 'youtube': resp = ess.youtube_target_identification(query)

        return resp

    def create_payload(self,title,description,input_url):

        try:
            resp = ess.create_payload(input_url)
            if(resp):
                if(resp['data']['data']):
                    obj = Ip_Logger(title=title,description=description,input_url=input_url,payload_data=resp['data']['data'])
                    obj.save()
                    publish('payload created successfully', message_type='notification')
                    return resp['data']['data']['payload_url']
                else:
                    publish('payload creation got failed by ESS',message_type='notification')
                    return None
            else:
                publish('responces from ESS is not satisfactory,payload failed', message_type='notification')
                return None

        except Exception as e:
            print(e)
            publish(str(e), message_type='info')
            return None

    def track_logged_payloads(self):
        try:

            loggers = Ip_Logger.objects(is_ip_logged=False)
            for logger in loggers:
                resp = ess.track_ip(code=logger.payload_data['tracking_code'],start_date=str(logger.start_date),end_date=str(datetime.date.today()))
                if(resp):
                    if(len(resp['data']['data'])>0):
                        if(resp['data']['data'][0]):
                            logger.logged_response = resp['data']['data'][0]
                            logger.updated_on = datetime.datetime.utcnow()
                            logger.is_ip_logged = True
                            logger.save()
                            publish('ip tracked for target'+logger.title,message_type='notification')


        except Exception as e:
            print(e)
            publish(str(e), message_type='info')













class Timeline_Manager(object):

    acq = None

    response_posts_list = None

    def __init__(self):
        self.acq = Acquistion_Manager()
        self.response_posts_list = []


    def fetch_posts_for_timeline(self,top=10):
        return Timeline_Posts.get_qualified_posts_with_hard_random(top)



    def get_qualified_response_objects(self):
        pass

    def get_all_unseen_posts(self,qualified_objects):
        pass

    def pick_posts_by_algo(self,qualified_unseen_posts):
        pass

    def update_timeline_posts_by_gtr_id(self,gtr_id):
        try:
            GTR = self.acq.get_gtr_by_id(gtr_id)
            self.update_timeline_posts(gtr=GTR)
        except Exception as e:
            print(e)
            publish(str(e),module_name=__name__,message_type='error')

    def encode_posts_packet(self,target_site,target_type,author,posts,**kwargs):

        posts_list = []

        if(len(posts) > 0):
            if(target_site == 'facebook'):
                if(target_type == 'profile'):
                    for post in posts :
                        try:
                            p_dir=v_dir = ''

                            if len(post.picture_directory) > 0 : p_dir = post.picture_directory[0]['url']
                            if len(post.video_directory) > 0: v_dir = post.video_directory[0]['url']

                            #print(post.picture_directory[0]['url'])
                            temp_dic = {'link':post.post_link,
                                      'text':post.post_text,
                                      'picture':p_dir,
                                      'vedio': v_dir,
                                        'author':author,
                                      'a_url':post.author_url,
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)


                        except Exception as e:
                            print(e)
                    return posts_list

                elif(target_type =='page'):
                    return posts_list

                elif (target_type == 'group'):
                    return posts_list

            elif(target_site == 'instagram'):
                if(target_type == 'profile'):
                    for post in posts :
                        try:



                            temp_dic = {'link':post.display_url,
                                      'text':post.caption,
                                      'picture':'',
                                      'vedio':'',
                                        'author':author,
                                      'a_url':'https://www.instagram.com/'+post.owner_username+'/',
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)


                        except Exception as e:
                            print(e)
                    return posts_list

            elif (target_site == 'twitter'):
                if(target_type=='profile'):
                    for post in posts :
                        try:

                            temp_dic = {'link':post.url,
                                      'text':post.text,
                                      'picture':'',
                                      'vedio': '',
                                        'author':author,
                                      'a_url':'https://www.twitter.com/'+post.username_tweet+'/',
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)

                        except Exception as e:
                            print(e)
                    return posts_list

            elif (target_site == 'reddit'):
                if(target_type=='subreddit'):
                    for post in posts :
                        try:
                            print('..................Reddit ........')
                            temp_dic = {'link':post['post_link'],
                                      'text':post['text'],
                                      'picture':post['media'],
                                      'vedio': '',
                                        'author':author,
                                      'a_url':kwargs['a_url'],
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)

                        except Exception as e:
                            print(e)
                    return posts_list

                elif(target_type=='profile'):
                    for post in posts :
                        try:
                            print('..................Reddit Profile ........')
                            temp_dic = {'link':post['post_link'],
                                      'text':post['text'],
                                      'picture':post['media'],
                                      'vedio': '',
                                        'author':author,
                                      'a_url':kwargs['a_url'],
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)

                        except Exception as e:
                            print(e)
                    return posts_list

            elif (target_site == 'youtube'):
                if(target_type=='channel'):
                    for post in posts :
                        try:
                            print('.................................................................Youtube ..............................................')
                            temp_dic = {'link':post['link'],
                                      'text':post['name'],
                                      'picture':post['thumbnail_directory'],
                                      'vedio': '',
                                        'author':author,
                                      'a_url':kwargs['a_url'],
                                      't_site':target_site,
                                      't_type':target_type,
                                      'seen':False
                                      }



                            posts_list.append(temp_dic)

                        except Exception as e:
                            print(e)
                    return posts_list

    def update_timeline_posts(self,gtr = None):

        sites_to_avoid = ['Linkedin']


        if(gtr is not None):
            try:
                if (not gtr.website.name in sites_to_avoid):
                    obj = self.acq.get_data_response_object_by_gtr_id(gtr.id)
                    if (obj is not None):
                        try:
                            if (gtr.website.name == 'Twitter'):
                                target_site = gtr.website.name
                                target_type = gtr.target_type
                                gtr_id = str(gtr.id)
                                username = obj.name
                                posts = self.encode_posts_packet(target_site.lower(),target_type.lower(),username,obj.tweets)
                                if (len(posts) < 1):
                                    return None

                                tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                    username=username, posts=posts)
                                tl.save()
                                print('timeline updated')


                            elif (gtr.website.name == 'Youtube'):

                                target_site = gtr.website.name

                                target_type = gtr.target_type

                                gtr_id = str(gtr.id)

                                username = obj.overview['name']

                                posts = self.encode_posts_packet(target_site.lower(), target_type.lower(), username,

                                                                 obj.videos['popular'], a_url=obj.overview['url'])

                                print('..................Youtube ........')

                                if (len(posts) < 1):
                                    return None

                                tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,

                                                    username=username, posts=posts)

                                tl.save()

                                print('timeline updated')

                            elif (gtr.website.name == 'Reddit'):

                                target_site = gtr.website.name
                                target_type = gtr.target_type
                                gtr_id = str(gtr.id)

                                print(obj, '.....................Reddit......................')

                                if(target_type.lower() == 'profile'):
                                    username = obj.username
                                else:
                                    username = obj.name

                                posts = self.encode_posts_packet(target_site.lower(), target_type.lower(), username,
                                                                 obj.posts, a_url=obj.url)

                                if (len(posts) < 1):
                                    return None

                                tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                    username=username, posts=posts)
                                tl.save()
                                print('timeline updated')

                            else:

                                target_site = gtr.website.name
                                target_type = gtr.target_type
                                gtr_id = str(gtr.id)
                                username = obj.username
                                posts = self.encode_posts_packet(target_site.lower(),target_type.lower(),username,obj.posts)

                                if (len(posts) < 1):
                                    return None

                                tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                    username=username, posts=posts)
                                tl.save()
                                print('timeline updated')
                        except Exception as e:
                            print('')

                    else:
                        print('given gtr has no response attatched')
            except Exception as e:
                print('')
        else:

            GTRs = Global_Target_Reference.objects()

            for gtr in GTRs:

                try:
                    if (not gtr.website.name in sites_to_avoid):
                        obj = self.acq.get_data_response_object_by_gtr_id(gtr.id)
                        if (obj is not None):
                            try:
                                if (gtr.website.name == 'Twitter'):
                                    target_site = gtr.website.name
                                    target_type = gtr.target_type
                                    gtr_id = str(gtr.id)
                                    username = obj.name
                                    posts = self.encode_posts_packet(target_site.lower(),target_type.lower(),username,obj.tweets)
                                    if(len(posts) < 1):
                                        continue

                                    tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                        username=username, posts=posts)
                                    tl.save()
                                    print('timeline updated')

                                elif (gtr.website.name == 'Youtube'):

                                    target_site = gtr.website.name
                                    target_type = gtr.target_type
                                    gtr_id = str(gtr.id)

                                    username = obj.overview['name']

                                    posts = self.encode_posts_packet(target_site.lower(), target_type.lower(), username,
                                                                     obj.videos['popular'], a_url=obj.overview['url'])
                                    print('..................Youtube ........')
                                    if (len(posts) < 1):
                                        continue

                                    tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                        username=username, posts=posts)
                                    tl.save()
                                    print('timeline updated')

                                elif (gtr.website.name == 'Reddit'):

                                    target_site = gtr.website.name
                                    target_type = gtr.target_type
                                    gtr_id = str(gtr.id)

                                    print(obj,'.....................Reddit......................')

                                    if (target_type.lower() == 'profile'):
                                        username = obj.username
                                    else:
                                        username = obj.name

                                    posts = self.encode_posts_packet(target_site.lower(), target_type.lower(), username,
                                                                     obj.posts, a_url=obj.url)

                                    if (len(posts) < 1):
                                        continue

                                    tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                        username=username, posts=posts)
                                    tl.save()
                                    print('timeline updated')
                                else:

                                    target_site = gtr.website.name
                                    target_type = gtr.target_type
                                    gtr_id = str(gtr.id)
                                    username = obj.username
                                    posts = self.encode_posts_packet(target_site.lower(),target_type.lower(),username,obj.posts)
                                    if (len(posts) < 1):
                                        continue
                                    tl = Timeline_Posts(target_type=target_type, target_site=target_site, gtr_id=gtr_id,
                                                        username=username, posts=posts)
                                    tl.save()
                                    print('timeline updated')
                            except Exception as e:
                                print(e)

                        else:
                            print('given gtr has no response attatched')
                except Exception as e:
                    print('')







































