"""webapp URL Configuration

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
from django.urls import path, re_path
from django.conf.urls import include, url
from . import views
from . import azure_auth
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    url(r'^', include(router.urls)),
    re_path(r'^', include('webapp.user_management.urls')),
    re_path(r'^home$', views.index, name='index'), # FE: homepage after login
    re_path(r'^login', views.login, name='login'), # FE: redirect to Azure login. "launch platform" btn
    re_path(r'^logout', views.logout, name='logout'), # FE: logout user
    re_path(r'^auth', azure_auth.authorized, name='authorized'),
]
