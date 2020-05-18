from django.urls import path
from Case_Management_System import views
app_name = 'Case_Management_System'

urlpatterns = [
    path('create/', views.CreateCase.as_view(), name='cms_create_case'),
    path('location/', views.StoreAndRetrieveLocation.as_view(), name='cms_location'),
    #path('target_response/',views.Target_Response.as_view(),name='target_response'),
    path('explore_data/', views.Explore_Data.as_view(), name='explore_data'),


]