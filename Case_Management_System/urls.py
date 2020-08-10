from django.urls import path
from Case_Management_System import views
app_name = 'Case_Management_System'
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('create/', login_required(views.CreateCase.as_view()), name='cms_create_case'),
    path('location/', login_required(views.StoreAndRetrieveLocation.as_view()), name='cms_location'),
    path('virtualevidence/', login_required(views.StoreAndRetrieveVirtualEvidence.as_view()), name='cms_virtual_evidence'),
    path('physicalevidence/', login_required(views.StoreAndRetrievePhysicalEvidence.as_view()), name='cms_physical_evidence'),
    path('poi/', login_required(views.StoreAndRetrievePersonOfInterest.as_view()), name='cms_person_of_interest'),
    path('addlanguage/', login_required(views.AddLanguagesToPOI.as_view()), name='cms_add_language'),
    #path('target_response/',login_required(views.Target_Response.as_view()),name='target_response'),


]