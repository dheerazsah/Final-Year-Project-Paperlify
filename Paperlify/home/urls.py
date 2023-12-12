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
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('resetpassword', views.resetpassword, name='resetpassword'),
    path('homepage', views.homepage, name='homepage'),
    path('dashboard2nd', views.dashboard2nd, name='dashboard2nd'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('test', views.test, name='test'),
    path('mydocuments', views.mydocuments, name='mydocuments'),
    path('mydocuments/<slug>', views.document_detail, name='document_detail')
    #path('<str:slug>', views.document, name='document'), 
    #path('document', views.document, name='document'),
]
