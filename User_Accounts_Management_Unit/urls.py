from django.urls import path,include
from User_Accounts_Management_Unit import views
from rest_framework import routers
app_name = 'User_Accounts_Management_Unit'

urlpatterns = [
    path('',views.User_Login.as_view(),name='user_login'),
    path('logout/',views.User_Logout.as_view(),name='user_logout'),
    path('do_login/',views.do_login,name = 'do_login'),
    path('do_logout/',views.do_logout,name='do_logout'),
]