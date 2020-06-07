from django.urls import path
from OSINT_System_Core import views

# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'OSINT_System_Core'

urlpatterns = [
    path('', views.Main.as_view(), name='main_page'),
    # path('target_author_main/',views.Target_Author_Main.as_view(),name = 'target_author_main'),
    path('target_headlines_main/', views.Target_Headlines_Main.as_view(),
         name='target_headlines_main'),
    # path('supported_site_list/',views.Supported_Social_Site_List.as_view(),name = 'supported_site_list'),
    # path('add_news_target/',views.News_Target.as_view(),name='add_news_target'),
    # path('add_instagram_target/', views.Add_Instagram_Target.as_view(), name='add_instagram_target'),
    # path('add_twitter_target/', views.Add_Twitter_Target.as_view(), name='add_twitter_target'),
    # path('add_facebook_target/', views.Add_Facebook_Target.as_view(), name='add_facebook_target'),
    # path('add_linkedin_target/', views.Add_Linkedin_Target.as_view(), name='add_linkedin_target'),

    path('article_stat_overview', views.Article_Stat_Overview.as_view(),
         name='article_stat_overview'),
    path('article_stat_slo', views.Article_Stat_Slo.as_view(),
         name='article_stat_slo'),
    path(
        'my_article_stat',
        views.My_Article_Stat.as_view(),
        name='my_article_stat'),
    path('ticket_stat', views.Ticket_State.as_view(), name='ticket_stat'),
    path('fetch_stat', views.Fetch_State.as_view(), name='fetch_stat'),
    path('extracted_article', views.Extracted_Article.as_view(),
         name='extracted_article'),
    path('extracted_selected_all_site', views.Extracted_All_Sites.as_view(),
         name='extracted_selected_all_site'),
    path('extracted_selected_all_social_sites', views.Extracted_All_Social_Sites.as_view(
    ), name='extracted_selected_all_social_sites'),
    path('processed_article', views.Processed_Article.as_view(),
         name='processed_article'),
    path('article_trend', views.Article_Trend.as_view(), name='article_trend'),
    path('send_to_pco', views.Sent_To_Pco, name='send_to_pco'),
    path('smart_search/<str:author_account>/<str:search_site>/',
         views.Smart_Search.as_view(), name='smart_search'),
    # path('get_facebook_targets',views.Get_Facebook_Targets.as_view(),name='get_facebook_target'),
    # path('get_twitter_targets',views.Get_Twitter_Targets.as_view(),name='get_twitter_target'),
    # path('get_instagram_targets',views.Get_Instagram_Targets.as_view(),name='get_instagram_target'),
    # path('get_linkedin_targets',views.Get_Linkedin_Person_Targets.as_view(),name='get_linkedin_target'),

    path('target_author_instagram/', views.Target_Author_Instagram.as_view(),
         name='target_author_instagram'),
    path('target_author_facebook/', views.Target_Author_Facebook.as_view(),
         name='target_author_facebook'),
    path('target_author_twitter/', views.Target_Author_Twitter.as_view(),
         name='target_author_twitter'),
    path('target_author_linkedin/', views.Target_Author_Linkedin.as_view(),
         name='target_author_linkedin'),
    path('dispatcher/<str:GTR>/<str:author_account>',
         views.Dispatcher.as_view(), name='dispatcher'),
    path('find_object/',views.Find_Object.as_view(), name='find_object'),
    path('link_object/',views.Link_Object.as_view(), name='link_object'),
    path('share_resource/',views.Share_Resource.as_view(), name='share_resource'),
    path('rabbit_message/',views.Rabbit_Message.as_view(), name='rabbit_message'),
    path('logged_ips/', views.Logged_Ips.as_view(), name='logged_ips'),
    path('delete_ips/<str:obj_id>/', views.Delete_Ips.as_view(), name='delete_ips'),
    path('views_ip_logger_resp/<str:latlons>/', views.View_Logged_Ip_Response.as_view(), name='views_ip_logger_resp'),


    # path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('test', views.test_view, name='test'),
    path('tsodash/', views.TSO_Dashboard.as_view(), name="tso-dashboard"),
    path('tmodash/', views.TMO_Dashboard.as_view(), name='tmo-dashboard'),
    path('rdodash/', views.RDO_Dashboard.as_view(), name='rdo-dashboard'),
    path('paodash/', views.PAO_Dashboard.as_view(), name='pao-dashboard'),


    # ahmed start
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('main/', views.main, name='main'),
    path('main_1/', views.main_1, name='main_1'),
    path('main/heatmap/', views.mainHeatMap, name='mainHeatMap'),
    path('newsmonitoring/', views.newsMonitor, name='newsMonitor'),
    path('top_news/', views.topNews, name='topNews'),
    path('getTrendsByCountry/', views.getTrendsByCountry, name='getTrendsByCountry'),
    path('getYoutubeTrends/', views.getYoutubeTrends, name='getYoutubeTrends'),
    path('update_micro_crawler_stats/',views.update_micro_crawler_stats,name='update_micro_crawler_stats'),
    path('update_internet_stats/',views.update_internet_stats,name='update_internet_stats'),
    path('update_dashboard_donutchart/',views.update_dashboard_donutchart,name='update_dashboard_donutchart'),
    path('worldwide_twitter_hashtags/',views.get_worldwide_hashtags,name='worldwide_twitter_hashtags'),
    path('getGoogleTrends/',views.getGoogleTrends,name='getGoogleTrends'),
    path('periodic_target/',views.Periodic_Target_DB,name='Periodic_Target_DB'),
    path('periodic_target/delete/<str:periodic_task_id>',views.Delete_Periodic_Target_DB.as_view(),name='Delete_Periodic_Target_DB'),
    path('design_test',views.design_test,name='design_test'),    # ahmed end
]

# urlpatterns = format_suffix_patterns(urlpatterns)