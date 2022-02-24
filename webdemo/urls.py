"""webdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from webapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='home-page'),
    path('session', views.sessions, name='session-page'),
    path('connectsvr', views.connect),
    path('profile', views.profileid, name='profile-page'),
    path('search', views.search, name='search-page'),
    path('datauser', views.datauser),
    path('rundsar', views.rundsar, name='rundsar-page'),
    path('viewreports', views.viewreports, name='DSAR-report-page'),
    path('scanhistory', views.scanhistory, name='scanhistory-page'),
]
