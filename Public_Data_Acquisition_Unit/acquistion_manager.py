from Public_Data_Acquisition_Unit.mongo_models import *
from Public_Data_Acquisition_Unit.ess_api_controller import Ess_Api_Controller
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

    def add_target(self,website_id,target_type_index,**kwargs):

        try:
            gtr = self.get_gtr(self.get_website_by_id(website_id),target_type_index)
            appropriate_class, _ = self.get_appropriate_method(gtr)
            ac_object = appropriate_class()
            target = ac_object.create(gtr,kwargs)

            if('periodic_interval' in kwargs):
                interval = kwargs['periodic_interval']
                if(interval > 0):
                    #print('in here')
                    Periodic_Targets(gtr,target,datetime.datetime.utcnow() + datetime.timedelta(minutes=interval)).save()

            return True
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
            print('unable to add bulk target few arguments are missing ')
            return False


    def add_periodic_target(self, gtr):

        """
        this is simplified method to add a task to crawler , user only need to pass the gtr of the target rest is been taken care of .
        this method is used by the celery periodic worker to add the periodic task to crawler.
        appropriate function is a function pointer later used to submit a task to ess using a specific function returned by the methond
        :param gtr:
        :return:
        """
        try:
            appropriate_class, appropriate_ess_method = self.get_appropriate_method(gtr)
            kwargs = appropriate_class.objects(GTR=gtr.id)[0].to_mongo()
            print(kwargs)
            """
            user needs to pass this kwargs and gtr to submit a task to ess,
            kwargs is taken from the database and gtr is the only thing which periodic database need to provide
            """
            print(kwargs['username'])
            response = appropriate_ess_method(kwargs['username'])
            print(response)

            return True
        except Exception as e:
            print(e)
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
                return (Facebook_Profile,ess.ess_add_facebook_person_target)
            elif (gtr.target_type == 'page'):
                pass
            elif (gtr.target_type == 'group'):
                pass
            elif (gtr.target_type == 'search'):
                pass
            else:
                print('target type not defined')

        elif (gtr.website.name == 'Twitter'):
            if (gtr.target_type == 'profile'):
                return Twitter_Profile
            elif (gtr.target_type == 'search'):
                pass
            else:
                print('target type not defined')

        elif (gtr.website.name == 'Instagram'):
            if (gtr.target_type == 'profile'):
                pass
            elif (gtr.target_type == 'search'):
                pass
            else:
                print('target type not defined')

        elif (gtr.website.name == 'Linkedin'):
            if (gtr.target_type == 'profile'):
                pass
            elif (gtr.target_type == 'search'):
                pass
            else:
                print('target type not defined')
        else:
            print('website type not defined')

    def get_dataobject_by_gtr(self,gtr):
        appropriate_class,_ = self.get_appropriate_method(gtr)
        # now we have the actual method
        #now find the gtr id in this method to get the object

        dataobject = appropriate_class.objects(GTR=gtr.id).first()
        return dataobject

    def get_dataobjects_by_gtr_list(self,gtr_list):
        object_list = []
        for gtr in gtr_list:
            obj = self.get_dataobject_by_gtr(gtr)
            object_list.append(obj)
        return object_list

    def add_facebook_target(self,gtr,kwargs):
        pass

    def add_twitter_target(self):
        pass

    def get_gtr_by_id(self,gtr_id):
        return Global_Target_Reference.objects(id=gtr_id)[0]

    def get_periodic_target_list(self):
        return Periodic_Targets.objects( )

    def do_invoke_target(self,gtr):
        self.add_periodic_target(gtr)

    def target_polling(self):

        tasks_list = self.get_periodic_target_list()

        for task in tasks_list:
            time_now = datetime.datetime.utcnow()
            invoke_time = task.re_invoke_time

            if (time_now > invoke_time):
                # then invoke the task
                #ap_cls,_ = self.get_appropriate_method(task.GTR)
                #target = ap_cls.objects(GTR=task.GTR.id)[0]
                task.revoke_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=task.target_reff.periodic_interval)
                task.save()
                self.do_invoke_target(task.GTR)
                print('*************************************Task Reinvoked {0}*****************************'.format(task.target_reff.name))

            self.remove_expired_targets(task)
        print('..................................Task Polling Survey Completed..................................')
        pass

    def remove_expired_targets(self,task):
        time_now = datetime.datetime.utcnow()
        expiry_time = task.target_reff.expired_on

        if (time_now > expiry_time):
            task.target_reff.make_me_expire()
            task.delete()
            print('######################################### expired task deleted #####################################')

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
