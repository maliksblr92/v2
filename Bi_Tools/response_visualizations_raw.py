from Data_Processing_Unit.models import *
from collections import Counter
from math import pi
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components
import collections, functools, operator
from operator import itemgetter
from bokeh.palettes import Spectral6
from datetime import datetime
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure

PLOT_HEIGHT = 350
BACKGROUND_COLOR = 'white'


def get_todays_trends(modelname):
    component = []
    if (modelname.objects):
        current_datetime = datetime.now()
        todays_date = current_datetime.strftime("%x")
        xyoutube = []
        yyoutube = []
        xtwitter = []
        ytwitter = []
        xreddit = []
        yreddit = []
        xgoogle = []
        ygoogle = []
        for each in Trends.objects:
            try:
                creation_datetimes = each['created_on']
                if (creation_datetimes.strftime("%M") != current_datetime.strftime("%M")):
                    creation_date = creation_datetimes.strftime("%x")
                    x = creation_datetimes.strftime("%H")
                    creation_datetime = int(x)
                    if (todays_date == creation_date):
                        trend_type = each['trend_type']
                        top_trends = each['top_Trends']
                        if (trend_type == 'youtube_trends'):
                            lentoptrends_y = len(top_trends)
                            xyoutube.append(creation_datetime)
                            yyoutube.append(lentoptrends_y)
                        if (trend_type == 'twitter_trends'):
                            lentoptrends_t = len(top_trends)
                            xtwitter.append(creation_datetime)
                            ytwitter.append(lentoptrends_t)
                        if (trend_type == 'reddit_trends'):
                            for each in top_trends:
                                trends = each['trends']
                                lentoptrends_r = len(trends)
                                xreddit.append(creation_datetime)
                                yreddit.append(lentoptrends_r)
                        if (trend_type == 'google_trends'):
                            for each in top_trends:
                                lentoptrends_g = len(each)
                                xgoogle.append(creation_datetime)
                                ygoogle.append(lentoptrends_g)

            except:
                a = 5

        colors_list = ['blue', 'yellow', 'red', 'green']
        legends_list = ['Youtube', 'Twitter', "Reddit", "Google"]
        xs = [xyoutube, xtwitter, xreddit, xgoogle]
        ys = [yyoutube, ytwitter, yreddit, ygoogle]
        for a, b, c in zip(legends_list, xs, ys):
            tem = {a: [b, c]}
            component.append(tem)
    return component


def get_top_hashtags(modelname):
    x = {}
    if (modelname.objects):
        popular_hashtag = []
        for each in modelname.objects:
            hashtags = each['popular_hashtag']
            if (len(hashtags) != 0):
                for each in hashtags:
                    popular_hashtag.append(each)
        d = Counter(popular_hashtag)
        x = dict(d)

    return x


def top_trends_visualization(modelname):
    component = []
    if (modelname.objects):
        x = {}
        y = {}
        z = {}
        all_keywords = []
        for each in modelname.objects:
            trend_type = each['trend_type']
            top_trends = each['top_Trends']

            if (trend_type == 'youtube_trends'):
                for each in top_trends:
                    video_name = each['video_name']
                    views = each['views']
                    if (views != ""):
                        x["Youtube: " + str(video_name)] = views
            if (trend_type == 'twitter_trends'):
                for each in top_trends:
                    tag = each['tag']
                    tweet_count = each['tweet_count']
                    if (tweet_count != '' or tweet_count != "null" or tweet_count):
                        if (tweet_count is None) == False:
                            a = tweet_count.replace('k', '000')
                            b = a.replace('K', '000')
                            c = b.replace('M', '000000')
                            if (str(c) != 'N/A'):
                                y["Twitter: " + str(tag)] = c
            if (trend_type == 'reddit_trends'):
                for each in top_trends:
                    trends = each['trends']
                    for each_trend in trends:
                        poster = each_trend['poster']
                        username = poster['username']
                        text = each_trend['text']
                        statistics = each_trend['statistics']
                        score = statistics['score']
                        z["Reddit: " + str(text)] = score

            if (trend_type == 'google_trends'):
                for each in top_trends:
                    for each_trend in each:
                        try:
                            keywords = each_trend['keywords']
                            a = keywords.split(' • ')
                            for each in a:
                                all_keywords.append("Google: " + str(each))
                        except:
                            a = 9
        d = Counter(all_keywords)
        xs = dict(d)
        list_of_counts = []
        youtube = dict(sorted(x.items(), key=itemgetter(1), reverse=True)[:1])
        twitter = dict(sorted(y.items(), key=itemgetter(1), reverse=True)[:1])
        reddit = dict(sorted(z.items(), key=itemgetter(1), reverse=True)[:1])
        google = dict(sorted(xs.items(), key=itemgetter(1), reverse=True)[:1])
        dict4 = {**youtube, **twitter, **reddit, **google}

        fruits = list(dict4.keys())
        count = list(dict4.values())
        counts = []
        for each in count:
            each = str(each)
            e = each.replace(",", "")
            counts.append(int(e))
        for b, c in zip(fruits, counts):
            tem = {b: c}
            component.append(tem)

    return component


def country_trends(modelname):
    component = []
    if (modelname.objects):
        xs = []
        for each in modelname.objects:
            country = each['country']
            if country != "":
                top_trends = each['top_Trends']
                count = len(top_trends)
                x = {country: int(count)}
                xs.append(x)
        result = {}
        for d in xs:
            for k in d.keys():
                result[k] = result.get(k, 0) + d[k]
        fruits = list(result.keys())
        counts = list(result.values())
        for b, c in zip(fruits, counts):
            tem = {b: c}
            component.append(tem)
    return component


def content_categorization_piechart(modelname):
    x = {}
    if (modelname.objects):
        categorization_for_match = []
        for each_target in modelname.objects:
            if (modelname == Twitter_Response_TMS):
                posts = each_target.tweets
            elif (modelname == Facebook_Page_Response_TMS):
                posts = each_target.page_posts
            elif (modelname == Keybase_Response_TMS):
                posts = each_target.data
            else:
                posts = each_target.posts
            if (len(posts) != 0):
                for each_post in posts:
                    try:
                        categorization = each_post['categorization']
                    except:
                        categorization = []
                    if (len(categorization) != 0):
                        # count= count + 1
                        for each_category in categorization:
                            categorization_for_match.append(each_category)
        if (len(categorization_for_match) != 0):
            a = Counter(categorization_for_match).keys()  # equals to list(set(words))
            b = Counter(categorization_for_match).values()  # counts the elements' frequency
            x = dict(zip(a, b))

            # show(p)
    return x


def most_active_users(modelname):
    com = {}
    if (modelname.objects):
        labels = []
        values = []

        for each_target in modelname.objects:
            if (modelname == Twitter_Response_TMS):
                posts = each_target.tweets
                name = each_target.name
            elif (modelname == Facebook_Page_Response_TMS):
                posts = each_target.page_posts
                name = each_target.name
            elif (modelname == Youtube_Response_TMS):
                posts = each_target.posts
                overview = each_target.overview
                name = overview['name']
            elif (modelname == Instagram_Response_TMS):
                posts = each_target.posts
                name = each_target.fullname
            elif (modelname == Reddit_Profile_Response_TMS):
                posts = each_target.posts
                name = each_target.username
            else:
                posts = each_target.posts
                name = each_target.name
            com[name] = len(posts)
        # x = dict(sorted(com.items(), key = itemgetter(1), reverse = True)[:18])

    return com


import numpy as np


# function to get unique values
def unique(list1):
    x = np.array(list1)
    return np.unique(x)


def common_categorization_profiles(modelname):
    data = {}
    if (modelname.objects):
        complete = []
        list_of_users = []
        for each_target in modelname.objects:
            if (modelname == Twitter_Response_TMS):
                posts = each_target.tweets
                name = each_target.name
            elif (modelname == Facebook_Page_Response_TMS):
                posts = each_target.page_posts
                name = each_target.name
            elif (modelname == Youtube_Response_TMS):
                posts = each_target.posts
                overview = each_target.overview
                name = overview['name']
            elif (modelname == Instagram_Response_TMS):
                posts = each_target.posts
                name = each_target.fullname
            elif (modelname == Reddit_Profile_Response_TMS):
                posts = each_target.posts
                name = each_target.username
            else:
                posts = each_target.posts
                name = each_target.name
            if (len(posts) != 0):
                for each_post in posts:
                    categorization = each_post['categorization']
                    if (len(categorization) != 0):
                        for each_category in categorization:
                            name = str(name)
                            if (str(each_category) == 'incitement to an offense'):
                                list_of_users.append(name)
                                complete.append({name: "incitement to an offense"})
                            if (str(each_category) == 'pornography'):
                                list_of_users.append(name)
                                complete.append({name: "pornography"})
                            if (str(each_category) == 'indecent'):
                                list_of_users.append(name)
                                complete.append({name: "indecent"})
                            if (str(each_category) == 'contempt of court'):
                                list_of_users.append(name)
                                complete.append({name: "contempt of court"})
                            if (str(each_category) == 'anti-state'):
                                list_of_users.append(name)
                                complete.append({name: "anti-state"})
        names = unique(list_of_users)
        fruits = []
        incitementtoanoffense = []
        pornographic = []
        indecency = []
        contemptofcourt = []
        antistates = []

        for each_name in names:
            offense = []
            pornography = []
            indecent = []
            contempt = []
            antistate = []
            for each_c in complete:
                try:
                    keyval = each_c[str(each_name)]
                except:
                    keyval = ""
                if (keyval == 'incitement to an offense'):
                    offense.append("incitement to an offense")
                if (keyval == 'pornography'):
                    pornography.append("pornography")
                if (keyval == 'indecent'):
                    indecent.append("indecent")
                if (keyval == 'contempt'):
                    contempt.append("contempt")
                if (keyval == 'anti-state'):
                    antistate.append("anti-state")
            fruits.append(each_name)
            incitementtoanoffense.append(len(offense))
            pornographic.append(len(pornography))
            indecency.append(len(indecent))
            contemptofcourt.append(len(contempt))
            antistates.append(len(antistate))

        output_file("bars.html")

        years = ['incitement to an offense', 'pornography', 'indecent', 'contempt of court', 'anti state']

        data = {'labels': fruits,
                'incitement to an offense': incitementtoanoffense,
                'pornography': pornographic,
                'indecent': indecency,
                'contempt of court': contemptofcourt,
                'anti state': antistates
                }

    return data


def common_sentiments_profiles(modelname):
    data = {}
    if (modelname.objects):
        fruits = []
        positives = []
        negatives = []
        for each_target in modelname.objects:
            if (modelname == Twitter_Response_TMS):
                posts = each_target.sentiments
                name = each_target.name
            elif (modelname == Facebook_Page_Response_TMS):
                posts = each_target.sentiments
                name = each_target.name
            elif (modelname == Instagram_Response_TMS):
                posts = each_target.sentiments
                name = each_target.fullname
            else:
                posts = each_target.sentiments
                name = each_target.name
            if (len(posts) != 0):
                positive = str(posts[0])
                negative = str(posts[1])
                positive = positive.split()
                positive = positive[0]
                negative = negative.split()
                negative = negative[0]
                if name not in fruits:
                    fruits.append(name)
                    positives.append(positive)
                    negatives.append(negative)

        output_file("bars.html")

        years = ['positive', 'negative']

        data = {'label': fruits,
                'positive': positives,
                'negative': negatives
                }

        # show(p)
    return data


def getList(dict):
    return dict.keys()


def getListv(dict):
    return dict.keys()


def profiles_similar_location(modelname):
    x = {}
    if (modelname.objects):
        locations = []
        c_loc = []
        for each_target in modelname.objects:
            name = each_target['name']
            location_details = each_target['location_details']
            if (len(location_details) != 0):
                for each_location_details in location_details:
                    location = each_location_details['location']
                    detail = each_location_details['details']
                    locations.append({"name": name, "location": location, "detail": detail})
            checkedins = each_target['check_ins']
            if (len(checkedins) != 0):
                for each_checkedins in checkedins:
                    checkedin = each_checkedins['name']
                    details = each_checkedins['details']
                    date = details['date']
                    locations.append({"name": name, "location": checkedin, "detail": date})
        for each in locations:
            eachs = each['location']
            c_loc.append(eachs)

        d = Counter(c_loc)
        x = dict(d)

    return x


def keywords_no_barplot(modelname):
    x = {}
    if (modelname.objects):
        queries = []
        for each_target in modelname.objects:
            data = each_target.data
            if (len(data) != 0):
                for each_data in data:
                    query = each_data['query']
                    queries.append(query)
        d = Counter(queries)
        x = dict(d)

    return x


def keywords_results_barplot(modelname):
    queries_record = []
    if (modelname.objects):
        queries = []
        check = []
        for each_target in modelname.objects:
            data = each_target.data
            if (len(data) != 0):
                for each_data in data:
                    query = each_data['query']
                    url = each_data['serp_url']
                    if query not in check:
                        queries.append({"query": query, "url": [url]})
                        check.append(query)
                    else:
                        for each_q in queries:
                            if (each_q['query'] == query):
                                v = each_q['url']
                                v.append(url)
        queries_record = []
        fruits = []
        counts = []
        for each in queries:
            qu = each['query']
            val = each['url']
            val_len = len(val)
            queries_record.append({"query": qu, "count": val_len})

    return queries_record


def keywords_availability(modelname):
    fquq = []
    if (modelname.objects):
        queries = []
        check = []
        for each_target in modelname.objects:
            data = each_target.data
            if (len(data) != 0):
                for each_data in data:
                    query = each_data['query']

                    status = ""
                    statuss = each_data['status']
                    if statuss == "200":
                        status = 'unblocked'
                    elif (statuss == "800"):
                        status = 'blocked'
                    else:
                        print("200 or 800 not found")
                    if status:
                        if query not in check:
                            queries.append({"query": query, "status": [status]})
                            check.append(query)
                        else:
                            for each_q in queries:
                                if (each_q['query'] == query):
                                    v = each_q['status']
                                    v.append(status)
        fruits = []
        queries_blocked = []
        queries_unblocked = []

        for eachq in queries:
            eachquery = eachq['query']
            eachstatus = eachq['status']
            eachstatuscount = Counter(eachstatus)
            eachstatuscount = dict(eachstatuscount)
            try:
                if (eachstatuscount['blocked']):
                    u = 9
            except:
                eachstatuscount['blocked'] = 0
            try:
                if (eachstatuscount['unblocked']):
                    r = 9
            except:
                eachstatuscount['unblocked'] = 0
            fruits.append(eachquery)
            queries_blocked.append(eachstatuscount['blocked'])
            queries_unblocked.append(eachstatuscount['unblocked'])

        for f, q, uq in zip(fruits, queries_blocked, queries_unblocked):
            fq = {'query': f, "blocked": q, "unblocked": uq}
            fquq.append(fq)
    return fquq


def trends_type_freq(modelname):
    x = {}
    if (modelname.objects):
        types = []
        for each in modelname.objects:
            target_type = each['trend_type']
            types.append(target_type)
        d = Counter(types)
        x = dict(d)

    return x


class Instagram_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Instagram_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Instagram_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Instagram_Response_TMS)

    def circle_pack_common_sentiments():
        return common_sentiments_profiles(Instagram_Response_TMS)


class Twitter_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Twitter_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Twitter_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Twitter_Response_TMS)

    def circle_pack_common_sentiments():
        return common_sentiments_profiles(Twitter_Response_TMS)


class Facebook_Profile_Response_TMS_visualization:
    """def profiles_with_similar_location():
        return profiles_similar_location(Facebook_Profile_Response_TMS)"""

    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Profile_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Profile_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Profile_Response_TMS)

    def circle_pack_common_sentiments():
        return common_sentiments_profiles(Facebook_Profile_Response_TMS)


# print(Facebook_Profile_Response_TMS_visualization.most_active_users_chart())
class Facebook_Group_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Group_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Group_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Group_Response_TMS)

    def circle_pack_common_sentiments():
        return common_sentiments_profiles(Facebook_Group_Response_TMS)


class Facebook_Page_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Page_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Page_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Page_Response_TMS)

    def circle_pack_common_sentiments():
        return common_sentiments_profiles(Facebook_Page_Response_TMS)


class Keybase_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Keybase_Response_TMS)

    def no_of_keywords():
        return keywords_no_barplot(Keybase_Response_TMS)

    def keywords_results():
        return keywords_results_barplot(Keybase_Response_TMS)

    def keywords_status_chart():
        return keywords_availability(Keybase_Response_TMS)


class Youtube_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Youtube_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Youtube_Response_TMS)

    """
    def circle_pack_common_categorization():
        return common_categorization_profiles(Youtube_Response_TMS)
    """


class Reddit_Profile_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Reddit_Profile_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Reddit_Profile_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Reddit_Profile_Response_TMS)"""


class Reddit_Subreddit_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Reddit_Subreddit_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Reddit_Subreddit_Response_TMS)

    """   
    def circle_pack_common_categorization():
        return common_categorization_profiles(Reddit_Subreddit_Response_TMS_visualization)"""


class Trends_visualization:
    def trends_type_frequency():
        return trends_type_freq(Trends)

    def country_wise_trends():
        return country_trends(Trends)

    def top_trend_detail():
        return top_trends_visualization(Trends)

    def overall_hashtags():
        return get_top_hashtags(Trends)

    def current_day_trends():
        return get_todays_trends(Trends)
