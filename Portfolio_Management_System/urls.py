from django.urls import path
from Portfolio_Management_System import views
app_name = 'Portfolio_Management_System'

urlpatterns = [

    path('search_portfolio/',views.Search_Portfolio.as_view(),name='search_portfolio'),
    # path('test/', views.test_view, name='test')
    path('create/', views.Create_Portfolio.as_view(), name='create_portfolio'),
    path('add_information/<str:portfolio_id>', views.Add_Extras.as_view(), name='add_information'),
    path('add_information/', views.Add_Extras.as_view(), name='add_information'),
    path('archive/', views.Archive.as_view(), name='archive'),
    path('overview/', views.Overview.as_view(), name='overview'),
    path('explore/', views.Explore.as_view(), name='explore'),
]
