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
    # ajax urls
    path('smartsearch/', views.Smart_Search.as_view(), name='tms_smartsearch'),
]
