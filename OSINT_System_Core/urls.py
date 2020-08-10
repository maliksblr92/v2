from django.urls import path,include
from OSINT_System_Core import views
from django.contrib.auth.decorators import login_required
# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'OSINT_System_Core'

urlpatterns = [
    path('', login_required(views.Main.as_view()), name='main_page'),
    # path('target_author_main/',views.Target_Author_Main.as_view(),name = 'target_author_main'),
    path('target_headlines_main/', login_required(views.Target_Headlines_Main.as_view()),
         name='target_headlines_main'),
    # path('supported_site_list/',views.Supported_Social_Site_List.as_view(),name = 'supported_site_list'),
    # path('add_news_target/',views.News_Target.as_view(),name='add_news_target'),
    # path('add_instagram_target/', views.Add_Instagram_Target.as_view(), name='add_instagram_target'),
    # path('add_twitter_target/', views.Add_Twitter_Target.as_view(), name='add_twitter_target'),
    # path('add_facebook_target/', views.Add_Facebook_Target.as_view(), name='add_facebook_target'),
    # path('add_linkedin_target/', views.Add_Linkedin_Target.as_view(), name='add_linkedin_target'),

    path('article_stat_overview', login_required(views.Article_Stat_Overview.as_view()),
         name='article_stat_overview'),
    path('article_stat_slo', login_required(views.Article_Stat_Slo.as_view()),
         name='article_stat_slo'),
    path(
        'my_article_stat',
        login_required(views.My_Article_Stat.as_view()),
        name='my_article_stat'),
    path('ticket_stat', login_required(views.Ticket_State.as_view()), name='ticket_stat'),
    path('fetch_stat', login_required(views.Fetch_State.as_view()), name='fetch_stat'),
    path('extracted_article',login_required(views.Extracted_Article.as_view()),
         name='extracted_article'),
    path('extracted_selected_all_site',login_required(views.Extracted_All_Sites.as_view()),
         name='extracted_selected_all_site'),
    path('extracted_selected_all_social_sites',login_required(views.Extracted_All_Social_Sites.as_view(
    )), name='extracted_selected_all_social_sites'),
    path('processed_article', views.Processed_Article.as_view(),
         name='processed_article'),
    path('article_trend', login_required(views.Article_Trend.as_view()), name='article_trend'),
    path('send_to_pco', login_required(views.Sent_To_Pco), name='send_to_pco'),
    path('smart_search/<str:author_account>/<str:search_site>/',
         login_required(views.Smart_Search.as_view()), name='smart_search'),
    # path('get_facebook_targets',views.Get_Facebook_Targets.as_view(),name='get_facebook_target'),
    # path('get_twitter_targets',views.Get_Twitter_Targets.as_view(),name='get_twitter_target'),
    # path('get_instagram_targets',views.Get_Instagram_Targets.as_view(),name='get_instagram_target'),
    # path('get_linkedin_targets',views.Get_Linkedin_Person_Targets.as_view(),name='get_linkedin_target'),

    path('target_author_instagram/', login_required(views.Target_Author_Instagram.as_view()),
         name='target_author_instagram'),
    path('target_author_facebook/', login_required(views.Target_Author_Facebook.as_view()),
         name='target_author_facebook'),
    path('target_author_twitter/', login_required(views.Target_Author_Twitter.as_view()),
         name='target_author_twitter'),
    path('target_author_linkedin/', login_required(views.Target_Author_Linkedin.as_view()),
         name='target_author_linkedin'),
    path('dispatcher/<str:GTR>/<str:author_account>',
         login_required(views.Dispatcher.as_view()), name='dispatcher'),
    path('find_object/',login_required(views.Find_Object.as_view()), name='find_object'),
    path('link_object/',login_required(views.Link_Object.as_view()), name='link_object'),
    path('share_resource/',login_required(views.Share_Resource.as_view()), name='share_resource'),
    path('rabbit_message/',login_required(views.Rabbit_Message.as_view()), name='rabbit_message'),
    path('logged_ips/', login_required(views.Logged_Ips.as_view()), name='logged_ips'),
    path('delete_ips/<str:obj_id>/', login_required(views.Delete_Ips.as_view()), name='delete_ips'),
    path('views_ip_logger_resp/<str:latlons>/', login_required(views.View_Logged_Ip_Response.as_view()), name='views_ip_logger_resp'),


    # path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('test', login_required(views.test_view), name='test'),
    path('tsodash/', login_required(views.TSO_Dashboard.as_view()), name="tso-dashboard"),
#     path('tmodash/', login_required(views.TMO_Dashboard.as_view()), name='tmo-dashboard'),
    path('rdodash/', login_required(views.RDO_Dashboard.as_view()), name='rdo-dashboard'),
    path('paodash/', login_required(views.PAO_Dashboard.as_view()), name='pao-dashboard'),


    # ahmed start
    path('dashboard/', login_required(views.Dashboard.as_view()), name='dashboard'),
    path('main/', login_required(views.main), name='main'),
    path('main_1/', login_required(views.main_1), name='main_1'),
    path('main/heatmap/', login_required(views.mainHeatMap), name='mainHeatMap'),
    path('newsmonitoring/', login_required(views.newsMonitor), name='newsMonitor'),
    path('top_news/', login_required(views.topNews), name='topNews'),
    path('getTrendsByCountry/', login_required(views.getTrendsByCountry), name='getTrendsByCountry'),
    path('getYoutubeTrends/', login_required(views.getYoutubeTrends), name='getYoutubeTrends'),
    path('update_micro_crawler_stats/',login_required(views.update_micro_crawler_stats),name='update_micro_crawler_stats'),
    path('update_internet_stats/',login_required(views.update_internet_stats),name='update_internet_stats'),
    path('update_dashboard_donutchart/',login_required(views.update_dashboard_donutchart),name='update_dashboard_donutchart'),
    path('worldwide_twitter_hashtags/',login_required(views.get_worldwide_hashtags),name='worldwide_twitter_hashtags'),
    path('getGoogleTrends/',login_required(views.getGoogleTrends),name='getGoogleTrends'),
    path('periodic_target/',login_required(views.Periodic_Target_DB),name='Periodic_Target_DB'),
    path('periodic_target/delete/<str:periodic_task_id>',login_required(views.Delete_Periodic_Target_DB.as_view()),name='Delete_Periodic_Target_DB'),
    path('tmo_base/',login_required(views.TMO_Base),name='tmo_base'),
    path('tmo_dashboard/',login_required(views.TMO),name='tmo_dashboard'), 
]

# urlpatterns = format_suffix_patterns(urlpatterns)
