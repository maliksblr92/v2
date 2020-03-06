from django.urls import path
from Data_Processing_Unit import views
app_name = 'Data_Processing_Unit'
import os
import time

urlpatterns = [

    path('target_response/',views.Target_Response.as_view(),name='target_response'),
    path('facebook_profile_view/<str:m_id>',views.Facebook_Profile_View.as_view(),name='facebook_profile_view'),
    path('twitter_profile_view/<str:m_id>',views.Twitter_Profile_View.as_view(),name='twitter_profile_view'),
    path('instagram_profile_view/<str:m_id>',views.Instagram_Profile_View.as_view(),name='instagram_profile_view'),
    path('linkedin_profile_person_view/<str:m_id>',views.Linkedin_Profile_Person_View.as_view(),name='linkedin_profile_person_view'),
    path('linkedin_profile_person_view/<str:m_id>',views.Linkedin_Profile_Company_View.as_view(),name='linkedin_profile_person_view'),
    path('big_view/', views.BigView.as_view(), name='big_view'),
    path('link_analysis/', views.Link_Analysis.as_view(), name='link_analysis'),
    path('twitter_trends_country/<str:country>', views.Twitter_Trends_Country.as_view(), name='twitter_trends_country'),
    path('twitter_trends_worldwide/', views.Twitter_Trends_Worldwide.as_view(), name='twitter_trends_worldwide'),
    path('news_monitoring/', views.News_Monitoring.as_view(), name='news_monitoring'),
    path('reports_management/', views.Report_Management_View.as_view(), name='reports_management'),
    path('convert_html_to_pdf/', views.Convert_Html_To_Pdf.as_view(), name='convert_html_to_pdf'),

]




