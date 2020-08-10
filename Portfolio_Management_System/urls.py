from django.urls import path
from Portfolio_Management_System import views
app_name = 'Portfolio_Management_System'
from django.contrib.auth.decorators import login_required
urlpatterns = [

    path('search_portfolio/',login_required(views.Search_Portfolio.as_view()),name='search_portfolio'),
    # path('test/', login_required(views.test_view, name='test')
    path('create/', login_required(views.Create_Portfolio.as_view()), name='create_portfolio'),
    path('add_information/<str:portfolio_id>', login_required(views.Add_Extras.as_view()), name='add_information'),
    path('add_information/', login_required(views.Add_Extras.as_view()), name='add_information'),
    path('archive/', login_required(views.Archive.as_view()), name='archive'),
    path('overview/', login_required(views.Overview.as_view()), name='overview'),
    path('explore/', login_required(views.Explore.as_view()), name='explore'),
    path('explore/<str:porfolio_id>', login_required(views.Explore_By_GTR.as_view()), name='Explore_By_GTR'),
    path('portfolio_links/<str:portfolio_id>', login_required(views.Portfolio_Links.as_view()), name='portfolio_links'),
    path('portfolio_links_analysis/<str:portfolio_id>', login_required(views.Portfolio_Link_Analysis.as_view()), name='portfolio_links_analysis')
]
