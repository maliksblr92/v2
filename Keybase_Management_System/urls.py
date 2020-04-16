from django.urls import path
from Keybase_Management_System import views
app_name = 'Keybase_Management_System'

urlpatterns = [

    # path('target_response/',views.Target_Response.as_view(),name='target_response'),
    path('create/', views.Create_Keybase.as_view(), name='kms_create'),
    path('archive/', views.Keybase_Archive.as_view(), name='kms_archive'),
    path('edit/', views.Edit_Keybase.as_view(), name='kms_edit'),
    path('delprop/', views.DeleteKeybaseProperty.as_view(), name='kms_delprop')

]