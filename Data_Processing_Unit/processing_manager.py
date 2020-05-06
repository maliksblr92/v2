from .tasks import fetch_news
import os
#from Public_Data_Acquisition_Unit.models import *
"""
from Data_Processing_Unit.models import News_Fetched_Data,\
    Twitter_Search,\
    Twitter_Person,\
    Search_Tweets,\
    Person_Tweets,\
    Linkedin_Person,\
    Linkedin_Company,\
    Instagram_Posts,\
    Instagram_Person,Facebook_Person,Profile_Analysis_Data
"""
import datetime

from mongoengine import Q

class Processing_Manager(object):

    """
    this processing manager class is to insert,update or delete data in mongoDb and fetch data from
    mongodb. insert data after processing, and also getting data and put multiple filters on the data and then return

    it has following function namming connevention like get , insert , update , and delete
    """


    def __init__(self):
        pass

    def get_all_facebook_objects(self):
        pass
        #return Facebook_Person.objects

    def get_all_latest_updated_targets(self):
        pass

    def get_all_target_responses(self):
        pass
        """
        responses = []

        GTRs = Global_Target_Record.objects.all().order_by('-id')

        for gtr in GTRs:
            obj = Facebook_Person.objects(GTR=gtr.id)
            if(len(obj) <= 0):
                obj = Twitter_Person.objects(GTR=gtr.id)
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

    def get_social_site_instance_by_GTR(self,GTR):
        pass
        """
        obj = Global_Target_Record.objects.get(id=GTR)
        return obj.social_site_reff
        """

    def get_target_instance_by_GTR(self,GTR):
        pass
        """
        try:
            obj = Global_Target_Record.objects.get(id=GTR).facebook_target_person
            return obj
        except :
            try:
                obj = Global_Target_Record.objects.get(id=GTR).twitter_target_person
                return obj
            except:
                try:
                    obj = Global_Target_Record.objects.get(id=GTR).instagram_target_person
                    return obj
                except:
                    try:
                        obj = Global_Target_Record.objects.get(id=GTR).linkedin_target_person
                        return obj
                    except:
                        try:
                            obj = Global_Target_Record.objects.get(id=GTR).linkedin_target_company
                            return obj
                        except:
                            return None
        """

    """
    def get_instagram_instance_by_id(self,instance_id):
        person = Instagram_Person.objects(id=instance_id)
        print(person[0].fullname)
        return person[0]

    def get_facebook_instance_by_id(self,instance_id):
        person = Facebook_Person.objects(id=instance_id)
        return person[0]

    def get_twitter_instance_by_id(self,instance_id):
        person = Twitter_Person.objects(id=instance_id)
        return person[0]

    def get_linkedin_person_instance_by_id(self,instance_id):
        person = Linkedin_Person.objects(id=instance_id)
        return person[0]

    def get_linkedin_company_instance_by_id(self,instance_id):
        person = Linkedin_Company.objects(id=instance_id)
        return person[0]

    def get_all_news_instances(self,news_sites=None,top=10):

        news_response = []

        for site in news_sites:
            news_site = News_Fetched_Data.objects(news_site=site).order_by('-id')[:top]
            if(len(news_site) > 0):
                news_response.append(news_site)

        for resp in news_response:
            for d in resp:
                print(len(news_response),d.news_site,d.title,d.created_on)

        return news_response


    def get_facebook_instances(self):
        person = Facebook_Person.objects()
        return person

    def get_profile_analysis_instance(self,author_account='atifaslam',social_site=None):
        obj = Profile_Analysis_Data.objects(author_account=author_account)
        return obj[0]

    def article_fetched_count_by_category(self):

        addition_factor = 5000

        facebook_count = len(Facebook_Person.objects()) + addition_factor
        twitter_count = len(Twitter_Person.objects()) + addition_factor
        instagram_count = len(Instagram_Person.objects())+ addition_factor
        linkedin_count = len(Linkedin_Person.objects())+ addition_factor
        news_count = len(News_Fetched_Data.objects())+ addition_factor

        print(facebook_count,twitter_count,instagram_count,linkedin_count,news_count)

        result = {'facebook_count':facebook_count,'twitter_count':twitter_count,'instagram_count':instagram_count,'linkedin_count':linkedin_count,'news_count':news_count}

        return result

    def article_fetched_count_by_date(self,days_back = 8):
        addition_factor = 100
        total_count = 0

        response_list = []

        for day in range(0,days_back):

            back_date = (datetime.datetime.utcnow() - datetime.timedelta(days=day))

            for object in Facebook_Person.objects():

                if(back_date.date() == object.created_on.date() ):
                    total_count = total_count + 1

            for object in Twitter_Person.objects():

                if(back_date.date() == object.created_on.date() ):
                    total_count = total_count + 1

            for object in Instagram_Person.objects():

                if(back_date.date() == object.created_on.date() ):
                    total_count = total_count + 1

            for object in Linkedin_Person.objects():

                if(back_date.date() == object.created_on.date() ):
                    total_count = total_count + 1

            for object in News_Fetched_Data.objects():

                if(back_date.date() == object.created_on.date() ):
                    total_count = total_count + 1


            obj_dict = {'date':str(back_date.date()).replace('-',','),'total_count':total_count}
            response_list.append(obj_dict)
            total_count = 0

        print(response_list)
        return response_list

    def ess_usage_average(self):

        facebook = 59
        twitter = 23
        instagram = 11
        linkedin = 5
        other = 2

        response = {'facebook':facebook,'twitter':twitter,'instagram':instagram,'linkedin':linkedin,'other':other}
        return response
"""