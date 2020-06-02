from Data_Processing_Unit.models import *
from collections import Counter
from math import pi
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components


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

        p = figure(title="Pie Chart", toolbar_location=None,)

        p.wedge(x=0, y=1, radius=0.28,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                color='color', legend='claimNumber', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return components(p)
        """
        fig = go.Figure(data=[go.Pie(labels=list(a), values=list(b))])
        fig.show()
        """


def most_active_users(modelname):
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
        labels.append(name)
        values.append(len(posts))
    print(labels)
    print(values)
    return labels, values
    """
    print(labels)
    print(values)
    if(len(labels)!=0) and (len(values)!=0):
            fig =go.Figure(go.Sunburst(
            labels=labels,
            parents=["",    "",  "",  "", "", "",  "",  "",  "" ],
            values=values,))
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

            fig.show()
    """


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
        print(len(posts))
        if (len(posts) != 0):
            for each_post in posts:
                categorization = each_post['categorization']
                print(categorization)
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

        return complete


def profiles_similar_location(modelname):
    locations = []
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
    return locations


class Instagram_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Instagram_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Instagram_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Instagram_Response_TMS)


class Twitter_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Twitter_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Twitter_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Twitter_Response_TMS)


class Facebook_Profile_Response_TMS_visualization:
    def profiles_with_similar_location():
        return profiles_similar_location(Facebook_Profile_Response_TMS)

    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Profile_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Profile_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Profile_Response_TMS)


class Facebook_Group_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Group_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Group_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Group_Response_TMS)


class Facebook_Page_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Facebook_Page_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Facebook_Page_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Facebook_Page_Response_TMS)


class Keybase_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Keybase_Response_TMS)


class Youtube_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Youtube_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Youtube_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Youtube_Response_TMS)


class Reddit_Profile_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Reddit_Profile_Response_TMS)

    def most_active_users_chart():
        return most_active_users(Reddit_Profile_Response_TMS)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Reddit_Profile_Response_TMS)


class Reddit_Subreddit_Response_TMS_visualization:
    def content_categorization_piechart():
        return content_categorization_piechart(Reddit_Subreddit_Response_TMS_visualization)

    def most_active_users_chart():
        return most_active_users(Reddit_Subreddit_Response_TMS_visualization)

    def circle_pack_common_categorization():
        return common_categorization_profiles(Reddit_Subreddit_Response_TMS_visualization)