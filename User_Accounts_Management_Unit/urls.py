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
    path('add_user_profile/',views.Add_User_Profile.as_view(), name='add_user_profile'),
    path('all_user_profile/',views.All_User_Profile.as_view(), name='all_user_profile'),
    path('update_user_profile/<str:id>/',views.Update_User_Profile.as_view(), name='update_user_profile')
]