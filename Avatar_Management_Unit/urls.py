from django.urls import path
from Avatar_Management_Unit import views
app_name = 'Avatar_Management_Unit'

urlpatterns = [
    # 1st submenu
    path('avatar/', views.Create_Avatar.as_view(), name='amu_avatar'),
    path('addwork/<str:details_type>/<str:avatar_id>/', views.Add_Work.as_view(), name='amu_add_work'),
    path('addinterest/', views.Add_Interest.as_view(), name='amu_add_interest'),
    path('addeducation/', views.Add_Education.as_view(), name='amu_add_education'),
    path('addmarriage/', views.Add_Marriage.as_view(), name='amu_add_marriage'),
    path('addbiography/', views.Add_Biography.as_view(), name='amu_add_biography'),
    path('addsocialaccount/', views.Add_Social_Account.as_view(), name='amu_add_socialaccount'),
    path('addsocialpost/', views.Add_Social_Post.as_view(), name='amu_add_socialpost'),
    path('addskill/', views.Add_Skill.as_view(), name='amu_add_skill'),

    # ---------------------
    # 2nd submenu
    path('setting/', views.Create_Avatar.as_view(), name='amu_setting'),
    
    # ---------------------
    # 3rd submenu
    path('report/', views.Create_Avatar.as_view(), name='amu_report'),
    path('send_message/', views.Action_Send_Message.as_view(), name='send_message'),
    path('send_message/<str:target_username>', views.Action_Send_Message.as_view(), name='send_message'),
    path('archive/', views.Archive.as_view(), name='archive'),
]