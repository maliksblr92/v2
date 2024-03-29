from django.urls import path
from Portfolio_Management_System import views
app_name = 'Portfolio_Management_System'
# from django.contrib.auth.decorators import login_required
urlpatterns = [

    path('search_portfolio/',views.Search_Portfolio.as_view(),name='search_portfolio'),
    # path('test/', views.test_view, name='test')
    path('create/', views.Create_Portfolio.as_view(), name='create_portfolio'),
    path('add_information/<str:portfolio_id>', views.Add_Extras.as_view(), name='add_information'),
    path('add_information/', views.Add_Extras.as_view(), name='add_information'),
    path('archive/', views.Archive.as_view(), name='archive'),
    path('overview/', views.Overview.as_view(), name='overview'),
    path('explore/', views.Explore.as_view(), name='explore'),
    path('explore/<str:porfolio_id>', views.Explore_By_GTR.as_view(), name='Explore_By_GTR'),
    path('portfolio_links/<str:portfolio_id>', views.Portfolio_Links.as_view(), name='portfolio_links'),
    path('portfolio_links_analysis/<str:portfolio_id>', views.Portfolio_Link_Analysis.as_view(), name='portfolio_links_analysis')
]
