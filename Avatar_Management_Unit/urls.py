from django.urls import path
from Avatar_Management_Unit import views
app_name = 'Avatar_Management_Unit'

urlpatterns = [
    path('avatar/', views.Create_Avatar.as_view(), name='amu_avatar'),
    path('setting/', views.Create_Avatar.as_view(), name='amu_setting'),
    path('report/', views.Create_Avatar.as_view(), name='amu_report')
]