from django.urls import path
from Avatar_Management_Unit import views
app_name = 'Avatar_Management_Unit'

urlpatterns = [
    # 1st submenu
    path('avatar/', views.Create_Avatar.as_view(), name='amu_avatar'),
    path('addwork/', views.Add_Work.as_view(), name='amu_add_work'),
    path('addinterest/', views.Add_Interest.as_view(), name='amu_add_interest'),
    path('addeducation/', views.Add_Education.as_view(), name='amu_add_education'),
    path('addmarriage/', views.Add_Marriage.as_view(), name='amu_add_marriage'),
    path('addskill/', views.Add_Skill.as_view(), name='amu_add_skill'),

    # ---------------------
    # 2nd submenu
    path('setting/', views.Create_Avatar.as_view(), name='amu_setting'),
    
    # ---------------------
    # 3rd submenu
    path('report/', views.Create_Avatar.as_view(), name='amu_report'),
]