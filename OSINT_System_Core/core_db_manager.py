"""
from OSINT_System_Core.models import Supported_Socail_Sites,Keyword_Groups,Keywords

from Public_Data_Acquisition_Unit.models import \
    Global_Target_Record,\
    News_Site_Target,\
    AUTHOR_TYPE,\
    NEWS_SITES,\
    PERIODIC_INTERVALS,\
    AUTHOR_TYPE_FACEBOOK,\
    AUTHOR_TYPE_INSTAGRAM,\
    AUTHOR_TYPE_NEWS,\
    AUTHOR_TYPE_TWITTER,\
    SEARCH_TYPE_TWITTER,\
    TWEETS_TYPE_TWITTER,\
    Twitter_Target_Search,\
    Twitter_Target_Person,\
    Instagram_Target_Person,\
    Facebook_Target_Person,Facebook_Target_Search,Facebook_Target_Hashtag,Facebook_Target_Group,Facebook_Target_Page,\
    Linkedin_Target_Person,Linkedin_Target_Company,AUTHOR_TYPE_LINKEDIN

from datetime import datetime,timedelta

class Coredb_Manager(object):
    #class to managed databases basic update and insertion methods

    def __init__(self):
        pass

    def get_social_site_reff(self,sss_id):
        try:
            site_reff = Supported_Socail_Sites.objects.get(id=sss_id)
            return site_reff

        except Exception as e:
            print(e)
            return None

    def insert_global_target_reff(self,sss_id,author_type):
        try:
            sss_reff = self.get_social_site_reff(sss_id)
            if(sss_reff is not None):
                obj = Global_Target_Record.objects.create(social_site_reff=sss_reff,ess_target_reff='null',author_type=author_type)
                obj.save()
                return obj
        except :
            return None

    def get_supported_social_sites_list(self):
        return Supported_Socail_Sites.objects.all().values('id','title')

    def get_choices_list_all(self):
        return (AUTHOR_TYPE,NEWS_SITES,PERIODIC_INTERVALS)

    def get_author_types_all(self):
        return (AUTHOR_TYPE_FACEBOOK,AUTHOR_TYPE_TWITTER,AUTHOR_TYPE_INSTAGRAM,AUTHOR_TYPE_NEWS,PERIODIC_INTERVALS,SEARCH_TYPE_TWITTER,TWEETS_TYPE_TWITTER,AUTHOR_TYPE_LINKEDIN)


    def insert_news_target(self,news_site,top,author_type,expired_on,is_enabled,is_expired,periodic_interval,sss_id= 5):
        try:
            GTR = self.insert_global_target_reff(sss_id,author_type)
            obj = News_Site_Target.objects.create(
                global_target_reff=GTR,
                news_site = news_site,
                top = top,
                expired_on=expired_on,
                is_enabled=is_enabled,
                is_expired=is_expired,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_facebook_person_target(self,author_type,author_id,author_account,author_name,author_url,need_screenshots,expired_on,periodic_interval,sss_id=1):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Facebook_Target_Person.objects.create(
                global_target_reff=GTR,
                author_id = author_id,
                author_account = author_account,
                author_name = author_name,
                author_url = author_url,
                need_screenshots = need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            print('Facebook Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_facebook_page_target(self,author_type,page_id,page_account,page_name,page_url,need_screenshots,expired_on,periodic_interval,sss_id=1):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Facebook_Target_Page.objects.create(
                global_target_reff=GTR,
                page_id = page_id,
                page_account = page_account,
                page_name = page_name,
                page_url = page_url,
                need_screenshots = need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_facebook_group_target(self,author_type,group_id,group_account,group_name,group_url,need_screenshots,expired_on,periodic_interval,sss_id=1):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Facebook_Target_Group.objects.create(
                global_target_reff=GTR,
                group_id=group_id,
                group_account=group_account,
                group_name=group_name,
                group_url=group_url,
                need_screenshots=need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_facebook_hashtag_target(self,author_type,target_keywords,page_url,expired_on,periodic_interval,sss_id=1):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Facebook_Target_Hashtag.objects.create(
                global_target_reff=GTR,
                target_keywords = target_keywords,
                web_page_url = page_url,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_facebook_search_target(self,author_type,target_keywords,page_url,expired_on,periodic_interval,sss_id=1):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Facebook_Target_Search.objects.create(
                global_target_reff=GTR,
                target_keywords = target_keywords,
                web_page_url = page_url,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    #twitter targets start bellow

    def insert_twitter_person_target(self,author_type,author_id,author_account,author_name,author_url,tweets_type,need_screenshots,expired_on,periodic_interval,sss_id=2):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Twitter_Target_Person.objects.create(
                global_target_reff=GTR,
                author_id=author_id,
                author_account=author_account,
                author_name=author_name,
                author_url=author_url,
                tweets_type= tweets_type,
                need_screenshots=need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_twitter_search_target(self,author_type,search_type,phrase,hashtags,location,distance,date,positive_attitude,negative_attitude,expired_on,periodic_interval,sss_id=2):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Twitter_Target_Search.objects.create(
                global_target_reff=GTR,
                hashtags = hashtags,
                phrase= phrase,
                date=date,
                location=location,
                distance=distance,
                search_type=search_type,

                expired_on=timedelta(days=expired_on, hours=10),
                periodic_interval=periodic_interval
            )


            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_twitter_hashtag_target(self,author_type,target_keywords,page_url,expired_on,periodic_interval,sss_id=2):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = News_Site_Target.objects.create(
                global_target_reff=GTR,
                target_keywords=target_keywords,
                web_page_url=page_url,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    #instagram targets start bellow

    def insert_instagram_person_target(self, author_type, author_id, author_account, author_name, author_url,need_screenshots, expired_on,periodic_interval,sss_id=4):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Instagram_Target_Person.objects.create(
                global_target_reff=GTR,
                author_id=author_id,
                author_account=author_account,
                author_name=author_name,
                author_url=author_url,
                need_screenshots=need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )


            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_instagram_search_target(self,author_type,target_keywords,page_url,expired_on,periodic_interval,sss_id=4):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = News_Site_Target.objects.create(
                global_target_reff=GTR,
                target_keywords=target_keywords,
                web_page_url=page_url,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            obj.save()
            print('Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_linkedin_person_target(self, author_type, author_id, author_account, author_name, author_url,need_screenshots, expired_on,periodic_interval,sss_id=6):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Linkedin_Target_Person.objects.create(
                global_target_reff=GTR,
                author_id=author_id,
                author_account=author_account,
                author_name=author_name,
                author_url=author_url,
                need_screenshots=need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            print('Linkedin Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def insert_linkedin_company_target(self, author_type, author_id, author_account, author_name, author_url,need_screenshots, expired_on, periodic_interval, sss_id=6):
        try:
            GTR = self.insert_global_target_reff(sss_id, author_type)
            obj = Linkedin_Target_Company.objects.create(
                global_target_reff=GTR,
                author_id=author_id,
                author_account=author_account,
                author_name=author_name,
                author_url=author_url,
                need_screenshots=need_screenshots,
                expired_on=expired_on,
                periodic_interval=periodic_interval
            )

            print('Linkedin Target inserted successfully')
            return True

        except Exception as e:
            print(e)
            return None

    def get_facebook_targets(self):
        return list(Facebook_Target_Person.objects.values())

    def get_twitter_targets(self):
        return list(Twitter_Target_Person.objects.values())

    def get_instagram_targets(self):
        return list(Instagram_Target_Person.objects.values())

    def get_linkedin_person_targets(self):
        return list(Linkedin_Target_Person.objects.values())

"""