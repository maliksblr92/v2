from django.http import JsonResponse
from django.shortcuts import render
import json
#from dashboard.models import Order
from Public_Data_Acquisition_Unit.mongo_models import *
from Data_Processing_Unit.models import *
from Bi_Tools.mongo_serializer import Mongo_Serializer
from Bi_Tools.visualizations import Visualisation_Mangager
#from Bi_Tools.response_visualizations import *
from Bi_Tools.response_visualizations_raw import *
import json

from bokeh.resources import CDN
from bokeh.layouts import row
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components

from django.core import serializers

from bson import ObjectId

ms = Mongo_Serializer()
vm = Visualisation_Mangager()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def dashboard_with_pivot(request):
    return render(request, 'Bi_Tools/dashboard_with_pivot.html', {})


def pivot_data(request):

    objects_list = Keybase_Response_TMS.objects()
    print(objects_list)

    #data = [{'Title':'Awais','Value':50},{'Title':'Nouman','Value':67}] #JSONEncoder().encode(supported_sites[0].to_mongo()) #serializers.serialize('json', supported_sites)

    data = [{"model": "business_intelligence_tool.order", "pk": 1, "fields": {"product_category": "Books", "payment_method": "Credit Card", "shipping_cost": "59", "unit_price": "39.00"}},
            {"model": "business_intelligence_tool.order", "pk": 2, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "88", "unit_price": "200.00"}},
            {"model": "business_intelligence_tool.order", "pk": 3, "fields": {"product_category": "Table", "payment_method": "Credit Card", "shipping_cost": "75", "unit_price": "259.00"}},
            {"model": "business_intelligence_tool.production", "pk": 1, "fields": {"product_category": "Table", "production_method": "Automatic", "cost": "88","price": "259.00"}}
            ]
    data = ms.keybase_responce_tms_serializer(objects_list)

    data = json.dumps(data)

    return JsonResponse(data, safe=False)



def simple_chart(request):

    data = {
        'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        'datasets': [{
            'label': '# of Votes',
            'data': [12, 19, 3, 5, 2, 3],
            'borderWidth': 1
        },{
            'label': '# of Votes',
            'data': [124, 169, 35, 5, 2, 3],
            'borderWidth': 1
        }]

    }



    script,div = vm.simple_chart()
    print('...............visual sent ..................')
    return render(request, "Bi_Tools/simple_chart.html", {"the_script": script, "the_div": div})

def keybase_visualization(request,content_type):
    dataset_list = []

    #a_script,a_div = Keybase_Response_TMS_visualization.content_categorization_piechart()
    #b_script, b_div = Keybase_Response_TMS_visualization.keywords_results()
    #c_script, c_div = Keybase_Response_TMS_visualization.keywords_status_chart()
    #d_script, d_div = Keybase_Response_TMS_visualization.no_of_keywords()


    print(content_type)
    # content_type = request.GET.get('content_type',None)

    if (content_type == 'keybase'):

        """
            {'pornography': 192, 'Neither': 55, 'indecent': 69, 'sectarian': 1, 'blasphemy': 1}

            [{'query': 'teen porn videos', 'blocked': 29, 'unblocked': 11},
             {'query': 'desi sex', 'blocked': 21, 'unblocked': 19}, {'query': 'Gang Rape Sex', 'blocked': 11, 'unblocked': 29},
             {'query': 'Porn', 'blocked': 27, 'unblocked': 13}, {'query': 'sex video', 'blocked': 32, 'unblocked': 8},
             {'query': 'Nude', 'blocked': 6, 'unblocked': 34}, {'query': 'Sex', 'blocked': 12, 'unblocked': 27},
             {'query': 'Rape', 'blocked': 11, 'unblocked': 27}]

            [{'query': 'teen porn videos', 'count': 40}, {'query': 'desi sex', 'count': 40},
             {'query': 'Gang Rape Sex', 'count': 40}, {'query': 'Porn', 'count': 40}, {'query': 'sex video', 'count': 40},
             {'query': 'Nude', 'count': 40}, {'query': 'Sex', 'count': 39}, {'query': 'Rape', 'count': 38}]

            {'teen porn videos': 40, 'desi sex': 40, 'Gang Rape Sex': 40, 'Porn': 40, 'sex video': 40, 'Nude': 40, 'Sex': 39,
             'Rape': 38}
            """

        try:

            a_chart = Keybase_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Keybase_Response_TMS_visualization.keywords_status_chart()
            c_chart = Keybase_Response_TMS_visualization.keywords_results()
            d_chart = Keybase_Response_TMS_visualization.no_of_keywords()

            # print(Keybase_Response_TMS_visualization.content_categorization_piechart())
            # print(Keybase_Response_TMS_visualization.keywords_status_chart())
            # print(Keybase_Response_TMS_visualization.keywords_results())
            # print(Keybase_Response_TMS_visualization.no_of_keywords())

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            labels = []
            a_dataset = []
            b_dataset = []
            for data in b_chart:
                labels.append(data['query'])
                a_dataset.append(data['blocked'])
                b_dataset.append(data['unblocked'])

            dataset_list.append(
                create_graph_response_keybase(labels, [a_dataset, b_dataset], 'bar', 'fa_chart',
                                              ['Blocked', 'Un Blocked'],
                                              'Blocked and Un Blocked Results'))

            # n0_labels = []
            # a0_dataset = []
            #
            # for data in c_chart:
            #     n0_labels.append(data['query'])
            #     a0_dataset.append(data['count'])

            #dataset_list.append(create_graph_response_keybase(c_chart.keys(), [c_chart.values()], 'bar', 'b_chart', ['Count'],
            #                                                  'Results found on keywords'))

            dataset_list.append(
                create_graph_response_keybase(d_chart.keys(), [d_chart.values()], 'bar', 'fb_chart', ['Count'],
                                              'Results found on keywords'))


        except Exception as e:
            print(e)


        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": 'keybase', 'dataset_list': dataset_list})


    elif (content_type == 'instagram'):

        try:

            a_chart = Instagram_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Instagram_Response_TMS_visualization.most_active_users_chart()
            c_chart = Instagram_Response_TMS_visualization.circle_pack_common_sentiments()
            d_chart = Instagram_Response_TMS_visualization.circle_pack_common_categorization()
            """
            {'Neither': 375, 'indecent': 71, 'contempt of court': 2, 'blasphemy': 2}
    {'فابیہ نزر': 0, 'Atif Aslam': 12, 'Ayesha Omar': 12, 'Maira khan': 12, 'Sajal Ahad Mir': 12, 'Maryam\u200c': 12, 'Amirtha-Thendral': 12, 'Amir Jaberi امیر جابری': 12, 'Amira Riaa': 12, '♔G𝟏 𝙼𝙾𝙷𝙰𝙼𝙼𝙴𝙳 𝙰𝚂𝙻𝙰𝙼': 12, 'ARTISTIK✨': 12, 'Melia ᵔᴥᵔ': 12, '📱Andrew™📡': 0, '🇵🇰x🇧🇩': 1, 'NASSO❤': 0, 'Cme 🌎': 12, 'manish rajawat': 0, 'DP 🖕': 0, 'cutie pie': 0, 'Ummeh Ammara': 0, 'Umair shafqat Shafqat umair': 1, 'Naveed Butt': 0, 'Rabia ke liye': 0, 'zubi_949': 0, '': 0, 'Gul e laila': 0, 'Eesha Tariq': 0, 'Maliha Khan': 1, 'soniya': 6, 'Hasnain Kanch': 0, 'Daniyal Ali Khan': 12, 'Mariam': 0, 'Zara Asif✨': 0, 'Fatima Tahira': 10, 'ABC': 0, '𝓭𝔂𝓮𝓾𝓷✨': 4, 'Anastasia Poetrii': 0, 'Rain': 0, '👜kebutuhan wanita': 6, '∆π': 0, 'egisaputra': 11, 'frenius latano': 10, 'bellasafitri': 0, 'yuniar firdausiana risky p.n': 3, '𝒟ℯ𝓁𝓁𝒶 𝓂𝒶𝓊𝓁𝒾𝓎𝒶𝓃𝒶🥀': 7, 'carissa syakillah Chandravia': 4, 'Joao vitor Guimaraes': 0, '[ E_C Team ]': 0, 'Muhamad Ramdany': 12, 'BERUANG.BIROE': 0, 'Rahma': 2, 'InfoAkunPenipu.Idn': 12, 'MAGGOT STORE BEKASI': 12, 'Meerajee  Official Team': 12, 'Bilal Ashraf': 12, 'Alastair (Ali-A)': 12}              

            {'label': ['فابیہ نزر', 'Atif Aslam', 'Ayesha Omar', 'Maira khan', 'Sajal Ahad Mir', 'Maryam\u200c', 'Amirtha-Thendral', 'Amir Jaberi امیر جابری', 'Amira Riaa', '♔G𝟏 𝙼𝙾𝙷𝙰𝙼𝙼𝙴𝙳 𝙰𝚂𝙻𝙰𝙼', 'ARTISTIK✨', 'Melia ᵔᴥᵔ', '📱Andrew™📡', '🇵🇰x🇧🇩', 'NASSO❤', 'Cme 🌎', 'manish rajawat', 'DP 🖕', 'cutie pie', 'Ummeh Ammara', 'Umair shafqat Shafqat umair', 'Naveed Butt', 'Rabia ke liye', 'zubi_949', '', 'Gul e laila', 'Eesha Tariq', 'Maliha Khan', 'soniya', 'Hasnain Kanch', 'Daniyal Ali Khan', 'Mariam', 'Zara Asif✨', 'Fatima Tahira', 'ABC', '𝓭𝔂𝓮𝓾𝓷✨', 'Anastasia Poetrii', 'Rain', '👜kebutuhan wanita', '∆π', 'egisaputra', 'frenius latano', 'bellasafitri', 'yuniar firdausiana risky p.n', '𝒟ℯ𝓁𝓁𝒶 𝓂𝒶𝓊𝓁𝒾𝓎𝒶𝓃𝒶🥀', 'carissa syakillah Chandravia', 'Joao vitor Guimaraes', '[ E_C Team ]', 'Muhamad Ramdany', 'BERUANG.BIROE', 'Rahma', 'InfoAkunPenipu.Idn', 'MAGGOT STORE BEKASI', 'Meerajee  Official Team', 'Bilal Ashraf', 'Alastair (Ali-A)'], 'positive': ['0', '64', '49', '41', '45', '12', '16', '1', '60', '0', '78', '55', '0', '0', '0', '20', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '0', '0', '0', '0', '11', '0', '0', '34', '0', '4', '0', '0', '15', '0', '0', '0', '0', '3', '6', '0', '0', '0', '38', '0', '0', '0', '66', '66', '51', '57'], 'negative': ['0', '14', '29', '4', '33', '66', '62', '77', '18', '0', '0', '23', '0', '1', '0', '35', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '10', '0', '0', '21', '0', '6', '0', '0', '0', '0', '1', '0', '0', '3', '22', '3', '0', '0', '17', '0', '0', '78', '0', '12', '27', '21']}
    {'labels': ['ARTISTIK✨', 'Alastair (Ali-A)', 'Atif Aslam', 'Ayesha Omar', 'Bilal Ashraf', 'Cme 🌎', 'Fatima Tahira', 'InfoAkunPenipu.Idn', 'Meerajee  Official Team', 'Sajal Ahad Mir'], 'incitement to an offense': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'pornography': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'indecent': [2, 1, 6, 4, 1, 25, 12, 12, 3, 5], 'contempt of court': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'anti state': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


            """

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'doughnut', 'fa_chart', ['Count'],
                                              'Most active users'))

            dataset_list.append(create_graph_response_keybase(c_chart['label'], [list(map(int, c_chart['positive'])),
                                                                                 list(map(int, c_chart['negative']))],
                                                              'bar', 'fb_chart', ['Positive', 'Negative'],
                                                              'Users with sentiments'))

            dataset_list.append(create_graph_response_keybase(d_chart['labels'], [d_chart['incitement to an offense'],
                                                                                  d_chart['pornography'],
                                                                                  d_chart['indecent'],
                                                                                  d_chart['contempt of court'],
                                                                                  d_chart['anti state']],
                                                              'bar', 'fc_chart',
                                                              ['Incitement to an offense', 'Pornography', 'indecent',
                                                               'contempt of court', 'anti state'],
                                                              'Users with categorization'))

            # c_script, c_div = Instagram_Response_TMS_visualization.circle_pack_common_categorization()

            # show(row(s1,s2,s3))

        except Exception as e:
            print(e)



        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type":content_type, 'dataset_list': dataset_list})

    elif (content_type == 'twitter'):

        try:
            a_chart = Twitter_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Twitter_Response_TMS_visualization.most_active_users_chart()
            c_chart = Twitter_Response_TMS_visualization.circle_pack_common_sentiments()
            d_chart = Twitter_Response_TMS_visualization.circle_pack_common_categorization()

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'doughnut', 'b_chart', ['Count'],
                                              'Most active users'))

            dataset_list.append(create_graph_response_keybase(c_chart['label'], [list(map(int, c_chart['positive'])),
                                                                                 list(map(int, c_chart['negative']))],
                                                              'bar', 'fb_chart', ['Positive', 'Negative'],
                                                              'Users with sentiments'))

            dataset_list.append(create_graph_response_keybase(d_chart['labels'],
                                                              [d_chart['incitement to an offense'],
                                                               d_chart['pornography'],
                                                               d_chart['indecent'], d_chart['contempt of court'],
                                                               d_chart['anti state']],
                                                              'bar', 'fc_chart',
                                                              ['Incitement to an offense', 'Pornography', 'indecent',
                                                               'contempt of court', 'anti state'],
                                                              'Users with categorization'))



        except Exception as e:
            print(e)



        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})

    elif (content_type == 'facebook'):

        try:

            a_chart = Facebook_Profile_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Facebook_Profile_Response_TMS_visualization.most_active_users_chart()
            c_chart = Facebook_Profile_Response_TMS_visualization.circle_pack_common_sentiments()
            d_chart = Facebook_Profile_Response_TMS_visualization.circle_pack_common_categorization()

            print(a_chart)
            print(b_chart)
            print(c_chart)
            print(d_chart)

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'doughnut', 'fa_chart', ['Count'],
                                              'Most active users'))

            dataset_list.append(create_graph_response_keybase(c_chart['label'], [list(map(int, c_chart['positive'])),
                                                                                 list(map(int, c_chart['negative']))],
                                                              'bar', 'fb_chart', ['Positive', 'Negative'],
                                                              'Users with sentiments'))

            dataset_list.append(create_graph_response_keybase(d_chart['labels'],
                                                              [d_chart['incitement to an offense'],
                                                               d_chart['pornography'],
                                                               d_chart['indecent'], d_chart['contempt of court'],
                                                               d_chart['anti state']],
                                                              'bar', 'fc_chart',
                                                              ['Incitement to an offense', 'Pornography', 'indecent',
                                                               'contempt of court', 'anti state'],
                                                              'Users with categorization'))


        except Exception as e:
            print(e)


        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})



    elif (content_type == 'youtube'):

        try:
            a_chart = Youtube_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Youtube_Response_TMS_visualization.most_active_users_chart()

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'bar', 'fa_chart', ['Count'],
                                              'Most active users'))



        except Exception as e:
            print(e)



        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})


    elif (content_type == 'reddit'):

        try:

            a_chart = Reddit_Profile_Response_TMS_visualization.most_active_users_chart()
            b_chart = Reddit_Profile_Response_TMS_visualization.content_categorization_piechart()

            print(a_chart)
            print(b_chart)

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'bar', 'fa_chart', ['Count'],
                                              'Most active users'))


        except Exception as e:
            print(e)



        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})

    elif (content_type == 'subreddit'):

        try:
            a_chart = Reddit_Subreddit_Response_TMS_visualization.content_categorization_piechart()
            b_chart = Reddit_Subreddit_Response_TMS_visualization.most_active_users_chart()

            print(a_chart)
            print(b_chart)

            dataset_list.append(
                create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                              'Content categorization'))

            dataset_list.append(
                create_graph_response_keybase(b_chart.keys(), [b_chart.values()], 'bar', 'fa_chart', ['Count'],
                                              'Most active users'))


        except Exception as e:
            print(e)

        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})



    elif (content_type == 'trends'):

        try:
            a_chart = Trends_visualization.current_day_trends()
            b_chart = Trends_visualization.top_trend_detail()
            c_chart = Trends_visualization.trends_type_frequency()
            d_chart = Trends_visualization.country_wise_trends()
            e_chart = Trends_visualization.overall_hashtags()

            #print(a_chart)
            print(b_chart)
            print(c_chart)

            print(a_chart)
            print(d_chart)
            print(e_chart)
            #dataset_list.append(
                #create_graph_response_keybase(a_chart.keys(), [a_chart.values()], 'pie', 'a_chart', ['Count'],
                                            #  'Content categorization'))



            labels = []
            a_dataset = []
            #b_dataset = []

            for data in b_chart:
                labels.append(list(data.keys())[0])
                a_dataset.append(list(data.values())[0])

            dataset_list.append(
                create_graph_response_keybase(list(map(lambda x:x[0:30],labels)), [a_dataset], 'polarArea', 'fa_chart', ['Count'],
                                              'top social trends'))




            dataset_list.append(
                create_graph_response_keybase(c_chart.keys(), [c_chart.values()], 'bar', 'fb_chart', ['Count'],
                                              'social trends'))

            dataset_list.append(
                create_graph_response_keybase(e_chart.keys(), [e_chart.values()], 'bar', 'fc_chart', ['Count'],
                                              'overall hashtags'))
        except Exception as e:
            print(e)

        print(dataset_list)
        return render(request, 'Bi_Tools/keybase_visualization.html',
                      {"content_type": content_type, 'dataset_list': dataset_list})



    #show(row(s1,s2,s3))
    return render(request,'Bi_Tools/keybase_visualization.html',{"content_type":'keybase','dataset_list':dataset_list})


def create_graph_response_keybase(labels,data_list,chart_type,chart_position,inner_label=[''],title=''):




    resp_dict = {'title':title,'div': chart_position, 'type': chart_type, 'data': {
        'labels': json.dumps(list(labels)),
        'datasets': []

    }}

    for i,data in enumerate(data_list):
        resp_dict['data']['datasets'].append({
            'label': inner_label[i],
            'data': list(data),
            'borderWidth': 1
        })

    return resp_dict


def visualization(request,content_type):
    pass
    """
    print(content_type)
    #content_type = request.GET.get('content_type',None)




    if(content_type =='keybase'):

        print('i have called ')
        a_script, a_div = Keybase_Response_TMS_visualization.content_categorization_piechart()
        b_script, b_div = Keybase_Response_TMS_visualization.keywords_results()
        c_script, c_div = Keybase_Response_TMS_visualization.keywords_status_chart()
        d_script, d_div = Keybase_Response_TMS_visualization.no_of_keywords()

        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "c_script": c_script, "c_div": c_div,
                                                                        "d_script": d_script, "d_div": d_div,
                                                                        "content_type": content_type
                                                                        })


    elif(content_type =='instagram'):
        a_script, a_div = Instagram_Response_TMS_visualization.content_categorization_piechart()
        b_script, b_div = Instagram_Response_TMS_visualization.most_active_users_chart()
        #c_script, c_div = Instagram_Response_TMS_visualization.circle_pack_common_categorization()

        #show(row(s1,s2,s3))
        return render(request,'Bi_Tools/visualization_template.html',{"a_script": a_script, "a_div": a_div,
                                                                      "b_script": b_script, "b_div": b_div,

                                                                      "content_type": content_type



                                                                     })

    elif(content_type =='twitter'):

        print('i have called ')
        a_script, a_div = Twitter_Response_TMS_visualization.most_active_users_chart()
        b_script, b_div = Twitter_Response_TMS_visualization.content_categorization_piechart()


        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "content_type": content_type
                                                                        })

    elif (content_type == 'facebook'):
        try:
            print('i have called ')
            a_script, a_div = Facebook_Profile_Response_TMS_visualization.content_categorization_piechart()
            b_script, b_div = Facebook_Profile_Response_TMS_visualization.most_active_users_chart()
            c_script, c_div = Facebook_Page_Response_TMS_visualization.most_active_users_chart()
            d_script, d_div = Facebook_Group_Response_TMS_visualization.content_categorization_piechart()


            return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                            "b_script": b_script, "b_div": b_div,
                                                                            "c_script": c_script, "c_div": c_div,
                                                                            "d_script": d_script, "d_div": d_div,
                                                                            "content_type": content_type
                                                                                    })
        except Exception as e:
            print(e)
            return render(request, 'Bi_Tools/visualization_template.html', {})



    elif (content_type == 'youtube'):

        print('i have called ')
        a_script, a_div = Youtube_Response_TMS_visualization.content_categorization_piechart()
        b_script, b_div = Youtube_Response_TMS_visualization.most_active_users_chart()

        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "content_type": content_type
                                                                        })
    elif (content_type == 'reddit'):

        print('i have called ')
        a_script, a_div = Reddit_Profile_Response_TMS_visualization.most_active_users_chart()
        b_script, b_div = Reddit_Profile_Response_TMS_visualization.content_categorization_piechart()

        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "content_type": content_type
                                                                        })

    elif (content_type == 'subreddit'):

        print('i have called ')
        a_script, a_div = Reddit_Subreddit_Response_TMS_visualization.content_categorization_piechart()
        b_script, b_div = Reddit_Subreddit_Response_TMS_visualization.most_active_users_chart()

        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "content_type": content_type
                                                                        })

    elif (content_type == 'trends'):

        print('i have called ')
        a_script, a_div = Trends_visualization.country_wise_trends()
        b_script, b_div = Trends_visualization.top_trend_detail()
        c_script, c_div = Trends_visualization.trends_type_frequency()

        return render(request, 'Bi_Tools/visualization_template.html', {"a_script": a_script, "a_div": a_div,
                                                                        "b_script": b_script, "b_div": b_div,
                                                                        "c_script": c_script, "c_div": c_div,
                                                                        "content_type": content_type
                                                                        })
                                                                        
    """