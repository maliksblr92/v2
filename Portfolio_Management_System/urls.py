from django.urls import path
from Portfolio_Management_System import views
app_name = 'Portfolio_Management_System'

urlpatterns = [

    path('search_portfolio/',views.Search_Portfolio.as_view(),name='search_portfolio'),
    # path('test/', views.test_view, name='test')
    path('create/', views.Create.as_view(), name='Create'),
    path('link/', views.Link.as_view(), name='Link'),
    path('archive/', views.Archive.as_view(), name='Archive'),
    path('overview/', views.Overview.as_view(), name='Overview'),
]
