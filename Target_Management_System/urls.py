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

    # path('target_response/',login_required(views.Target_Response.as_view()),name='target_response'),
    # template urls
    path('marktarget/', login_required(views.Add_Target.as_view()), name="tms_marktarget"),
    path('marktarget_portfolio/<str:portfolio_id>', login_required(views.Add_Target.as_view()), name="tms_marktarget_portfolio"),
    path('marktarget_prime/<str:prime_argument>/<str:target_site>', login_required(views.Add_Target.as_view()), name="tms_marktarget_prime"),
    path(
        'fetchtarget/',login_required(
        views.Target_Fetched.as_view()),
        name="tms_fetchtarget"),
    path(
        'fetchtarget/<str:target_site>',login_required(
        views.Target_Fetched.as_view()),
        name="tms_fetchtarget"),

    path(
        'identifytarget/',login_required(
        views.Identify_Target.as_view()),
        name="tms_identifytarget"),

    path(
        'survey/',login_required(
        views.Target_Internet_Survey.as_view()),
        name="tms_internetsurvey"),
    path(
        'crawl/',login_required(
        views.Dyanamic_Crawling.as_view()),
        name="tms_dynamiccrawling"),
    path('crawl_prime/<str:url>',login_required(views.Dyanamic_Crawling.as_view()),name="dynamic_crawling_prime"),
    path('keybase_crawling/',login_required(views.Keybase_Crawling.as_view()),name="tms_keybase_crawling"),
    path('targets_created/', login_required(views.Created_Targets.as_view()), name="tms_targetscreated"),
    path('facebook_target_response/', login_required(views.Facebook_Target_Response.as_view()), name="facebook_target_response"),
    # ajax urls
    path('smartsearch/', login_required(views.Smart_Search.as_view()), name='tms_smartsearch'),
    path('test/', login_required(views.Test_View.as_view()), name="sendevent"),
    path('test1/', login_required(views.Test_View1.as_view()), name="alertevent"),
    path('identifytarget_request/',login_required(views.Identify_Target_Request.as_view()),name="tms_identifytarget_request"),
    path('timeline/',login_required(views.Timeline.as_view()),name="timeline"),
    path('timeline_fetch/',login_required(views.Timeline_Fetch.as_view()),name="timeline_fetch"),
    path('link_analysis/<str:object_gtr_id>',login_required(views.Link_Analysis.as_view()),name="link_analysis"),
    path('close_associates_tree_graph/<str:object_gtr_id>',login_required(views.Close_Associates_Tree_Graph.as_view()),name="close_associates_tree_graph"),
    path('instagram_follower_tree_graph/<str:object_gtr_id>',login_required(views.Instagram_Follower_Tree_Graph.as_view()),name="instagram_follower_tree_graph"),
    path('twitter_follower_tree_graph/<str:object_gtr_id>',login_required(views.Twitter_Follower_Tree_Graph.as_view()),name="twitter_follower_tree_graph"),
    # ahmed Class Views
    path('target/instagram/<str:object_gtr_id>', login_required(Instagram_Target_Response.as_view()), name="Instagram_Target_Response"),
    path('report/instagram/<str:object_gtr_id>', login_required(Instagram_Target_Report.as_view()), name="Instagram_Target_Report"),
    
    # Twitter reports and targets pages
    path('target/twitter/<str:object_gtr_id>', login_required(Twitter_Target_Response.as_view()), name="Twitter_Target_Response"),
    path('report/twitter/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(Twitter_Target_Report.as_view()), name="Twitter_Target_Report"),
    
    # Linkedin reports and targets pages
    path('target/linkedin/person/<str:object_gtr_id>', login_required(LinkedinPerson_Target_Response.as_view()), name="LinkedinPerson_Target_Response"),
    path('target/linkedin/company/<str:object_gtr_id>', login_required(LinkedinCompany_Target_Response.as_view()), name="LinkedinCompany_Target_Response"),
    path('report/linkedin/person/<str:object_gtr_id>', login_required(LinkedinPerson_Target_Report.as_view()), name="LinkedinPerson_Target_Report"),
    path('report/linkedin/company/<str:object_gtr_id>', login_required(LinkedinCompany_Target_Report.as_view()), name="LinkedinCompany_Target_Report"),
    
    # Facebook reports and targets pages 
    path('target/facebook/person/<str:object_gtr_id>', login_required(FacebookPerson_Target_Response.as_view()), name="FacebookPerson_Target_Response"),
    path('target/facebook/page/<str:object_gtr_id>', login_required(FacebookPage_Target_Response.as_view()), name="FacebookPage_Target_Response"),
    path('target/facebook/group/<str:object_gtr_id>', login_required(FacebookGroup_Target_Response.as_view()), name="FacebookGroup_Target_Response"),
    path('report/facebook/person/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(FacebookPersonReport.as_view()), name="FacebookPersonReport"),
    path('report/facebook/page/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(FacebookPageReport.as_view()), name="FacebookPageReport"),
    path('report/facebook/group/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(FacebookGroupReport.as_view()), name="FacebookGroupReport"),
    
    # Reddit reports and targets pages 
    path('report/target/reddit/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(Reddit_Target_Report.as_view()), name="Reddit_Target_Report"),
    path('target/reddit/<str:object_gtr_id>', login_required(Reddit_Target_Response.as_view()), name="reddit_target_response"),
    # Sub-Reddit reports and targets pages 
    path('report/target/subreddit/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(Subreddit_Target_Report.as_view()), name="Subreddit_Target_Report"),
    path('target/sub_reddit/<str:object_gtr_id>/',login_required(Subreddit_Target_Resposne.as_view()), name="subreddit_target_resposne"),

    # Youtube reports and targets pages 
    path('report/target/youtube/?P(?P<object_gtr_id>[0-9]+)\\/$/', login_required(Youtube_Target_Report.as_view()), name="Youtube_Target_Report"),
    path('target/youtube/<str:object_gtr_id>/', login_required(Youtube_Target_Response.as_view()), name="Youtube_Target_Response"),
    # Dynamic  reports and targets pages 
    path('target/dynmaic_crawling/<str:object_gtr_id>/',login_required(Dynamic_Crawling_Target.as_view()), name="dynamic_crawling_target"),
    path('report/dynmaic_crawling/<str:object_gtr_id>/',login_required(Dynamic_Crawling_Report.as_view()), name="dynamic_crawling_report"),
    path('bulk_targets/',login_required(Bulk_Targets.as_view()), name="bulk_targets"),
    path('graph/<str:object_gtr_id>/',login_required(views.Graph.as_view()), name="graph"),
   
 
   


  
    
]