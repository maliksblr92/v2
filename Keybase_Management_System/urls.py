from django.urls import path
from Keybase_Management_System import views
app_name = 'Keybase_Management_System'
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # path('target_response/',login_required(views.Target_Response.as_view()),name='target_response'),
    path('create/', login_required(views.Create_Keybase.as_view()), name='kms_create'),
    path('archive/', login_required(views.Keybase_Archive.as_view()), name='kms_archive'),
    path('edit/', login_required(views.Edit_Keybase.as_view()), name='kms_edit'),
    path('delprop/', login_required(views.DeleteKeybaseProperty.as_view()), name='kms_delprop'),
    path('keybase_fetched_responses/<str:GTR_id>', login_required(views.Keybase_Fetched_Responses.as_view()), name='Keybase_Fetched_Responses'),
    path('report/keybase_fetched_responses/<str:GTR_id>/', login_required(views.Keybase_Fetched_Report.as_view()), name='Keybase_Fetched_Report'),
    path('block_url/', login_required(views.Block_URL.as_view()),name='block_url'),
    path('block_keybase_url/<str:url>/', login_required(views.Block_URL.as_view()),name='block_keybase_url'),
    path('delete_url/<str:url_id>/', login_required(views.Delete_URL.as_view()),name='delete_url'),
    path('keybase_processed_report/<str:GTR_id>/', login_required(views.Keybase_Processed_Report.as_view()),name='keybase_processed_report'),
    path('graph/<str:GTR_id>/', login_required(views.Graph_Analysis.as_view()),name='graph_analysis'),

]