from django.urls import path
from Target_Management_System import views
app_name = 'Target_Management_System'

urlpatterns = [

    # path('target_response/',views.Target_Response.as_view(),name='target_response'),
    # template urls
    path('marktarget/', views.Add_Target.as_view(), name="tms_marktarget"),
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
    path('targets_created/', views.Created_Targets.as_view(), name="tms_targetscreated"),
    path('explore_target/', views.Explore_Target.as_view(), name="explore_target"),
    # ajax urls
    path('smartsearch/', views.Smart_Search.as_view(), name='tms_smartsearch'),
    path('test/', views.Test_View.as_view(), name="sendevent"),
    path('test1/', views.Test_View1.as_view(), name="alertevent"),
    path('identifytarget_request/',views.Identify_Target_Request.as_view(),name="tms_identifytarget_request"),
]
