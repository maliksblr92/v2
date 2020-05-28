from django.urls import path,include
from Bi_Tools import views

app_name = 'Bi_Tools'

urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
]