from django.urls import path
from Data_Processing_Unit import views
app_name = 'Data_Processing_Unit'
import os
import time
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('target_response/',login_required(views.Target_Response.as_view()),name='target_response'),
    path('facebook_profile_view/<str:m_id>',login_required(views.Facebook_Profile_View.as_view()),name='facebook_profile_view'),
    path('twitter_profile_view/<str:m_id>',login_required(views.Twitter_Profile_View.as_view()),name='twitter_profile_view'),
    path('instagram_profile_view/<str:m_id>',login_required(views.Instagram_Profile_View.as_view()),name='instagram_profile_view'),
    path('linkedin_profile_person_view/<str:m_id>',login_required(views.Linkedin_Profile_Person_View.as_view()),name='linkedin_profile_person_view'),
    path('linkedin_profile_person_view/<str:m_id>',login_required(views.Linkedin_Profile_Company_View.as_view()),name='linkedin_profile_person_view'),
    path('big_view/', login_required(views.BigView.as_view()), name='big_view'),
    path('link_analysis/', login_required(views.Link_Analysis.as_view()), name='link_analysis'),
    path('twitter_trends_country/<str:country>', login_required(views.Twitter_Trends_Country.as_view()), name='twitter_trends_country'),
    path('twitter_trends_worldwide/', login_required(views.Twitter_Trends_Worldwide.as_view()), name='twitter_trends_worldwide'),
    path('news_monitoring/', login_required(views.News_Monitoring.as_view()), name='news_monitoring'),
    path('reports_management/', login_required(views.Report_Management_View.as_view()), name='reports_management'),
    path('convert_html_to_pdf/', login_required(views.Convert_Html_To_Pdf.as_view()), name='convert_html_to_pdf'),
    path('response_changes_view/', login_required(views.Response_Changes_View.as_view()), name='response_changes_view'),

    # ahmed paths
    path('index/', login_required(views.Index.as_view()), name='index'),
    path('index_scrapper/', login_required(views.Index_Scrapper.as_view()), name='index_scrapper'),
    path('index_darkweb/', login_required(views.Index_Darkweb.as_view()), name='index_darkweb'),
    path('index_textprocessing/', login_required(views.Index_Textprocessing.as_view()), name='index_textprocessing'),
    # ahmed twitter urls
    path('twitter/', login_required(views.Twitter.as_view()), name="Twitter"),
    path('tweets/', login_required(views.Tweets.as_view()), name="Tweets"),
    path('get_hashtag_tweets/?P(?P<hashtag_name>[0-9]+)\\/$/', login_required(views.Get_Hashtag_Tweets.as_view()), name="get_hashtag_tweets"),
    path('iptools/', login_required(views.Ip_Tools.as_view()), name="iptools"),
]




