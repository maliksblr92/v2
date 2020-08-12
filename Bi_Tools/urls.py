from django.urls import path,include
from Bi_Tools import views
# from django.contrib.auth.decorators import login_required
app_name = 'Bi_Tools'

urlpatterns = [
    path('flex/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
    path('chart', views.simple_chart, name='chart'),
    #path('keybase_visualisation', login_required(views.keybase_visualization, name='keybase_visualisation'),
    path('visualization/<str:content_type>/', views.keybase_visualization, name='visualization'),
]