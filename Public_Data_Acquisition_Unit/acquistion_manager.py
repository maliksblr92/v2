from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.ess_api_controller import Ess_Api_Controller
from OSINT_System_Core.publisher import publish
from Public_Data_Acquisition_Unit.ess_api_controller import *
from Public_Data_Acquisition_Unit.mongo_models import *
from OSINT_System_Core.Data_Sharing import Mongo_Lookup
from Portfolio_Management_System.models import Portfolio_PMS
from bson import ObjectId

import logging

import datetime
ess = Ess_Api_Controller()

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
                if(interval > 0):
                    #print('in here')
                    pt = Periodic_Targets()
                    pt.GTR = gtr
                    pt.target_reff = target
                    pt.re_invoke_time =  datetime.datetime.utcnow() + datetime.timedelta(minutes=interval)
                    pt.save()
                    publish(' {0} is added to periodic targets'.format(target), message_type='info', module_name=__name__)


            self.add_crawling_target(gtr,0)
            return target
        except Exception as e:
            print(e)
            return False

    def add_bulk_targts(self,website_id,target_type_index,prime_argument_list,expired_on,periodic_interval):
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


            for prime_argument in prime_argument_list:
                #gtr = self.get_gtr(website_id, target_type_index)

                if(not self.add_target(website_id,target_type_index,username=prime_argument,expired_on=expired_on,periodic_interval=periodic_interval)):
                    print('unable to add bulk target for '+prime_argument)

            return True

        else:

            publish('unable to add bulk target few arguments are missing ', message_type='alert', module_name=__name__)
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
                response = None #appropriate_ess_method(kwargs['url'],kwargs['ip'],kwargs['domain'],kwargs['pictures'],kwargs['videos'],kwargs['headings'],kwargs['paragraphs'],kwargs['links'],gtr,ctr)
                print(response)
                publish('keybase target added successfully', message_type='info', module_name=__name__)

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



                response = appropriate_ess_method(kwargs['url'],ip,domain,pictures,videos,headings,paragraphs,links,gtr,ctr)
                print(response)
                publish('dynamic crawling target added successfully', message_type='info', module_name=__name__)
            else:

                #ess_api needs basic arguments for adding a target

                username = kwargs['username']
                category = gtr.website.name.lower()
                entity_type = gtr.target_type

                GTR = gtr.id
                CTR = ctr

                print(username,category,entity_type,GTR,CTR)

                response = appropriate_ess_method(username,category,entity_type,GTR,CTR)
                print(response)
                publish('crawling target added successfully', message_type='info', module_name=__name__)




            return True
        except Exception as e:
            publish(str(e), message_type='alert', module_name=__name__)
            return False
        pass

    def get_tasks_kwargs(self,gtr):
        pass

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
                return (Dynamic_Crawling, ess.dynamic_crawling,None)
            elif (gtr.target_type == 'keybase_crawling'):
                return (Keybase_Crawling, None ,None)
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)
        elif (gtr.website.name == 'Reddit'):
            if (gtr.target_type == 'profile'):
                return (Reddit_Profile,ess.add_target,None)
            elif (gtr.target_type == 'subreddit'):
                return (Reddit_Subreddit, ess.add_target ,None)
            else:
                publish('target type not defined',message_type='alert',module_name=__name__)

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

    def fetch_smart_search(self,username,search_site):
        try:
            response = ess.ess_add_smart_serach_target(username,search_site)

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

    def get_fetched_targets(self,top=50):
        responses = []

        ml = Mongo_Lookup()
        GTRs = Global_Target_Reference.objects.all().order_by('-id')

        for gtr in GTRs:


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


    def crawler_internet_connection(self):
        return ess.crawler_internet_connection()

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


    def identify_target(self,query,website):

        resp = None

        if website =='facebook': resp = ess.facebook_target_identification(query)
        if website == 'instagram': resp = ess.instagram_target_identification(query)
        if website == 'twitter': resp = ess.twitter_target_identification(query)
        if website == 'linkedin': resp = ess.linkedin_target_identification(query)
        if website == 'reddit': resp = ess.reddit_target_identification(query)

        return resp




