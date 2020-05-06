from django.urls import path
from Target_Management_System import views
app_name = 'Target_Management_System'
# ahmed  imports
from .views import  Instagram_Target_Response
from .views import  Twitter_Target_Response
from .views import  LinkedinPerson_Target_Response
from .views import  LinkedinCompany_Target_Response
from .views import  FacebookPerson_Target_Response
from .views import  FacebookPage_Target_Response
from .views import  FacebookGroup_Target_Response
from .views import Index

# end ahmed imports
urlpatterns = [

    # path('target_response/',views.Target_Response.as_view(),name='target_response'),
    # template urls
    path('marktarget/', views.Add_Target.as_view(), name="tms_marktarget"),
    path('marktarget/<str:portfolio_id>', views.Add_Target.as_view(), name="tms_marktarget"),
    path(
        'fetchtarget/',
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
path(
        'keybase_crawling/',
        views.Keybase_Crawling.as_view(),
        name="tms_keybase_crawling"),
    path('targets_created/', views.Created_Targets.as_view(), name="tms_targetscreated"),
    path('facebook_target_response/', views.Facebook_Target_Response.as_view(), name="facebook_target_response"),
    # ajax urls
    path('smartsearch/', views.Smart_Search.as_view(), name='tms_smartsearch'),
    path('test/', views.Test_View.as_view(), name="sendevent"),
    path('test1/', views.Test_View1.as_view(), name="alertevent"),
    path('identifytarget_request/',views.Identify_Target_Request.as_view(),name="tms_identifytarget_request"),

    # ahmed Class Views
    path('target/instagram/', Instagram_Target_Response.as_view(), name="Instagram_Target_Response"),
    path('target/twitter/', Twitter_Target_Response.as_view(), name="Twitter_Target_Response"),
    path('target/linkedin/person/', LinkedinPerson_Target_Response.as_view(), name="LinkedinPerson_Target_Response"),
    path('target/linkedin/company/', LinkedinCompany_Target_Response.as_view(), name="LinkedinCompany_Target_Response"),
    path('target/facebook/person/', FacebookPerson_Target_Response.as_view(), name="FacebookPerson_Target_Response"),
    path('target/facebook/page/', FacebookPage_Target_Response.as_view(), name="FacebookPage_Target_Response"),
    path('target/facebook/group/', FacebookGroup_Target_Response.as_view(), name="FacebookGroup_Target_Response"),
    path('target/test/', Index.as_view(), name="Index"),

]
