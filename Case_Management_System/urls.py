from django.urls import path
from Case_Management_System import views
app_name = 'Case_Management_System'

urlpatterns = [
    path('create/', views.CreateCase.as_view(), name='cms_create_case'),
    path('location/', views.StoreAndRetrieveLocation.as_view(), name='cms_location'),
    path('virtualevidence/', views.StoreAndRetrieveVirtualEvidence.as_view(), name='cms_virtual_evidence'),
    path('physicalevidence/', views.StoreAndRetrievePhysicalEvidence.as_view(), name='cms_physical_evidence'),
    path('poi/', views.StoreAndRetrievePersonOfInterest.as_view(), name='cms_person_of_interest'),
    path('addlanguage/', views.AddLanguagesToPOI.as_view(), name='cms_add_language'),
    #path('target_response/',views.Target_Response.as_view(),name='target_response'),


]