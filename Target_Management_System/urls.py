from django.urls import path
from Target_Management_System import views
app_name = 'Target_Management_System'
from django.contrib.auth.decorators import login_required
# ahmed  imports
from .views import  Instagram_Target_Response
from .views import Instagram_Target_Report
from .views import  Twitter_Target_Response
from .views import  LinkedinPerson_Target_Response
from .views import  LinkedinCompany_Target_Response
from .views import  LinkedinCompany_Target_Report
from .views import LinkedinPerson_Target_Report
from .views import  FacebookPerson_Target_Response
from .views import  FacebookPage_Target_Response
from .views import  FacebookGroup_Target_Response
from .views import FacebookPersonReport
from .views import FacebookPageReport
from .views import FacebookGroupReport
from .views import Bulk_Targets
from .views import Reddit_Target_Response
from .views import Reddit_Target_Report
from .views import  Youtube_Target_Response
from .views import Youtube_Target_Report
from .views import Dynamic_Crawling_Target
from .views import Subreddit_Target_Resposne
from .views import Subreddit_Target_Report
from .views import Twitter_Target_Report
from .views import Dynamic_Crawling_Report


# end ahmed imports
urlpatterns = [

    # path('target_response/',views.Target_Response.as_view(),name='target_response'),
    # template urls
    path('marktarget/', views.Add_Target.as_view(), name="tms_marktarget"),
    path('marktarget_portfolio/<str:portfolio_id>', views.Add_Target.as_view(), name="tms_marktarget_portfolio"),
    path('marktarget_prime/<str:prime_argument>/<str:target_site>', views.Add_Target.as_view(), name="tms_marktarget_prime"),
    path('fetchtarget/',views.Target_Fetched.as_view(),name="tms_fetchtarget"),
    path(
        'fetchtarget/<str:target_site>',
        views.Target_Fetched.as_view(),
        name="tms_fetchtarget"),

    path(
        'identifytarget/',
        views.Identify_Target.as_view(),
        name="tms_identifytarget"),

    path(
        'survey/',
        views.Target_Internet_Survey.as_view(),
        name="tms_internetsurvey"),
    path(
        'crawl/',
        views.Dyanamic_Crawling.as_view(),
        name="tms_dynamiccrawling"),
    path('crawl_prime/<str:url>',views.Dyanamic_Crawling.as_view(),name="dynamic_crawling_prime"),
    path('keybase_crawling/',views.Keybase_Crawling.as_view(),name="tms_keybase_crawling"),
    path('targets_created/', views.Created_Targets.as_view(), name="tms_targetscreated"),
    path('facebook_target_response/', views.Facebook_Target_Response.as_view(), name="facebook_target_response"),
    # ajax urls
    path('smartsearch/', views.Smart_Search.as_view(), name='tms_smartsearch'),
    path('test/', views.Test_View.as_view(), name="sendevent"),
    path('test1/', views.Test_View1.as_view(), name="alertevent"),
    path('identifytarget_request/',views.Identify_Target_Request.as_view(),name="tms_identifytarget_request"),
    path('timeline/',views.Timeline.as_view(),name="timeline"),
    path('timeline_fetch/',views.Timeline_Fetch.as_view(),name="timeline_fetch"),
    path('link_analysis/<str:object_gtr_id>',views.Link_Analysis.as_view(),name="link_analysis"),
    path('close_associates_tree_graph/<str:object_gtr_id>',views.Close_Associates_Tree_Graph.as_view(),name="close_associates_tree_graph"),
    path('instagram_follower_tree_graph/<str:object_gtr_id>',views.Instagram_Follower_Tree_Graph.as_view(),name="instagram_follower_tree_graph"),
    path('twitter_follower_tree_graph/<str:object_gtr_id>',views.Twitter_Follower_Tree_Graph.as_view(),name="twitter_follower_tree_graph"),
    # ahmed Class Views
    path('target/instagram/<str:object_gtr_id>', Instagram_Target_Response.as_view(), name="Instagram_Target_Response"),
    path('report/instagram/<str:object_gtr_id>', Instagram_Target_Report.as_view(), name="Instagram_Target_Report"),
    
    # Twitter reports and targets pages
    path('target/twitter/<str:object_gtr_id>', Twitter_Target_Response.as_view(), name="Twitter_Target_Response"),
    path('report/twitter/?P(?P<object_gtr_id>[0-9]+)\\/$/', Twitter_Target_Report.as_view(), name="Twitter_Target_Report"),
    
    # Linkedin reports and targets pages
    path('target/linkedin/person/<str:object_gtr_id>', LinkedinPerson_Target_Response.as_view(), name="LinkedinPerson_Target_Response"),
    path('target/linkedin/company/<str:object_gtr_id>', LinkedinCompany_Target_Response.as_view(), name="LinkedinCompany_Target_Response"),
    path('report/linkedin/person/<str:object_gtr_id>', LinkedinPerson_Target_Report.as_view(), name="LinkedinPerson_Target_Report"),
    path('report/linkedin/company/<str:object_gtr_id>', LinkedinCompany_Target_Report.as_view(), name="LinkedinCompany_Target_Report"),
    
    # Facebook reports and targets pages 
    path('target/facebook/person/<str:object_gtr_id>', FacebookPerson_Target_Response.as_view(), name="FacebookPerson_Target_Response"),
    path('target/facebook/page/<str:object_gtr_id>', FacebookPage_Target_Response.as_view(), name="FacebookPage_Target_Response"),
    path('target/facebook/group/<str:object_gtr_id>', FacebookGroup_Target_Response.as_view(), name="FacebookGroup_Target_Response"),
    path('report/facebook/person/?P(?P<object_gtr_id>[0-9]+)\\/$/', FacebookPersonReport.as_view(), name="FacebookPersonReport"),
    path('report/facebook/page/?P(?P<object_gtr_id>[0-9]+)\\/$/', FacebookPageReport.as_view(), name="FacebookPageReport"),
    path('report/facebook/group/?P(?P<object_gtr_id>[0-9]+)\\/$/', FacebookGroupReport.as_view(), name="FacebookGroupReport"),
    
    # Reddit reports and targets pages 
    path('report/target/reddit/?P(?P<object_gtr_id>[0-9]+)\\/$/', Reddit_Target_Report.as_view(), name="Reddit_Target_Report"),
    path('target/reddit/<str:object_gtr_id>', Reddit_Target_Response.as_view(), name="reddit_target_response"),
    # Sub-Reddit reports and targets pages 
    path('report/target/subreddit/?P(?P<object_gtr_id>[0-9]+)\\/$/', Subreddit_Target_Report.as_view(), name="Subreddit_Target_Report"),
    path('target/sub_reddit/<str:object_gtr_id>/',Subreddit_Target_Resposne.as_view(), name="subreddit_target_resposne"),

    # Youtube reports and targets pages 
    path('report/target/youtube/?P(?P<object_gtr_id>[0-9]+)\\/$/', Youtube_Target_Report.as_view(), name="Youtube_Target_Report"),
    path('target/youtube/<str:object_gtr_id>/', Youtube_Target_Response.as_view(), name="Youtube_Target_Response"),
    # Dynamic  reports and targets pages 
    path('target/dynmaic_crawling/<str:object_gtr_id>/',Dynamic_Crawling_Target.as_view(), name="dynamic_crawling_target"),
    path('report/dynmaic_crawling/<str:object_gtr_id>/',Dynamic_Crawling_Report.as_view(), name="dynamic_crawling_report"),
    path('bulk_targets/',Bulk_Targets.as_view(), name="bulk_targets"),
    path('graph/<str:object_gtr_id>/',views.Graph.as_view(), name="graph"),
    path('generatePDF/<str:object_gtr_id>/',views.generatePDF,name='generatePDF'), 
    # 5ec047b84202dee21e2dd8b7
   


  
    
]