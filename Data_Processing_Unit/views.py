from django.contrib import messages
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from Data_Processing_Unit import tasks
from django.http import JsonResponse
from Data_Processing_Unit.processing_manager import Processing_Manager
from xhtml2pdf import pisa
# Create your views here.

from io import BytesIO
from Data_Processing_Unit.models import Change_Record

from django.template.loader import get_template
from Public_Data_Acquisition_Unit.ess_api_controller import Ess_Api_Controller
from Public_Data_Acquisition_Unit.ais_api_controller import Ais_Api_Controller
from Public_Data_Acquisition_Unit.acquistion_manager import Acquistion_Manager
from django.template import Context
from django.contrib import messages

p_manager = Processing_Manager()
ess = Ess_Api_Controller()
ais = Ais_Api_Controller()
acq = Acquistion_Manager()

# ahmed imports
import twint
#import nest_asyncio
import asyncio
#import geopy
from geopy import Nominatim



class Main(View):
    def get(self, request):
        return HttpResponse('in data processing unit')


class Target_Response(View):
    def get(self, request):
        responses = p_manager.get_all_target_responses()
        return render(request, 'Data_Processing_Unit/target_response.html', {'responses': responses})


class Facebook_Profile_View(View):
    def get(self, request, *args, **kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        profile_obj = p_manager.get_facebook_instance_by_id(ob_id)
        return render(request, 'Data_Processing_Unit/facebook_profile_view.html', {'person': profile_obj})


class Twitter_Profile_View(View):

    def get(self, request, *args, **kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        profile_obj = p_manager.get_twitter_instance_by_id(ob_id)
        return render(request, 'Data_Processing_Unit/twitter_profile_view.html', {'person': profile_obj})


class Instagram_Profile_View(View):
    def get(self, request, *args, **kwargs):

        ob_id = ObjectId(kwargs['m_id'])

        profile_obj = p_manager.get_instagram_instance_by_id(ob_id)
        analysis_obj = p_manager.get_profile_analysis_instance()

        return render(request, 'Data_Processing_Unit/instagram_profile_view.html', {'person': profile_obj, 'analysis_instance': analysis_obj})


class Linkedin_Profile_Person_View(View):
    def get(self, request, *args, **kwargs):
        ob_id = ObjectId(kwargs['m_id'])
        try:
            profile_obj = p_manager.get_linkedin_person_instance_by_id(ob_id)
            return render(request, 'Data_Processing_Unit/linkedin_profile_person_view.html', {'person': profile_obj})
        except:
            profile_obj = p_manager.get_linkedin_company_instance_by_id(ob_id)
            return render(request, 'Data_Processing_Unit/linkedin_profile_company_view.html', {'person': profile_obj})


class Linkedin_Profile_Company_View(View):
    def get(self, request):
        return render(request, 'Data_Processing_Unit/linkedin_profile_company_view.html', {})


class BigView(View):
    def get(self, request):
        fetched_by_date = p_manager.article_fetched_count_by_date()
        ess_time_usage = p_manager.ess_usage_average()
        return render(request, 'Data_Processing_Unit/big_view.html', {'fetched_by_category': p_manager.article_fetched_count_by_category(), 'fetched_by_date': fetched_by_date, 'ess_time_usage': ess_time_usage})


class Link_Analysis(View):
    def get(self, request):
        return render(request, 'Data_Processing_Unit/link_analysis.html', {})

# ................................................News Response_Views....................................................

class News_Monitoring(View):

    def get(self, request, *args, **kwargs):
        resp = None
        response = p_manager.get_all_news_instances(
            ['ary', 'bbc', 'geo', 'dawn', 'abp', 'ndtv', 'indiatoday', 'zee'])
        return render(request, 'Data_Processing_Unit/news_monitoring.html', {'news_response': response})


# ................................................Twitter_Trend_Views....................................................
class Twitter_Trends_Country(View):

    def get(self, request, *args, **kwargs):
        print(kwargs['country'])
        resp = tasks.fetch_twitter_trends_country(kwargs['country'])
        return JsonResponse(resp, safe=False)

class Twitter_Trends_Worldwide(View):

    def get(self, request, *args, **kwargs):
        resp = tasks.fetch_twitter_trends_worldwide()
        return JsonResponse(resp, safe=False)


# ................................................Reports Management Views....................................................
class Report_Management_View(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'Data_Processing_Unit/reports_management_view.html', {})


class Convert_Html_To_Pdf(View):
    def get(self, request):
        c = Generate_Reports()
        country_trends = tasks.fetch_twitter_trends_country('pakistan')
        world_trends = tasks.fetch_twitter_trends_worldwide()
        news_response = p_manager.get_all_news_instances(
            ['ary', 'bbc', 'abp', 'indiatoday'])
        social_responses = p_manager.get_all_target_responses()
        return render(request, 'Data_Processing_Unit/report_template.html', {'country_trends': country_trends, 'world_trends': world_trends, 'news_response': news_response, 'responses': social_responses})
        # c.render_to_pdf()



class Generate_Reports(object):

    def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


class Response_Changes_View(View):

    def get(self,request):

        resp_changes = []
        changes = Change_Record.objects().order_by('-created_on')
        for change in changes:
            resp_obj = acq.get_dataobject_by_gtr(acq.get_gtr_by_id(change.GTR))
            resp_changes.append({'resp_obj':resp_obj,'ctr':change.CTR,'detected_on':change.created_on})
        return render(request,'Data_Processing_Unit/response_changes_view.html',{'resp_changes':resp_changes})



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Data_Processing_Unit/index.html')

    def post(self, request, *args, **kwargs):
        nationality = request.POST['nationality']
        gender = request.POST['gender']
        age = request.POST['age']
        resp=ess.fake_identitity_generator(nationality,gender,age)
        return render(request, 'Data_Processing_Unit/index.html',{'resp':resp})
        print("nationality == ", nationality)
        print("gender == ", gender)
        print("age == ", age)

        resp = ess.fake_identitity_generator(nationality,gender,age)

        print(resp)
        return redirect('/dpu/index/')


class Index_Darkweb(View):
    def get(self, request, *args, **kwargs):
        resp={}
        return render(request, 'Data_Processing_Unit/index_darkweb.html',{'resp':resp})

    def post(self, request, *args, **kwargs):
        query = request.POST['query']
        resp=ess.dark_web_search(query)
        if len(resp)  == 0:
            print("No response ")
        return render(request, 'Data_Processing_Unit/index_darkweb.html',{'resp':resp})


class Index_Scrapper(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'Data_Processing_Unit/index_scrapper.html')

    def post(self, request, *args, **kwargs):
        form_name = request.POST['form_name']

        if form_name == 'e_market_scrapper_form':
            query = request.POST['query']
            print("form_name    ==   ", form_name)
            print("query  ==  ", query)

        elif form_name == 'daraz_data_scrapper_form':
            query = request.POST['query']
            print("form_name    ==   ", form_name)
            print("query  ==  ", query)
            ess.daraz_data_scraper(query)

        elif form_name == 'google_scholar':
            query = request.POST['query']
            print("form_name    ==   ", form_name)
            print("query  ==  ", query)
            google_scholar_resposne=ess.google_scholar_data_scraper(query)
            return render(request, 'Data_Processing_Unit/index_scrapper.html',{'google_scholar_resposne':google_scholar_resposne})


        elif form_name == 'google_patent':
            query = request.POST['query']
            print("form_name    ==   ", form_name)
            print("query  ==  ", query)
            google_patent_resposne=ess.google_patents_data_scraper(query)
            return render(request, 'Data_Processing_Unit/index_scrapper.html',{'google_patent_resposne':google_patent_resposne})

        return redirect('/dpu/index_scrapper')


class Index_Textprocessing(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'Data_Processing_Unit/index_textprocessing.html')

    def post(self, request, *args, **kwargs):
        task_name = request.POST['task']
        print(task_name)

        if (task_name == 'common_words'):
            text = request.POST['text']
            print("common words form submitted ")
            common_words=ais.text_analytics(text,task_name)
            print(common_words)
            return render(request,'Data_Processing_Unit/index_textprocessing.html',{'common_words':common_words})

        elif (task_name == 'sentiments'):
            text = request.POST['text']
            sentiments=ais.text_analytics(text,task_name)
            print("sentiments form submitted ")
            print(sentiments)
            return render(request,'Data_Processing_Unit/index_textprocessing.html',{'sentiments':sentiments})

       
        elif (task_name == 'most_used_hashtags'):
            text = request.POST['text']
            most_used_hashtags=ais.text_analytics(text,task_name)
            print("most_used_hashtags form submitted ")
            print(most_used_hashtags)
            return render(request,'Data_Processing_Unit/index_textprocessing.html',{'most_used_hashtags':most_used_hashtags})

        elif (task_name == 'wordcloud'):
            text = request.POST['text']
            wordcloud=ais.text_analytics(text,task_name)
            print("wordcloud form submitted ")
            return render(request,'Data_Processing_Unit/index_textprocessing.html',{'wordcloud':wordcloud})

class Twitter(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Data_Processing_Unit/twitter.html')

    def post(self, request, *args, **kwargs):
        search_type = request.POST['search_type']
        
        
        
        
        print(search_type)
        if search_type == 'phrase_near_location':
            location = request.POST['location']
            phrase = request.POST['phrase']
            limit = request.POST['limit']
            radius = request.POST['radius']
            print(phrase, location)
            geolocator = Nominatim()
            location1 = geolocator.geocode(location)
            lat=str(location1.latitude)
            lon=str(location1.longitude)
            rad=str(radius)
            dic=LocationSearchTweets(phrase,limit,lat,lon,rad)
            print(dic)
            if(len(dic) > 0 ):
                messages.success(
                    request, 'Query Executed Successfully --Location Search With Phrase and  Radius ')
                return render(request, 'Data_Processing_Unit/twint_tweets.html', {'tweets_json': dic})
            else:
                messages.error(request, 'Query execution failed')
               
                return redirect('/dpu/twitter')
            return redirect('/dpu/twitter')


        elif search_type == 'near_location_within_miles':
            location = request.POST['location']
            distance = request.POST['distance']
            limit = request.POST['limit']
            geolocator = Nominatim()
            location = geolocator.geocode(location)
            print(location.latitude, location.longitude)
            asyncio.set_event_loop(asyncio.new_event_loop())
            c = twint.Config()
            c.Limit =limit
            lat=str(location.latitude)
            long=str(location.longitude)
            dist=str(distance)
            c.Geo=""+lat+","+long+","+dist+"km"
            # c.Output = False
            c.Store_object = True
            c.Images = True
           
            twint.output.clean_lists()
            twint.run.Search(c)
            tweets = twint.output.tweets_list
            dic = []
            id=[]
            id_str=[]
            conversation_id=[]
            datetime=[]
            datestamp=[]
            timestamp=[]
            user_id=[]
            user_id_str=[]
            username=[]
            name=[]
            place=[]
            timezone=[]
            img=[]
            mentions=[]
            urls=[]
            photos=[]
            video=[]
            text=[]
            hashtags=[]
            cashtags=[]
            replies_count=[]
            retweets_count=[]
            likes_count=[]
            link=[]
            user_rt_id=[]
            retweet=[]
            retweet_id=[]
            retweet_date=[]
            quote_url=[]
            near=[]
            geo=[]
            source=[]
            reply_to=[]
            for tweet in tweets:
                
                id.append(tweet.id)
                id_str.append(tweet.id_str)
                conversation_id.append(tweet.conversation_id)
                datetime.append(tweet.datetime)
                datestamp.append(tweet.datestamp)
                timestamp.append(tweet.timestamp)
                user_id.append(tweet.user_id)
                user_id_str.append(tweet.user_id_str)
                username.append(tweet.username)
                name.append(tweet.name)
                place.append(tweet.place)
                timezone.append(tweet.timezone)
                mentions.append(tweet.mentions)
                urls.append(tweet.urls)
                photos.append(tweet.photos)
                video.append(tweet.video)
                text.append(tweet.tweet)
                hashtags.append(tweet.hashtags)
                cashtags.append(tweet.cashtags)
                replies_count.append(tweet.replies_count)
                retweets_count.append(tweet.retweets_count)
                likes_count.append(tweet.likes_count)
                link.append(tweet.link)
                user_rt_id.append(tweet.user_rt_id)
                retweet.append(tweet.retweet)
                retweet_id.append(tweet.retweet_id)
                retweet_date.append(tweet.retweet_date)
                quote_url.append(tweet.quote_url)
                near.append(tweet.near)
                geo.append(tweet.geo)
                source.append(tweet.source)
                reply_to.append(tweet.reply_to)
            
            for item in zip(id,id_str,conversation_id,datetime,
                datestamp,timestamp,user_id,user_id_str,username
                ,name,place,timezone,mentions,urls,photos,
                 video,text,hashtags,cashtags,replies_count,likes_count,retweets_count,link
               ,user_rt_id,retweet,retweet_id,retweet_date,quote_url,near,geo,
                source,reply_to
               ):

                dic.append({
            'id':item[0],
            'id_str':item[1],
            'conversation_id':item[2],
            'datetime':item[3],
            'datestamp':item[4],
            'timestamp':item[5],
            'user_id':item[6],
            'user_id_str':item[7],
            'username':item[8],
            'name':item[9],
            'place':item[10],
            'timezone':item[11],
            'mentions':item[12],
            'urls':item[13],
            'photos':item[14],
            'video':item[15],
            'text':item[16],
            'hashtags':item[17],
            'cashtags':item[18],
            'replies_count':item[19],
            'likes_count':item[20],
            'retweets_count':item[21],
            'link':item[22],
            'user_rt_id':item[23],
            'retweet':item[24],
            'retweet_id':item[25],
            'retweet_date':item[26],
            'quote_url':item[27],
            'near':item[28],
            'geo':item[29],
            'source':item[30],
            'reply_to':item[31],
                })
            print(dic)
            if(len(dic) > 0 ):
                messages.success(
                    request, 'Query Executed Successfully --Location Search With Radius ')
                return render(request, 'Data_Processing_Unit/twint_tweets.html', {'tweets_json': dic})
            else:
                messages.error(request, 'Query execution failed')
               
                return redirect('/dpu/twitter')
            
            
            
            
            
            
            
            
            

        elif search_type == 'sentiments_search':
            sentiment = request.POST['sentiment']
            phrase = request.POST['phrase']
            lower_letter_phrase=phrase.lower()
            print(sentiment, phrase)
            if(sentiment == 'positive'):
                tweets_json = ess.tweets_positive(phrase)
                if(len(tweets_json) > 0):
                    messages.success(
                        request, 'Query executed successfully   --Positive Tweets ')
                    print(
                        "=======================ESS REPLY=========================\n", tweets_json)
                    return render(request, 'Data_Processing_Unit/tweets.html', {'tweets_json': tweets_json})
                else:
                    messages.error(request, 'Query execution failed')
                    print(
                        "=======================ESS REPLY=========================\n", tweets_json)
                    return redirect('/dpu/twitter')
            else:
                tweets_json = ess.tweets_negative(phrase)
                print("printing negitive tweets ");
                length=len(tweets_json)
                if(len(tweets_json) > 0):
                    messages.success(request, 'Query executed successfully --Negitive Tweets')
                    print("=======================ESS REPLY=========================\n", tweets_json)
                    return render(request, 'Data_Processing_Unit/sentiment_tweets.html', {'tweets_json': tweets_json})

                else:
                    messages.error(request, 'Query execution failed')
                    print(
                        "=======================ESS REPLY=========================\n", tweets_json)
                    return redirect('/dpu/twitter')
                
                
                
                
                
                
                
                
                
                

        elif search_type == 'phrase_search':
            phrase = request.POST['phrase']
            limit = request.POST['limit']
            print(phrase)
            tweets_json=[]
            # tweets_json = ess.tweets(phrase)
            asyncio.set_event_loop(asyncio.new_event_loop())
            c = twint.Config()
            c.Limit =limit
            c.Search = ""+phrase
            c.Images = True
            # c.Output = False
            c.Store_object = True
            dic = []
            id=[]
            id_str=[]
            conversation_id=[]
            datetime=[]
            datestamp=[]
            timestamp=[]
            user_id=[]
            user_id_str=[]
            username=[]
            name=[]
            place=[]
            timezone=[]
            img=[]
            mentions=[]
            urls=[]
            photos=[]
            video=[]
            text=[]
            hashtags=[]
            cashtags=[]
            replies_count=[]
            retweets_count=[]
            likes_count=[]
            link=[]
            user_rt_id=[]
            retweet=[]
            retweet_id=[]
            retweet_date=[]
            quote_url=[]
            near=[]
            geo=[]
            source=[]
            reply_to=[]
            twint.output.clean_lists()
            twint.run.Search(c)
            tweets = twint.output.tweets_list
            for tweet in tweets:
            
                id.append(tweet.id)
                id_str.append(tweet.id_str)
                conversation_id.append(tweet.conversation_id)
                datetime.append(tweet.datetime)
                datestamp.append(tweet.datestamp)
                timestamp.append(tweet.timestamp)
                user_id.append(tweet.user_id)
                user_id_str.append(tweet.user_id_str)
                username.append(tweet.username)
                name.append(tweet.name)
                place.append(tweet.place)
                timezone.append(tweet.timezone)
                mentions.append(tweet.mentions)
                urls.append(tweet.urls)
                photos.append(tweet.photos)
                video.append(tweet.video)
                text.append(tweet.tweet)
                hashtags.append(tweet.hashtags)
                cashtags.append(tweet.cashtags)
                replies_count.append(tweet.replies_count)
                retweets_count.append(tweet.retweets_count)
                likes_count.append(tweet.likes_count)
                link.append(tweet.link)
                user_rt_id.append(tweet.user_rt_id)
                retweet.append(tweet.retweet)
                retweet_id.append(tweet.retweet_id)
                retweet_date.append(tweet.retweet_date)
                quote_url.append(tweet.quote_url)
                near.append(tweet.near)
                geo.append(tweet.geo)
                source.append(tweet.source)
                reply_to.append(tweet.reply_to)
            
            for item in zip(id,id_str,conversation_id,datetime,
                datestamp,timestamp,user_id,user_id_str,username
                ,name,place,timezone,mentions,urls,photos,
                 video,text,hashtags,cashtags,replies_count,likes_count,retweets_count,link
               ,user_rt_id,retweet,retweet_id,retweet_date,quote_url,near,geo,
                source,reply_to
               ):

                dic.append({
            'id':item[0],
            'id_str':item[1],
            'conversation_id':item[2],
            'datetime':item[3],
            'datestamp':item[4],
            'timestamp':item[5],
            'user_id':item[6],
            'user_id_str':item[7],
            'username':item[8],
            'name':item[9],
            'place':item[10],
            'timezone':item[11],
            'mentions':item[12],
            'urls':item[13],
            'photos':item[14],
            'video':item[15],
            'text':item[16],
            'hashtags':item[17],
            'cashtags':item[18],
            'replies_count':item[19],
            'likes_count':item[20],
            'retweets_count':item[21],
            'link':item[22],
            'user_rt_id':item[23],
            'retweet':item[24],
            'retweet_id':item[25],
            'retweet_date':item[26],
            'quote_url':item[27],
            'near':item[28],
            'geo':item[29],
            'source':item[30],
            'reply_to':item[31],
                })
            print(dic)
            if(len(dic) > 0 ):
                messages.success(
                      request, 'Query Executed Successfully --Phrase Search ')
                print(
                    "=======================ESS REPLY=========================\n", tweets_json)
                return render(request, 'Data_Processing_Unit/twint_tweets.html', {'tweets_json': dic})
            else:
                messages.error(request, 'Query execution failed')
                print(
                    "=======================ESS REPLY=========================\n", tweets_json)
                return redirect('/dpu/twitter')
            
            
            
            
            
            
            
            


class Tweets(View):
    def get(self, request, *args, **kwargs):
         tweets_json={}
         return render(request, 'Data_Processing_Unit/tweets.html', {'tweets_json': tweets_json})



class Get_Hashtag_Tweets(View):
    def get(self,request,*args,**kwargs):
            phrase = kwargs['hashtag_name']
            print(phrase)
            tweets_json=[]
            asyncio.set_event_loop(asyncio.new_event_loop())
            c = twint.Config()
            c.Limit =20
            c.Search = ""+phrase
            c.Images = True
            # c.Output = False
            c.Store_object = True
            dic = []
            id=[]
            id_str=[]
            conversation_id=[]
            datetime=[]
            datestamp=[]
            timestamp=[]
            user_id=[]
            user_id_str=[]
            username=[]
            name=[]
            place=[]
            timezone=[]
            img=[]
            mentions=[]
            urls=[]
            photos=[]
            video=[]
            text=[]
            hashtags=[]
            cashtags=[]
            replies_count=[]
            retweets_count=[]
            likes_count=[]
            link=[]
            user_rt_id=[]
            retweet=[]
            retweet_id=[]
            retweet_date=[]
            quote_url=[]
            near=[]
            geo=[]
            source=[]
            reply_to=[]
            twint.output.clean_lists()
            twint.run.Search(c)
            tweets = twint.output.tweets_list
            for tweet in tweets:
            
                id.append(tweet.id)
                id_str.append(tweet.id_str)
                conversation_id.append(tweet.conversation_id)
                datetime.append(tweet.datetime)
                datestamp.append(tweet.datestamp)
                timestamp.append(tweet.timestamp)
                user_id.append(tweet.user_id)
                user_id_str.append(tweet.user_id_str)
                username.append(tweet.username)
                name.append(tweet.name)
                place.append(tweet.place)
                timezone.append(tweet.timezone)
                mentions.append(tweet.mentions)
                urls.append(tweet.urls)
                photos.append(tweet.photos)
                video.append(tweet.video)
                text.append(tweet.tweet)
                hashtags.append(tweet.hashtags)
                cashtags.append(tweet.cashtags)
                replies_count.append(tweet.replies_count)
                retweets_count.append(tweet.retweets_count)
                likes_count.append(tweet.likes_count)
                link.append(tweet.link)
                user_rt_id.append(tweet.user_rt_id)
                retweet.append(tweet.retweet)
                retweet_id.append(tweet.retweet_id)
                retweet_date.append(tweet.retweet_date)
                quote_url.append(tweet.quote_url)
                near.append(tweet.near)
                geo.append(tweet.geo)
                source.append(tweet.source)
                reply_to.append(tweet.reply_to)
            
            for item in zip(id,id_str,conversation_id,datetime,
                datestamp,timestamp,user_id,user_id_str,username
                ,name,place,timezone,mentions,urls,photos,
                 video,text,hashtags,cashtags,replies_count,likes_count,retweets_count,link
               ,user_rt_id,retweet,retweet_id,retweet_date,quote_url,near,geo,
                source,reply_to
               ):

                dic.append({
            'id':item[0],
            'id_str':item[1],
            'conversation_id':item[2],
            'datetime':item[3],
            'datestamp':item[4],
            'timestamp':item[5],
            'user_id':item[6],
            'user_id_str':item[7],
            'username':item[8],
            'name':item[9],
            'place':item[10],
            'timezone':item[11],
            'mentions':item[12],
            'urls':item[13],
            'photos':item[14],
            'video':item[15],
            'text':item[16],
            'hashtags':item[17],
            'cashtags':item[18],
            'replies_count':item[19],
            'likes_count':item[20],
            'retweets_count':item[21],
            'link':item[22],
            'user_rt_id':item[23],
            'retweet':item[24],
            'retweet_id':item[25],
            'retweet_date':item[26],
            'quote_url':item[27],
            'near':item[28],
            'geo':item[29],
            'source':item[30],
            'reply_to':item[31],
                })
            # print(dic)
            # if(len(dic) > 0 ):
            #     messages.success(
            #           request, 'Query Executed Successfully --Phrase Search ')
            return render(request,'Data_Processing_Unit/twint_tweets.html', {'tweets_json': dic})
        
        
class Ip_Tools(View):
    def get(self,request,*args,**kwargs):
        return render(request,'Data_Processing_Unit/ip_tools.html')
    
    def post(self,request,*args,**kwargs):
        query_type=request.POST['query_type']
        if query_type=='image_reverse_lookup':
            print("Query Type "+query_type)
            url=request.POST.get('url',None)
            image=request.FILES.get('image[]',None)
            print(url)
            #print(image)
            if(image == '' or image == None):
                resp = ess.image_reverse_lookup(image=None, url=url)
            else:
                resp = ess.image_reverse_lookup(image=image, url=None)

            print(resp)

        elif query_type=='ip_shortend':
            print("Query Type "+query_type)

            title = request.POST['title']
            description = request.POST['description']
            url=request.POST['url']

            print(url)
            resp = acq.create_payload(title,description,url)
            print(resp)

        elif query_type=='ip_tracking':
            code=request.POST['code']
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            print(code,start_date,end_date)

        elif query_type=='domains_ip_info':
            domain=request.POST['domain']
            resp = ess.get_domains_ip_info(domain)
            print(resp)
            if(resp['code'] == 0 ):
                messages.success(request, 'No Response for the given domain ip ')
                return render(request,'Data_Processing_Unit/ip_tools.html',{'query_type':query_type,'response':resp})
            else:
                return render(request,'Data_Processing_Unit/ip_tools.html',{'query_type':query_type,'response':resp})
    

        elif query_type == 'domains_info':
            domain = request.POST['domain']
            resp = ess.get_domains_info(domain)
            print("#####################################################################################")
            print(resp)
            if(resp['code'] == 0 ):
                messages.warning(request, 'No Response for the given domain ip ')
                return render(request,'Data_Processing_Unit/ip_tools.html',{'query_type':query_type,'response':resp})
            else:
                messages.success(request, 'Query Successfull ! Showing response for  '+domain)
                return render(request,'Data_Processing_Unit/ip_tools.html',{'query_type':query_type,'response':resp})


        return render(request,'Data_Processing_Unit/ip_tools.html',{'query_type':query_type,'response':resp})
    
    
def LocationSearchTweets(_phrase,_limit,_lat,_lon,_rad):
    

    # # c.Hide_output = True
    # c.Output = True
    asyncio.set_event_loop(asyncio.new_event_loop())
    c = twint.Config()
    c.Limit =_limit
    c.Geo=""+_lat+","+_lon+","+_rad+"km"
    if _phrase!='':
        c.Search = ""+_phrase
        c.Images = True
    # c.Output = False
    c.Store_object = True
    # print(_tweet_type)
    # if _tweet_type =='both':
    #     c.Images = False
    #     print("image=false")
    # if _tweet_type=='img':
    #     c.Images = True
    #     print("image=true")
    # if _tweet_type=='text':
    #     c.Images = False
    #     print("image=false")
# lists
    id=[]
    id_str=[]
    conversation_id=[]
    datetime=[]
    datestamp=[]
    timestamp=[]
    user_id=[]
    user_id_str=[]
    username=[]
    name=[]
    place=[]
    timezone=[]
    img=[]
    mentions=[]
    urls=[]
    photos=[]
    video=[]
    text=[]
    hashtags=[]
    cashtags=[]
    replies_count=[]
    retweets_count=[]
    likes_count=[]
    link=[]
    user_rt_id=[]
    retweet=[]
    retweet_id=[]
    retweet_date=[]
    quote_url=[]
    near=[]
    geo=[]
    source=[]
    reply_to=[]
# Search starts here
    twint.output.clean_lists()
    twint.run.Search(c)
    tweets = twint.output.tweets_list
    for tweet in tweets:
      id.append(tweet.id)
      id_str.append(tweet.id_str)
      conversation_id.append(tweet.conversation_id)
      datetime.append(tweet.datetime)
      datestamp.append(tweet.datestamp)
      timestamp.append(tweet.timestamp)
      user_id.append(tweet.user_id)
      user_id_str.append(tweet.user_id_str)
      username.append(tweet.username)
      name.append(tweet.name)
      place.append(tweet.place)
      timezone.append(tweet.timezone)
      mentions.append(tweet.mentions)
      urls.append(tweet.urls)
      photos.append(tweet.photos)
      video.append(tweet.video)
      text.append(tweet.tweet)
      hashtags.append(tweet.hashtags)
      cashtags.append(tweet.cashtags)
      replies_count.append(tweet.replies_count)
      retweets_count.append(tweet.retweets_count)
      likes_count.append(tweet.likes_count)
      link.append(tweet.link)
      user_rt_id.append(tweet.user_rt_id)
      retweet.append(tweet.retweet)
      retweet_id.append(tweet.retweet_id)
      retweet_date.append(tweet.retweet_date)
      quote_url.append(tweet.quote_url)
      near.append(tweet.near)
      geo.append(tweet.geo)
      source.append(tweet.source)
      reply_to.append(tweet.reply_to)

    # Construct Dictionary of Tweets
    dic = []
    for item in zip(id,id_str,conversation_id,datetime,
                datestamp,timestamp,user_id,user_id_str,username
                ,name,place,timezone,mentions,urls,photos,
                 video,text,hashtags,cashtags,replies_count,likes_count,retweets_count,link
               ,user_rt_id,retweet,retweet_id,retweet_date,quote_url,near,geo,
                source,reply_to
               ):

        dic.append({
            'id':item[0],
            'id_str':item[1],
            'conversation_id':item[2],
            'datetime':item[3],
            'datestamp':item[4],
            'timestamp':item[5],
            'user_id':item[6],
            'user_id_str':item[7],
            'username':item[8],
            'name':item[9],
            'place':item[10],
            'timezone':item[11],
            'mentions':item[12],
            'urls':item[13],
            'photos':item[14],
            'video':item[15],
            'text':item[16],
            'hashtags':item[17],
            'cashtags':item[18],
            'replies_count':item[19],
            'likes_count':item[20],
            'retweets_count':item[21],
            'link':item[22],
            'user_rt_id':item[23],
            'retweet':item[24],
            'retweet_id':item[25],
            'retweet_date':item[26],
            'quote_url':item[27],
            'near':item[28],
            'geo':item[29],
            'source':item[30],
            'reply_to':item[31],
                })




    return dic