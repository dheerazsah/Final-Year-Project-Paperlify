"""
URL configuration for Paperlify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from home import views

urlpatterns = [
    path('', views.signupPage, name='signup'),
    path('login', views.loginPage, name='login'),
    path('signup', views.signupPage, name='signup'),
    path('homepage', views.homepage, name='homepage'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard2nd', views.dashboard2nd, name='dashboard2nd'),
    path('mydocuments', views.mydocuments, name='mydocuments'),
    path('document', views.document, name='document'),
    path('test', views.test, name='test'),
]
