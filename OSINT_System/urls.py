"""OSINT_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
import multiprocessing
import time
import os

from OSINT_System_Core.rabbit_thread import Rabbit_Consumer
consumer = Rabbit_Consumer(1)
#consumer.start()


urlpatterns = [
    path('core/', include('OSINT_System_Core.urls')),
    path('admin/', admin.site.urls),
    path('avatar_management/', include('Avatar_Management_Unit.urls')),
    path('dpu/', include('Data_Processing_Unit.urls')),
    path('data_acquisition/', include('Public_Data_Acquisition_Unit.urls')),
    path('system_log/', include('System_Log_Management_Unit.urls')),
    path('', include('User_Accounts_Management_Unit.urls')),
    path('tms/', include('Target_Management_System.urls')),
    path('pms/', include('Portfolio_Management_System.urls')),
    path('kms/', include('Keybase_Management_System.urls')),
    path('cms/', include('Case_Management_System.urls')),
]
