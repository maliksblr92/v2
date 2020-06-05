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

PLOT_HEIGHT = 350
BACKGROUND_COLOR = 'white'


def top_trends_visualization(modelname):
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
    output_file("bar_sorted.html")
    # sorting the bars means sorting the range factors
    sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

    p = figure(x_range=sorted_fruits, title="Most Trending Trend",
               toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.background_fill_color = BACKGROUND_COLOR
    return components(p)


def country_trends(modelname):
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
    output_file("bar_sorted.html")
    # sorting the bars means sorting the range factors
    sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

    p = figure(x_range=sorted_fruits, title="Country wise Trends",
               toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.background_fill_color = BACKGROUND_COLOR

    # show(p)
    return components(p)


def content_categorization_piechart(modelname):
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
        chart_colors = ['#44e5e2', '#e29e44', '#e244db',
                        '#d8e244', '#eeeeee', '#56e244', '#007bff', 'black']

        data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(
            index=str, columns={0: 'value', 'index': 'claimNumber'})
        data['angle'] = data['value'] / sum(x.values()) * 2 * pi
        data['color'] = chart_colors[:len(x)]

        p = figure(plot_height=PLOT_HEIGHT, title="Content Categorization Statistics", toolbar_location=None)

        p.wedge(x=0, y=1, radius=0.28,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                color='color', legend='claimNumber', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        p.background_fill_color = BACKGROUND_COLOR
        # show(p)
        return components(p)
        """
        fig = go.Figure(data=[go.Pie(labels=list(a), values=list(b))])
        fig.show()
        """


def most_active_users(modelname):
    labels = []
    values = []
    com = {}
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
    x = dict(sorted(com.items(), key=itemgetter(1), reverse=True)[:18])
    if (len(x) == 1):
        x[''] = 0
        x[' '] = 0
    if (len(x) == 2):
        x[''] = 0
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x)]
    p = figure(title="Most Active Users", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.background_fill_color = BACKGROUND_COLOR
    return components(p)


def common_categorization_profiles(modelname):
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    complete = []
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
                        if (str(each_category) == 'Neither'):
                            if name not in a:
                                complete.append({"name": name, "category": "Neither"})
                            a.append(name)
                        if (str(each_category) == 'incitement to an offense'):
                            if name not in b:
                                complete.append({"name": name, "category": "incitement to an offense"})
                            b.append(name)
                        if (str(each_category) == 'pornography'):
                            if name not in c:
                                complete.append({"name": name, "category": "pornography"})
                            c.append(name)
                        if (str(each_category) == 'indecent'):
                            if name not in d:
                                complete.append({"name": name, "category": "indecent"})
                            d.append(name)
                        if (str(each_category) == 'contempt of court'):
                            if name not in e:
                                complete.append({"name": name, "category": "contempt of court"})
                            e.append(name)
                        if (str(each_category) == 'anti-state'):
                            if name not in f:
                                complete.append({"name": name, "category": "anti-state"})
                            f.append(name)
        x = []
        y = []
        for each in complete:
            k = each['name']
            v = each['category']
            x.append(k)
            y.append(v)

        output_file("multiple.html")

        p = figure(plot_width=400, plot_height=PLOT_HEIGHT)

        # add both a line and circles on the same plot
        p.line(x, y, line_width=2)
        p.circle(x, y, fill_color="white", size=8)
        p.background_fill_color = BACKGROUND_COLOR
        return complete


def getList(dict):
    return dict.keys()


def getListv(dict):
    return dict.keys()


def profiles_similar_location(modelname):
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
    x = dict(sorted(x.items(), key=itemgetter(1), reverse=True)[:18])

    # print(x)
    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0: 'value',
                                                                                                    'index': 'country'})
    data['angle'] = data['value'] / sum(x.values()) * 2 * pi
    if (len(x) == 1):
        x[''] = 0
        x[' '] = 0
    if (len(x) == 2):
        x[''] = 0
    data['color'] = Category20c[len(x)]

    p = figure(plot_height=PLOT_HEIGHT, title="Most Popular Locations ", toolbar_location=None,
               tools="hover", tooltips="@country: @value")

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='country', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.background_fill_color = BACKGROUND_COLOR
    # show(p)

    return components(p)


profiles_similar_location(Facebook_Profile_Response_TMS)


def keywords_no_barplot(modelname):
    queries = []
    for each_target in modelname.objects:
        data = each_target.data
        if (len(data) != 0):
            for each_data in data:
                query = each_data['query']
                queries.append(query)
    d = Counter(queries)
    x = dict(d)
    x = dict(sorted(x.items(), key=itemgetter(1), reverse=True)[:18])
    # print(x)
    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0: 'value',
                                                                                                    'index': 'country'})
    data['angle'] = data['value'] / sum(x.values()) * 2 * pi
    if (len(x) == 1):
        x[''] = 0
        x[' '] = 0
    if (len(x) == 2):
        x[''] = 0
    data['color'] = Category20c[len(x)]

    p = figure(plot_height=PLOT_HEIGHT, title="Keybase Fetched Results Statistics ", toolbar_location=None,
               tools="hover", tooltips="@country: @value")

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='country', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.background_fill_color = BACKGROUND_COLOR
    # show(p)

    return components(p)


def keywords_results_barplot(modelname):
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
    for each in queries_record:
        fruits.append(each['query'])
        counts.append(each['count'])

    output_file("bar_sorted.html")
    # sorting the bars means sorting the range factors
    sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

    p = figure(x_range=sorted_fruits, plot_height=PLOT_HEIGHT, title="Keybase Content Frequency",
               toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.background_fill_color = BACKGROUND_COLOR
    return components(p)


def keywords_availability(modelname):
    from bokeh.io import output_file, show
    from bokeh.models import ColumnDataSource, FactorRange
    from bokeh.plotting import figure
    output_file("bars.html")
    queries = []
    check = []
    for each_target in modelname.objects:
        data = each_target.data
        if (len(data) != 0):
            for each_data in data:
                query = each_data['query']

                try:
                    statuss = each_data['status']
                    if statuss == 200:
                        status = 'unblocked'
                    else:
                        status = 'blocked'
                except:
                    status = "unblocked"

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
                print("blocked exists")
        except:
            eachstatuscount['blocked'] = 0
        try:
            if (eachstatuscount['unblocked']):
                print("unblocked exists")
        except:
            eachstatuscount['unblocked'] = 0
        fruits.append(eachquery)
        queries_blocked.append(eachstatuscount['blocked'])
        queries_unblocked.append(eachstatuscount['unblocked'])

    from bokeh.io import output_file, show
    from bokeh.models import ColumnDataSource, FactorRange
    from bokeh.plotting import figure

    output_file("bars.html")

    years = ['blocked', 'unblocked']

    data = {'fruits': fruits,
            'blocked': queries_blocked,
            'unblocked': queries_unblocked
            }

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [(fruit, year) for fruit in fruits for year in years]
    counts = sum(zip(data['blocked'], data['unblocked']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), plot_height=PLOT_HEIGHT, title="Keybase Fetched Sites Status",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.background_fill_color = BACKGROUND_COLOR
    return components(p)


def trends_type_freq(modelname):
    types = []
    for each in modelname.objects:
        target_type = each['trend_type']
        types.append(target_type)
    d = Counter(types)
    x = dict(d)
    fruits = list(x.keys())
    counts = list(x.values())
    output_file("bar_sorted.html")
    # sorting the bars means sorting the range factors
    sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

    p = figure(x_range=sorted_fruits, plot_height=PLOT_HEIGHT, title="Trends Frequency",
               toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.background_fill_color = BACKGROUND_COLOR
    return components(p)


class Instagram_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Instagram_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Instagram_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Instagram_Response_TMS)"""


class Twitter_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Twitter_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Twitter_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Twitter_Response_TMS)"""


class Facebook_Profile_Response_TMS_visualization:
    """def profiles_with_similar_location():
        return profiles_similar_location(Facebook_Profile_Response_TMS)"""

    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Profile_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Profile_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Profile_Response_TMS)"""


# print(Facebook_Profile_Response_TMS_visualization.most_active_users_chart())
class Facebook_Group_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Group_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Group_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Group_Response_TMS)"""


class Facebook_Page_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Page_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Page_Response_TMS)

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Page_Response_TMS)"""


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

    """def circle_pack_common_categorization():
        return common_categorization_profiles(Youtube_Response_TMS)"""


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
    # above three working
    def trends_type_frequency():
        return trends_type_freq(Trends)

    def country_wise_trends():
        return country_trends(Trends)

    def top_trend_detail():
        return top_trends_visualization(Trends)