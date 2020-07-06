from django.urls import path
from Keybase_Management_System import views
app_name = 'Keybase_Management_System'


urlpatterns = [

    # path('target_response/',views.Target_Response.as_view(),name='target_response'),
    path('create/', views.Create_Keybase.as_view(), name='kms_create'),
    path('archive/', views.Keybase_Archive.as_view(), name='kms_archive'),
    path('edit/', views.Edit_Keybase.as_view(), name='kms_edit'),
    path('delprop/', views.DeleteKeybaseProperty.as_view(), name='kms_delprop'),
    path('keybase_fetched_responses/<str:GTR_id>', views.Keybase_Fetched_Responses.as_view(), name='Keybase_Fetched_Responses'),
    path('report/keybase_fetched_responses/<str:GTR_id>/', views.Keybase_Fetched_Report.as_view(), name='Keybase_Fetched_Report'),
    path('block_url/', views.Block_URL.as_view(),name='block_url'),
    path('block_keybase_url/<str:url>/', views.Block_URL.as_view(),name='block_keybase_url'),
    path('delete_url/<str:url_id>/', views.Delete_URL.as_view(),name='delete_url'),

]