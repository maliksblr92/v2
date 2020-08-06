from django.urls import path,include
from User_Accounts_Management_Unit import views
from rest_framework import routers
app_name = 'User_Accounts_Management_Unit'

urlpatterns = [
path('',views.User_Login.as_view(),name='user_login'),
    path('login/',views.User_Login.as_view(),name='user_login'),
    path('logout/',views.User_Logout.as_view(),name='user_logout'),
    path('do_login/',views.do_login,name = 'do_login'),
    path('do_logout/',views.do_logout,name='do_logout'),
    # Ahmed Routes
    # user_profile_routes
    path('add_user_profile/',views.Add_User_Profile.as_view(), name='add_user_profile'),
    path('all_user_profile/',views.All_User_Profile.as_view(), name='all_user_profile'),
    path('update_user_profile/<str:id>/',views.Update_User_Profile.as_view(), name='update_user_profile'),
    path('delete_user_profile/<str:id>/',views.Delete_User_Profile.as_view(), name='delete_user_profile'),
    # user-group_routes
    
    path('add_user_group/',views.Add_User_Group.as_view(), name='add_user_group'),
    path('delete_user_group/<str:id>/',views.Delete_User_Group, name='delete_user_group'),
    path('update_user_group/',views.Update_User_Group, name='update_user_group'),
    path('all_user_group/',views.All_User_Group.as_view(), name='all_user_group'),
    path('add_users_to_groups/',views.Add_Users_To_Groups.as_view(),name='add_users_to_groups'),
    path('remove_users_to_groups/',views.Remove_Users_To_Groups.as_view(),name='remove_users_to_groups'),
    path('get_all_group_users/<str:id>/',views.Get_All_Group_Users.as_view(),name='get_all_group_users'),
# User Routes
    path('add_user/',views.Add_User.as_view(), name='add_user'),
    path('delete_user/<str:id>/',views.Delete_User.as_view(), name='delete_user'),
    path('all_users/',views.All_Users.as_view(), name='all_users'),
    path('update_user/<str:id>/',views.Update_User.as_view(), name='update_user'),
]