
from Data_Processing_Unit.models import *

"""
bellow are the packages for text processing and predictions 

"""
import re,string, random
import json
import objectpath
import collections
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import os




class News_Data(object):
    def __init__(self):
        pass

    def insert_news_data_to_mongodb(self,response, news_site, top, GTR_ID):
        # save data to mongoDB
        try:

            for headline in response['News']:
                print(headline)
                if (headline['Link'] == ' '):
                    headline['Link'] = 'http://empty.com'
                obj = News_Fetched_Data.objects.create(
                    news_site=news_site,
                    title=headline['HeadLine'],
                    description=headline['Description'],
                    url=headline['Link'],
                    time=headline['Time'],
                    global_target_id=GTR_ID,
                    processed=False,
                    created_on=datetime.datetime.utcnow(),
                )
                obj.save()

            return False
        except Exception as e:
            print(e)
            return False

class Facebook_Data(object):
    def __init__(self):
        pass

    def insert_facebook_person_mongodb(self,GTR, responses, author_account):

        res_overview = responses['overview']
        res_posts = responses['posts']
        res_closeAssociates = responses['closeAssociates']
        res_checkIns = responses['checkIns']
        res_interests = responses['interests']
        # res_complete_profile = responses['completeProfile']

        fp = Facebook_Person()
        fp.created_on = datetime.datetime.utcnow()
        fp.target_update_count = self.facebook_author_identification(author_account)

        fp.GTR = GTR

        if (res_overview is not None and res_posts is not None and res_checkIns is not None and res_closeAssociates is not None and res_interests is not None):
            fp.profile_summary = self.get_summary_of_facebook_profile(res_overview, res_posts, res_checkIns,
                                                                 res_closeAssociates, res_interests)

        if (res_overview is not None):
            res_overview = res_overview['overview']['overview']

            fp.name = res_overview['name']
            fp.author_id = res_overview['id']
            fp.author_account = author_account
            fp.profile_picture_url = res_overview['profile_picture_link']
            fp.work = res_overview['work']
            fp.education = res_overview['education']
            fp.professional_skills = res_overview['professional_skills']
            fp.location_details = res_overview['location_details']
            fp.contact_information = res_overview['contact_information']
            fp.web_links = res_overview['web_links']
            fp.general_information = res_overview['general_information']
            fp.relationship = res_overview['relationship']
            fp.family = res_overview['family']
            fp.life_events_timeline = res_overview['life_events_timeline']

        if (res_posts is not None):
            fp.post_frequency_graph = self.get_graph_of_facebook_profile(res_posts)
            res_posts = res_posts['posts']
            fp.posts = res_posts

        if (res_closeAssociates is not None):
            res_closeAssociates = res_closeAssociates['close_associates']
            fp.close_associates = res_closeAssociates

        if (res_checkIns is not None):
            res_checkIns = res_checkIns['check_ins']
            fp.check_ins = res_checkIns

        if (res_interests is not None):
            res_interests = res_interests['interests']
            fp.interests = res_interests

        # if(res_complete_profile is not None):
        # fp.complete_profile = res_complete_profile['Profile']

        fp.save()
        print('............................MongoDb Updated...........................')

    def facebook_author_identification(self,author_account):
        # this function takes the mongodb table and fetch all of its
        # objects and try to find the match for the given author_name

        fp = Facebook_Person.objects(author_account=author_account)
        if (fp is not None):
            count = len(fp)
            return count + 1
        return 1

    def get_summary_of_facebook_profile(self,dataoverview, facebook_pofile_posts, facebook_profile_checkins,
                                        facebook_profile_close_associates, facebook_profile_interests):
        """ read facebook overview data  """
        jsonnn_overview_tree = objectpath.Tree(dataoverview['overview'])
        Namelist = list(jsonnn_overview_tree.execute('$..name'))
        Name = ' '.join(map(str, Namelist))

        """ read facebook posts data """
        jsonnn_post_tree = objectpath.Tree(facebook_pofile_posts['posts'])
        result_of_posts = list(jsonnn_post_tree.execute('$..posts'))
        timestamp = [sub['time_stamp'] for sub in result_of_posts]

        """   read facebook checkins   """
        data_dict = facebook_profile_checkins["check_ins"]
        checkins_list = data_dict["check_ins"]
        location_checkins = [sub['location'] for sub in checkins_list]

        """   read facebook close associates    """
        closeassociates_dict = facebook_profile_close_associates["close_associates"]
        closeassociates_list = closeassociates_dict["close_associates"]
        names_of_closeassociates = [sub['name'] for sub in closeassociates_list]

        """ read facebook interest              """
        facebook_interests_dict = facebook_profile_interests["interests"]
        facebook_interests_list = facebook_interests_dict["interests"]

        facebook_sports_interests_list = facebook_interests_list["sports"]
        facebook_music_interests_list = facebook_interests_list["music"]
        facebook_films_interests_list = facebook_interests_list["films"]
        facebook_tv_programmes_interests_list = facebook_interests_list["tv_programmes"]
        facebook_books_interests_list = facebook_interests_list["books"]
        facebook_apps_and_games_interests_list = facebook_interests_list["apps_and_games"]
        facebook_likes_interests_list = facebook_interests_list["likes"]
        facebook_events_interests_list = facebook_interests_list["events"]
        facebook_questions_interests_list = facebook_interests_list["questions"]
        facebook_reviews_interests_list = facebook_interests_list["reviews"]
        facebook_notes_interests_list = facebook_interests_list["notes"]

        interest_in_sports = [sub['name'] for sub in facebook_sports_interests_list]
        interest_in_music = [sub['name'] for sub in facebook_music_interests_list]
        interest_in_films = [sub['name'] for sub in facebook_films_interests_list]
        interest_in_tv_programmes = [sub['name'] for sub in facebook_tv_programmes_interests_list]
        interest_in_books = [sub['name'] for sub in facebook_books_interests_list]
        interest_in_apps_and_games = [sub['name'] for sub in facebook_apps_and_games_interests_list]
        interest_in_likes = [sub['name'] for sub in facebook_likes_interests_list]
        interest_in_events = [sub['name'] for sub in facebook_events_interests_list]
        interest_in_questions = [sub['name'] for sub in facebook_questions_interests_list]
        interest_in_reviews = [sub['name'] for sub in facebook_reviews_interests_list]
        interest_in_notes = [sub['name'] for sub in facebook_notes_interests_list]

        """ check number of posts   """

        postdate = []
        for eachdate in timestamp:
            postdate.append(eachdate.split())
        complete = []
        for eachdate in postdate:
            for each in eachdate:
                complete.append(each)
        janpost = complete.count("January")
        febpost = complete.count("February")
        marchpost = complete.count("March")
        aprilpost = complete.count("April")
        maypost = complete.count("May")
        junepost = complete.count("June")
        julypost = complete.count("July")
        augpost = complete.count("August")
        seppost = complete.count("September")
        octpost = complete.count("October")
        novpost = complete.count("November")
        decpost = complete.count("December")

        yaxis = [janpost, febpost, marchpost, aprilpost, maypost, junepost, julypost, augpost, seppost, octpost,
                 novpost,
                 decpost]
        xaxis = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"]
        summary = []
        summary.append(Name)

        """ check user type   """

        totalpostperyear = sum(yaxis)
        averagepost = totalpostperyear / 12
        averagepostpermonth = round(averagepost)
        if averagepostpermonth < 1:
            typeofuser = "a novice"
        elif averagepostpermonth == 1:
            typeofuser = "an intermediate level"
        else:
            typeofuser = " an expert user"
        summary.append(typeofuser)

        """ check month of maximum posts    """
        greaterpostsmonth = xaxis[yaxis.index(max(yaxis))]
        summary.append(greaterpostsmonth)

        """   check the checkins cities   """

        cities = ''
        for i in range(0, len(location_checkins)):

            if i == (len(location_checkins) - 1):
                last_checkin = str(location_checkins[i])
        for each in location_checkins:
            if each != last_checkin:
                each += " and "
            cities += str(each)

        """  check the user close associates  """
        all_close_associates = ''
        for i in range(0, len(names_of_closeassociates)):

            if i == (len(names_of_closeassociates) - 1):
                last_close_associate_in_the_list = str(names_of_closeassociates[i])
        for each_close_associate in names_of_closeassociates:
            if each_close_associate != last_close_associate_in_the_list:
                each_close_associate += " , "
            all_close_associates += str(each_close_associate)

        """ check the interest"""

        def Enquiry(list_of_specific_interest):
            if len(list_of_specific_interest) == 0:
                return 0
            else:
                return 1

        """ intrest in supports   """
        sports_names = ''
        if Enquiry(interest_in_sports):
            for i in range(0, len(interest_in_sports)):
                if i == (len(interest_in_sports) - 1):
                    last_sport_in_the_list = str(interest_in_sports[i])
            for each_sport_name in interest_in_sports:
                if each_sport_name != last_sport_in_the_list:
                    each_sport_name += " , "
                sports_names += str(each_sport_name)
            sport = ". " + Name + " likes " + sports_names + " in the sports. "

        else:
            sport = ""

        """ interest in music  """
        music_names = ''
        if Enquiry(interest_in_music):
            for i in range(0, len(interest_in_music)):
                if i == (len(interest_in_music) - 1):
                    last_music_in_the_list = str(interest_in_music[i])
            for each_music_name in interest_in_music:
                if each_music_name != last_music_in_the_list:
                    each_music_name += " , "
                music_names += str(each_music_name)
            music = Name + "'s music interest is " + music_names + ". "

        else:
            music = ""

        """ interest in films  """
        films_names = ''
        if Enquiry(interest_in_films):
            for i in range(0, len(interest_in_films)):
                if i == (len(interest_in_films) - 1):
                    last_films_in_the_list = str(interest_in_films[i])
            for each_films_name in interest_in_films:
                if each_films_name != last_films_in_the_list:
                    each_films_name += " , "
                films_names += str(each_films_name)
            films = Name + "'s films interest is " + films_names + ". "

        else:
            films = ""

        """ interest in tv_programmes  """
        tv_programmes_names = ''
        if Enquiry(interest_in_tv_programmes):
            for i in range(0, len(interest_in_tv_programmes)):
                if i == (len(interest_in_tv_programmes) - 1):
                    last_tv_programmes_in_the_list = str(interest_in_tv_programmes[i])
            for each_tv_programmes_name in interest_in_tv_programmes:
                if each_tv_programmes_name != last_tv_programmes_in_the_list:
                    each_tv_programmes_name += " , "
                tv_programmes_names += str(each_films_name)
            tv_programmes = Name + "'s tv_programmes interest is " + tv_programmes_names + ". "

        else:
            tv_programmes = ""

        """ interest in books  """
        books_names = ''
        if Enquiry(interest_in_books):
            for i in range(0, len(interest_in_books)):
                if i == (len(interest_in_books) - 1):
                    last_books_in_the_list = str(interest_in_books[i])
            for each_books_name in interest_in_books:
                if each_books_name != last_books_in_the_list:
                    each_books_name += " , "
                books_names += str(each_books_name)
            books = Name + "'s books interest is " + books_names + ". "

        else:
            books = ""

        """ interest in apps_and_games  """
        apps_and_games_names = ''
        if Enquiry(interest_in_apps_and_games):
            for i in range(0, len(interest_in_apps_and_games)):
                if i == (len(interest_in_apps_and_games) - 1):
                    last_apps_and_games_in_the_list = str(interest_in_apps_and_games[i])
            for each_apps_and_games_name in interest_in_apps_and_games:
                if each_apps_and_games_name != last_apps_and_games_in_the_list:
                    each_apps_and_games_name += " , "
                apps_and_games_names += str(each_apps_and_games_name)
            apps_and_games = Name + "'s apps_and_games interest is " + apps_and_games_names + ". "

        else:
            apps_and_games = ""

        """ interest in likes  """
        likes_names = ''
        if Enquiry(interest_in_likes):
            for i in range(0, len(interest_in_likes)):
                if i == (len(interest_in_likes) - 1):
                    last_likes_in_the_list = str(interest_in_likes[i])
            for each_likes_name in interest_in_likes:
                if each_likes_name != last_likes_in_the_list:
                    each_likes_name += " , "
                likes_names += str(each_likes_name)
            likes = Name + "'s likes " + likes_names + ". "

        else:
            likes = ""

        """ interest in events  """
        events_names = ''
        if Enquiry(interest_in_events):
            for i in range(0, len(interest_in_events)):
                if i == (len(interest_in_events) - 1):
                    last_events_in_the_list = str(interest_in_events[i])
            for each_events_name in interest_in_events:
                if each_events_name != last_events_in_the_list:
                    each_events_name += " , "
                events_names += str(each_events_name)
            events = Name + "'s events interest is " + events_names + ". "

        else:
            events = ""

        """ interest in questions  """
        questions_names = ''
        if Enquiry(interest_in_questions):
            for i in range(0, len(interest_in_questions)):
                if i == (len(interest_in_questions) - 1):
                    last_questions_in_the_list = str(interest_in_questions[i])
            for each_questions_name in interest_in_questions:
                if each_questions_name != last_questions_in_the_list:
                    each_questions_name += " , "
                questions_names += str(each_questions_name)
            questions = Name + "'s questions interest is " + questions_names + ". "

        else:
            questions = ""

        """ interest in reviews  """
        reviews_names = ''
        if Enquiry(interest_in_reviews):
            for i in range(0, len(interest_in_reviews)):
                if i == (len(interest_in_reviews) - 1):
                    last_reviews_in_the_list = str(interest_in_reviews[i])
            for each_reviews_name in interest_in_reviews:
                if each_reviews_name != last_reviews_in_the_list:
                    each_reviews_name += " , "
                reviews_names += str(each_reviews_name)
            reviews = Name + "'s reviews interest is " + reviews_names + ". "

        else:
            reviews = ""

        """ interest in notes  """
        notes_names = ''
        if Enquiry(interest_in_notes):
            for i in range(0, len(interest_in_notes)):
                if i == (len(interest_in_notes) - 1):
                    last_notes_in_the_list = str(interest_in_notes[i])
            for each_notes_name in interest_in_notes:
                if each_notes_name != last_notes_in_the_list:
                    each_notes_name += " , "
                notes_names += str(each_notes_name)
            notes = Name + "'s notes interest is " + notes_names + ". "

        else:
            notes = ""

        complete_summary = Name + " is a Facebook user. " + Name + " is " + typeofuser + " user of Facebook. " + Name + " posts " + str(
            totalpostperyear) + " number of posts per year. " + "Mostly, posts have been posted in the month of " + greaterpostsmonth + ". " + Name + " have visited the " + cities + ". " + Name + "'s close associates are " + all_close_associates + sport + music + films + tv_programmes + books + apps_and_games + likes + events + questions + reviews + notes
        return complete_summary

    def get_graph_of_facebook_profile(self,facebook_posts_data):

        jsonnn_tree = objectpath.Tree(facebook_posts_data['posts'])
        all_posts = list(jsonnn_tree.execute('$..posts'))
        timestamp = [sub['time_stamp'] for sub in all_posts]

        postdate = []
        for eachdate in timestamp:
            postdate.append(eachdate.split())
        complete = []
        for eachdate in postdate:
            for each in eachdate:
                complete.append(each)
        print(complete)
        janpost = complete.count("January")
        febpost = complete.count("February")
        marchpost = complete.count("March")
        aprilpost = complete.count("April")
        maypost = complete.count("May")
        junepost = complete.count("June")
        julypost = complete.count("July")
        augpost = complete.count("August")
        seppost = complete.count("September")
        octpost = complete.count("October")
        novpost = complete.count("November")
        decpost = complete.count("December")

        noOfPost = [janpost, febpost, marchpost, aprilpost, maypost, junepost, julypost, augpost, seppost, octpost,
                    novpost, decpost]
        # print(noOfPost)

        yaxis = [janpost, febpost, marchpost, aprilpost, maypost, junepost, julypost, augpost, seppost, octpost,
                 novpost, decpost]
        xaxis = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"]

        # fig = go.Figure([go.Scatter(x=xaxis, y=yaxis)])
        # fig.show()
        return xaxis, yaxis


class Twitter_Data(object):
    def __init__(self):
        pass

    def insert_search_tweets_mongodb(self,GTR, hashtags, phrase, date, distance, response, tweet_type):

        try:
            # first get the data from the given response

            tweet_objects_list = []

            ts = Twitter_Search()
            ts.GTR = GTR
            ts.hashtags = hashtags
            ts.pharse = phrase
            ts.date = date
            ts.distance = distance
            ts.created_on = datetime.datetime.utcnow()

            for tweet in list(response['tweets'].values()):
                # this tweet variable contains one tweeet dictionayr decode and insert it to the db

                username_tweet = tweet['usernameTweet']
                id = tweet['ID']
                text = tweet['text']
                url = tweet['url']
                number_of_retweets = tweet['nbr_retweet']
                number_of_favorite = tweet['nbr_favorite']
                number_of_replies = tweet['nbr_reply']
                date_time = tweet['datetime']
                is_reply = tweet['is_reply']
                is_retweet = tweet['is_retweet']
                user_id = tweet['user_id']

                st = Search_Tweets()
                st.tweet_type = tweet_type
                st.username_tweet = username_tweet
                st.id = id
                st.text = text
                st.url = url
                st.replies_count = number_of_replies
                st.retweeet_count = number_of_retweets
                st.favourite_count = number_of_favorite
                st.datetime_created = date_time
                st.is_retweet = is_retweet
                st.is_reply = is_reply
                st.user_id = user_id

                tweet_objects_list.append(st)

            # print(query_data,tweet_type,username_tweet,id,text,url,number_of_favorite,number_of_replies,number_of_retweets,date_time,is_reply,is_retweet,user_id)
            ts.tweets = tweet_objects_list
            ts.save()

        except Exception as e:
            print(e)

    def insert_person_tweets_mongodb(self,GTR, idn, name, account, response, response_profile_a, tweet_type, url):

        tweet_objects_list = []

        ts = Twitter_Person()

        ts.profile_summary = self.get_twitter_profile_summary(response_profile_a)

        ts.frequent_hashtags = self.get_frequent_hashtags_in_tweets(response_profile_a)
        ts.interests = self.get_author_interests_from_tweets(response_profile_a)

        response_profile = response_profile_a['profile']

        ts.created_on = datetime.datetime.utcnow()
        ts.GTR = GTR
        ts.profile_url = response_profile['profile_image_url']
        ts.author_account = account
        ts.name = response_profile['Full_name']
        ts.biodata = response_profile['bio_data']
        ts.location = response_profile['location']
        ts.website = response_profile['website']

        ts.joined_twitter = response_profile['join_date']
        ts.tweets_count = response_profile['Tweets']
        ts.following_count = response_profile['Following']
        ts.follower_count = response_profile['Followers']
        ts.likes_count = response_profile['Likes']
        ts.moments = response_profile['moments']

        ts.target_update_count = self.twitter_author_identification(account)

        close_associates, tweets_frequency = self.get_graph_of_tweets(response, account)

        ts.close_associates = close_associates
        ts.post_frequency_graph = tweets_frequency

        for tweet in list(response_profile_a['tweets'].values()):
            # this tweet variable contains one tweeet dictionayr decode and insert it to the db

            username_tweet = tweet['usernameTweet']
            id = tweet['ID']
            text = tweet['text']
            url = tweet['url']
            number_of_retweets = tweet['nbr_retweet']
            number_of_favorite = tweet['nbr_favorite']
            number_of_replies = tweet['nbr_reply']
            date_time = tweet['datetime']
            is_reply = tweet['is_reply']
            is_retweet = tweet['is_retweet']
            user_id = tweet['user_id']

            st = Person_Tweets()
            st.tweet_type = tweet_type
            st.username_tweet = username_tweet
            st.id = int(id)
            st.text = text
            st.url = url
            st.replies_count = number_of_replies
            st.retweeet_count = number_of_retweets
            st.favourite_count = number_of_favorite
            st.datetime_created = date_time
            st.is_retweet = is_retweet
            st.is_reply = is_reply
            st.user_id = user_id
            st.sentiment = ''  # get_sentiment_analysis_of_tweets(text)
            print(st.text)

            tweet_objects_list.append(st)

        # print(query_data,tweet_type,username_tweet,id,text,url,number_of_favorite,number_of_replies,number_of_retweets,date_time,is_reply,is_retweet,user_id)
        ts.tweets = tweet_objects_list
        ts.save()

    def insert_twitter_trends_to_mongodb(self,response):
        pass

    def twitter_author_identification(self,author_account):
        # this function takes the mongodb table and fetch all of its
        # objects and try to find the match for the given author_name

        tp = Twitter_Person.objects(author_account=author_account)
        if (tp is not None):
            count = len(tp)
            return count + 1
        return 1

    def get_twitter_profile_summary(self,twitter_profile_data):
        twitter_profile_dict = twitter_profile_data["profile"]

        name_twitter_profile = twitter_profile_dict['Full_name']
        bio_data_twitter_profile = twitter_profile_dict['bio_data']
        join_date_twitter_profile = twitter_profile_dict['join_date']
        tweets_twitter_profile = twitter_profile_dict['Tweets']
        following_twitter_profile = twitter_profile_dict['Following']
        followers_twitter_profile = twitter_profile_dict['Followers']
        likes_twitter_profile = twitter_profile_dict['Likes']
        website_twitter_profile = twitter_profile_dict['website']

        if name_twitter_profile == None:
            twitter_name = ''
        else:
            twitter_name = name_twitter_profile + " is a twitter user. "

        if bio_data_twitter_profile == None:
            twitter_bio_data = ''
        else:
            twitter_bio_data = bio_data_twitter_profile + " is " + name_twitter_profile + "'s personal biography. "

        if website_twitter_profile == None:
            twitter_websites = ''
        else:
            twitter_websites = name_twitter_profile + " have his/her site named as " + website_twitter_profile + ". "

        if join_date_twitter_profile == None:
            twitter_join_date = ''
        else:
            twitter_join_date = name_twitter_profile + " " + join_date_twitter_profile + ". "

        if tweets_twitter_profile == None:
            twitter_tweets = ''
        else:
            twitter_tweets = "He/she have total " + tweets_twitter_profile + ". "

        if following_twitter_profile == None:
            twitter_following = ''
        else:
            twitter_following = "Currently, " + name_twitter_profile + " have " + following_twitter_profile + " ,"

        if followers_twitter_profile == None:
            twitter_followers = ''
        else:
            twitter_followers = followers_twitter_profile + " and "

        if likes_twitter_profile == None:
            twitter_likes = ''
        else:
            twitter_likes = likes_twitter_profile + ". "

        complete_twitter_summary = twitter_name + twitter_bio_data + twitter_websites + twitter_join_date + twitter_tweets + twitter_following + twitter_followers + twitter_likes

        return complete_twitter_summary

    def get_graph_of_tweets(self,twitter_tweets_data, username_of_targeted_account):
        tweets_dictionary = twitter_tweets_data['tweets']

        list_of_tweets_description = list(tweets_dictionary.values())
        username = []
        datetime = []
        for each in list_of_tweets_description:
            username.append(each['usernameTweet'])
            datetime.append(each['datetime'])
            # timestamp = [ sub['usernameTweet'] for sub in each ]

        postdate = []
        complete = []
        unique_names = []

        for eachdate in datetime:
            postdate.append(eachdate.split())

        new = [item[0] for item in postdate]

        for each in new:
            slice_object = slice(4)
            complete.append(each[slice_object])

        # traverse for all elements
        for x in username:
            # check if exists in unique_list or not
            if x not in unique_names:
                unique_names.append(x)

                # print list

        complete_tweet_info = {}
        for each in unique_names:
            count = username.count(each)
            complete_tweet_info[each] = count

        if username_of_targeted_account in complete_tweet_info.keys():
            del complete_tweet_info[username_of_targeted_account]

        c = Counter(complete_tweet_info)
        mc = c.most_common(10)
        close_associates_in_twitter = [x[0] for x in mc]

        close_associates_and_frequencies = [x for x in mc]
        close_associates_frequencies_in_twitter = [x[1] for x in close_associates_and_frequencies]

        return close_associates_in_twitter, close_associates_and_frequencies

    def get_frequent_hashtags_in_tweets(self,twitter_tweets_data):
        tweets_dictionary = twitter_tweets_data['tweets']

        list_of_tweets_description = list(tweets_dictionary.values())
        tweet_text = []
        hashtags_list = []
        single_list_of_hashtags = []
        hashtag_and_frequency = {}
        for each in list_of_tweets_description:
            tweet_text.append(each['text'])
        for each_tweet in tweet_text:
            result_from_tweet = re.findall(r"#(\w+)", each_tweet)
            if len(result_from_tweet) != 0:
                hashtags_list.append(result_from_tweet)
        for each in hashtags_list:
            for eachtag in each:
                single_list_of_hashtags.append(eachtag)
        for each_hashtag in single_list_of_hashtags:
            count = single_list_of_hashtags.count(each_hashtag)
            hashtag_and_frequency[each_hashtag] = count

        c = Counter(hashtag_and_frequency)
        mc = c.most_common(5)
        most_used_hashtags = [x[0] for x in mc]

        return most_used_hashtags

    def get_author_interests_from_tweets(self,twitter_tweets_data):
        def std_codes_list(standard_codes):

            std_codes = []  # empty list which will later contain all the standard op-codes read from the ops.txt file

            with open(standard_codes, 'r') as fp:
                for cnt, line in enumerate(fp):  # reading each op-code in the txt file
                    read_lines = fp.read();
                    read_lines = read_lines.split("\n")
                    std_codes = read_lines
                    std_codes.pop()  # last element is '' blank, so pop it and return the final list

            return std_codes

        base = 'keyset/'
        agencies = base + 'agencies'
        domesticsecurity = base + 'domesticsecurity'
        borderviolence = base + 'borderviolence'
        cybersecurity = base + 'cybersecurity'
        infrastructuresecurity = base + 'infrastructuresecurity'
        nuclear = base + 'nuclear'
        terrorism = base + 'terrorism'
        health = base + 'health'
        WeatherDisasterEmergency = base + 'WeatherDisasterEmergency'
        arts = base + 'arts'
        business = base + 'business'
        education = base + 'education'
        entertainment = base + 'entertainment'
        fashion = base + 'fashion'
        food = base + 'food'
        religion = base + 'religion'
        nature = base + 'nature'
        politics = base + 'politics'
        sports = base + 'sports'
        technology = base + 'technology'
        law = base + 'law'

        agencies = std_codes_list(agencies)
        domesticsecurity = std_codes_list(domesticsecurity)
        borderviolence = std_codes_list(borderviolence)
        cybersecurity = std_codes_list(cybersecurity)
        infrastructuresecurity = std_codes_list(infrastructuresecurity)
        nuclear = std_codes_list(nuclear)
        terrorism = std_codes_list(terrorism)
        health = std_codes_list(health)
        WeatherDisasterEmergency = std_codes_list(WeatherDisasterEmergency)
        arts = std_codes_list(arts)
        business = std_codes_list(business)
        education = std_codes_list(education)
        entertainment = std_codes_list(entertainment)
        fashion = std_codes_list(fashion)
        food = std_codes_list(food)
        law = std_codes_list(law)
        religion = std_codes_list(religion)
        nature = std_codes_list(nature)
        politics = std_codes_list(politics)
        sports = std_codes_list(sports)
        technology = std_codes_list(technology)

        tweets_dictionary = twitter_tweets_data['tweets']
        tweet_text = []

        list_of_tweets_description = list(tweets_dictionary.values())
        for each in list_of_tweets_description:
            tweet_text.append(each['text'])

        def match_op_codes(std_keywords, eachnews, label):

            # split each news into words
            result = eachnews.split()
            totalfrequencyfornews = []
            # print("The total number of words is: "  + str(len(result)))
            # check how many times each keyword occurs in the splitted news
            for each in std_keywords:
                frequencycount = result.count(each)
                # append the all the counted numbers in the list
                totalfrequencyfornews.append(frequencycount)
            # add all of th counted numbers present in the list to form a single frequency for some specific news
            sumfrequency = sum(totalfrequencyfornews)
            freqnews = {}
            # add the single frequency along the news itself in the dictionary
            freqnews[label] = sumfrequency
            # print(k[v.index(max(v))])

            # print(max(freqnews.values(), value=(lambda k: freqnews[k])))
            sumfrequency = 0

            return freqnews

            # print(max(freqnews.iteritems(), key=operator.itemgetter(1))[0])
            # print("The word " + each + " occurs: " + str(result.count(each)))

        count = 0
        for eachnews in tweet_text:
            count = count + 1
        totalNoOfnews = count

        def getpercentage(labelkeywords, label):
            v = []
            k = []
            for eachnews in tweet_text:
                frequency = match_op_codes(labelkeywords, eachnews, label)
                v.append(frequency.values())
                # print(sum(healthfrequency.values()))
                # v.append(healthfrequency.values())
            newvalues = []
            for i in v:
                for j in i:
                    newvalues.append(j)

            # print(newvalues)
            fullkeysvalue = {}
            frequencysum = sum(newvalues)
            # print(frequencysum)

            percentage = (frequencysum / totalNoOfnews) * 100

            fullkeysvalue[label] = percentage
            return fullkeysvalue

        healthpercentage = getpercentage(health, "Health")
        WeatherDisasterEmergencypercentage = getpercentage(WeatherDisasterEmergency, "Weather/Disaster/Emergency")
        agenciespercentage = getpercentage(agencies, "Agencies")
        domesticsecuritypercentage = getpercentage(domesticsecurity, "Domestic Security")
        borderviolencepercentage = getpercentage(borderviolence, "Border Violence")
        cybersecuritypercentage = getpercentage(cybersecurity, "Cyber Security")
        infrastructuresecuritypercentage = getpercentage(infrastructuresecurity, "Infrastructure Security")
        nuclearpercentage = getpercentage(nuclear, "Nuclear")
        terrorismpercentage = getpercentage(terrorism, "Terrorism")
        artspercentage = getpercentage(arts, "Arts")
        businesspercentage = getpercentage(business, "Business")
        educationpercentage = getpercentage(education, "Education")
        entertainmentpercentage = getpercentage(entertainment, "Entertainment")
        fashionpercentage = getpercentage(fashion, "Fashion")
        foodpercentage = getpercentage(food, "Food")
        religionpercentage = getpercentage(religion, "Religious")
        naturepercentage = getpercentage(nature, "Nature")
        politicspercentage = getpercentage(politics, "Politics")
        sportspercentage = getpercentage(sports, "Sports")
        technologypercentage = getpercentage(technology, "Technology")
        lawpercentage = getpercentage(law, "Law")

        dict4 = {**lawpercentage, **religionpercentage, **healthpercentage, **WeatherDisasterEmergencypercentage,
                 **agenciespercentage, **domesticsecuritypercentage, **borderviolencepercentage,
                 **cybersecuritypercentage,
                 **infrastructuresecuritypercentage, **nuclearpercentage, **terrorismpercentage, **politicspercentage,
                 **sportspercentage, **technologypercentage, **artspercentage, **businesspercentage,
                 **educationpercentage,
                 **entertainmentpercentage, **fashionpercentage, **foodpercentage, **naturepercentage}
        # print(dict4)
        c = Counter(dict4)
        mc = c.most_common(3)
        major_interests = [x[0] for x in mc]
        return major_interests

    def get_sentiment_analysis_of_tweets(self,custom_tweet):
        def remove_noise(tweet_tokens, stop_words=()):

            cleaned_tokens = []

            for token, tag in pos_tag(tweet_tokens):
                token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                               '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
                token = re.sub("(@[A-Za-z0-9_]+)", "", token)

                if tag.startswith("NN"):
                    pos = 'n'
                elif tag.startswith('VB'):
                    pos = 'v'
                else:
                    pos = 'a'

                lemmatizer = WordNetLemmatizer()
                token = lemmatizer.lemmatize(token, pos)

                if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                    cleaned_tokens.append(token.lower())
            return cleaned_tokens

        def get_all_words(cleaned_tokens_list):
            for tokens in cleaned_tokens_list:
                for token in tokens:
                    yield token

        def get_tweets_for_model(cleaned_tokens_list):
            for tweet_tokens in cleaned_tokens_list:
                yield dict([token, True] for token in tweet_tokens)

        stop_words = stopwords.words('english')

        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []

        for tokens in positive_tweet_tokens:
            positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        for tokens in negative_tweet_tokens:
            negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        all_pos_words = get_all_words(positive_cleaned_tokens_list)

        positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
        negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

        positive_dataset = [(tweet_dict, "Positive")
                            for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, "Negative")
                            for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)

        train_data = dataset[:7000]

        classifier = NaiveBayesClassifier.train(train_data)

        prediction = []
        custom_tokens = remove_noise(word_tokenize(custom_tweet))
        prediction.append(classifier.classify(dict([token, True] for token in custom_tokens)))
        for tweet_prediction in prediction:
            return tweet_prediction


class Instagram_Data(object):
    def __init__(self):
        pass

    def insert_instagram_profile_to_mongodb(self,GTR_ID, response, author_account):
        posts_object_list = []
        a_data = response['graphql']['user']

        ip = Instagram_Person()
        ip.created_on = datetime.datetime.utcnow()

        ip.target_update_count = self.instagram_author_identification(author_account)

        ip.author_account = author_account
        ip.GTR = GTR_ID
        ip.biography = a_data['biography']
        ip.external_url = a_data['external_url']
        ip.followed_by = a_data['edge_followed_by']['count']
        ip.follow = a_data['edge_follow']['count']
        ip.fullname = a_data['full_name']
        ip.username = a_data['username']
        ip.is_business_account = a_data['is_business_account']
        ip.person_id = a_data['id']
        ip.is_joined_recently = a_data['is_joined_recently']
        ip.is_verified = a_data['is_verified']
        ip.profile_picture_url = a_data['profile_pic_url']
        ip.connected_fb_page = a_data['connected_fb_page']
        ip.profile_summary = self.get_instagram_summary(response)
        print(a_data['edge_owner_to_timeline_media']['edges'])

        for edge in a_data['edge_owner_to_timeline_media']['edges']:
            insta_p = Instagram_Posts()

            insta_p.caption = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            insta_p.comment_count = edge['node']['edge_media_to_comment']['count']
            insta_p.likes_count = edge['node']['edge_liked_by']['count']
            insta_p.display_url = edge['node']['display_url']
            insta_p.owenr_id = edge['node']['owner']['id']
            insta_p.owner_username = edge['node']['owner']['username']

            posts_object_list.append(insta_p)

        ip.posts = posts_object_list
        ip.save()
        print('............................MongoDb Updated...........................')

    def get_instagram_summary(self,instagram_data):
        graphql_data = instagram_data["graphql"]
        user_data = graphql_data["user"]
        full_name_data = user_data["full_name"]
        is_business_account_data = user_data["is_business_account"]
        followersdict = user_data["edge_followed_by"]
        followers = followersdict["count"]

        followsdict = user_data["edge_follow"]
        follows = followsdict["count"]

        is_private_data = user_data["is_private"]
        is_verified_data = user_data["is_verified"]
        username_data = user_data["username"]
        edge_owner_to_timeline_media_data = user_data["edge_owner_to_timeline_media"]
        edges_data = edge_owner_to_timeline_media_data['edges']
        totalposts = edge_owner_to_timeline_media_data['count']

        if is_business_account_data == True:
            account_type = "holds a business instagram account with the username: " + username_data + ". "
        else:
            account_type = "used a regular instagram account with username: " + username_data + ". "

        if is_private_data == True:
            data_type = "is using a private instagram account. "
        else:
            data_type = "prefers regular instagram account rather than private instagram account. "

        if is_verified_data == True:
            verification = " also holds a verified instagram account. "
        else:
            verification = " does not hold a verified instagram account. "

        if not totalposts:
            totalpost = ''
        else:
            totalpost = "Total instagram posts this user have posted are : " + str(totalposts)

        complete_instagram_summary = full_name_data + " is an instagram user who " + account_type + "and have " + str(
            followers) + " number of followers with " + str(
            follows) + " number of following. " + " This user " + data_type + full_name_data + verification + totalpost

        return complete_instagram_summary

    def instagram_author_identification(self,author_account):
        # this function takes the mongodb table and fetch all of its
        # objects and try to find the match for the given author_name

        ips = Instagram_Person.objects(author_account=author_account)
        if (ips is not None):
            count = len(ips)
            return count + 1
        return 1

class Linked_In_Data(object):
    def __init__(self):
        pass

    def insert_linkedin_company_to_mongodb(self,GTR, response, author_account):

        if (response is not None):
            data = response['Profile']['overview']

            lc = Linkedin_Company()

            lc.created_on = datetime.datetime.utcnow()
            lc.author_account = author_account
            lc.GTR = GTR
            lc.description = data['description']
            lc.name = data['name']
            lc.company_size = data['company_size']
            lc.website = data['website']
            lc.industry = data['industry']
            lc.headquarters = data['headquarters']
            lc.type = data['type']
            lc.founded = data['founded']
            lc.specialties = data['specialties']
            lc.number_of_employees = data['num_employees']
            lc.image_url = data['image']

            lc.target_update_count = self.linkedin_company_identification(author_account)

            if (response['Profile']['jobs'] is not None):
                lc.jobs = dict(response['Profile']['jobs'])
            else:
                lc.jobs = {}

            lc.save()

    def insert_linkedin_person_to_mongodb(self,GTR, response, author_account):

        if (response is not None):
            data = response['Profile']['personal_info']

            lp = Linkedin_Person()  # linkdin person mongo object

            lp.created_on = datetime.datetime.utcnow()
            lp.author_account = author_account
            lp.GTR = GTR
            lp.name = data['name']
            lp.headline = data['headline']
            lp.company = data['company']
            lp.school = data['school']
            lp.location = data['location']
            lp.summary = data['summary']
            lp.profile_summary = self.get_linkedin_person_profile_summary(response)
            lp.image_url = data['image']
            lp.followers = data['followers']
            lp.email = data['email']
            lp.phone = data['phone']
            lp.connected = data['connected']
            lp.websites = data['websites']
            lp.current_company_link = data['current_company_link']

            lp.target_update_count = self.linkedin_person_identification(author_account)
            lp.experience = response['Profile']['experiences']

            lp.save()

    def linkedin_person_identification(self,author_account):
        # this function takes the mongodb table and fetch all of its
        # objects and try to find the match for the given author_name

        tp = Linkedin_Person.objects(author_account=author_account)
        if (tp is not None):
            count = len(tp)
            return count + 1
        return 1

    def linkedin_company_identification(self,author_account):
        # this function takes the mongodb table and fetch all of its
        # objects and try to find the match for the given author_name

        tp = Linkedin_Company.objects(author_account=author_account)
        if (tp is not None):
            count = len(tp)
            return count + 1
        return 1

    def get_linkedin_person_profile_summary(self,linkenin_data):
        linkenin_profile_data = linkenin_data["Profile"]
        linkenin_interests_data = linkenin_profile_data["interests"]
        linkenin_skills_data = linkenin_profile_data["skills"]

        linkenin_profile_dict = linkenin_profile_data["personal_info"]

        name_linkenin_profile = linkenin_profile_dict['name']
        company_linkenin_profile = linkenin_profile_dict['company']
        location_linkenin_profile = linkenin_profile_dict['location']
        summary_linkenin_profile = linkenin_profile_dict['summary']
        email_linkenin_profile = linkenin_profile_dict['email']
        phone_linkenin_profile = linkenin_profile_dict['phone']
        followers_linkenin_profile = linkenin_profile_dict['followers']
        # website_linkenin_profile = linkenin_profile_dict['websites']

        if not name_linkenin_profile:
            linkenin_name = ''
        else:
            linkenin_name = name_linkenin_profile + " is a Linkedin user. "

        if company_linkenin_profile == None:
            linkenin_company = ''
        else:
            linkenin_company = company_linkenin_profile + " is the company where this user works. "

        if location_linkenin_profile == None:
            linkenin_location = ''
        else:
            linkenin_location = location_linkenin_profile + " is the location from where " + name_linkenin_profile + " belongs. "

        if summary_linkenin_profile == "":
            linkenin_summary = ''
        else:
            linkenin_summary = " This user profile's summary is " + summary_linkenin_profile + ". "

        if email_linkenin_profile == None:
            linkenin_email = ''
        else:
            linkenin_email = "Email: " + email_linkenin_profile + ". "

        if followers_linkenin_profile == "":
            linkenin_followers = ''
        else:
            linkenin_followers = "This user have " + followers_linkenin_profile + ' have number of followers'

        if phone_linkenin_profile == None:
            linkenin_phone = ''
        else:
            linkenin_phone = ". Contact:" + phone_linkenin_profile + ". "

        if not linkenin_interests_data:
            linkenin_interest = ''
        else:
            notes_names = ''
            for i in range(0, len(linkenin_interests_data)):
                if i == (len(linkenin_interests_data) - 1):
                    last_notes_in_the_list = str(linkenin_interests_data[i])
            for each_notes_name in linkenin_interests_data:
                if each_notes_name != last_notes_in_the_list:
                    each_notes_name += " , "
                notes_names += str(each_notes_name)
            linkenin_interest = " User interests are: " + notes_names + ". "

        """skills """
        skills = []
        for each in linkenin_skills_data:
            skills.append(each['name'])

        if not skills:
            linkenin_skills = ''
        else:
            skills_names = ''
            for i in range(0, len(skills)):
                if i == (len(skills) - 1):
                    last_notes_in_the_list = str(skills[i])
            for each_notes_name in skills:
                if each_notes_name != last_notes_in_the_list:
                    each_notes_name += " , "
                skills_names += str(each_notes_name)
            linkenin_skills = " User skills are: " + skills_names + ". "

        complete_linkedin_summary = linkenin_name + linkenin_company + linkenin_location + linkenin_summary + linkenin_email + linkenin_followers + linkenin_phone + linkenin_interest + linkenin_skills

        return complete_linkedin_summary

