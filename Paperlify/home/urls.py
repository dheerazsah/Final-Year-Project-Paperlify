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
#Importing necessary modules from Django
#Importing the admin module for Django admin functionality
from django.contrib import admin
#Importing the path function for defining URL patterns
from django.urls import path
#Importing views from home app
from home import views

from home.views import profile, reactivate_account

#URL patterns for the application
urlpatterns = [
    path('', views.signupPage, name='signup'), #Mapping the root URL to the signupPage view
    path('login', views.loginPage, name='login'), #Mapping '/login' to the loginPage view
    path('signup', views.signupPage, name='signup'), #Mapping '/signup' to the signupPage view
    path('forgotpassword', views.forgotpassword, name='forgotpassword'), #Mapping '/forgotpassword' to the forgotpassword view
    path('send_otp', views.send_otp, name='send_otp'), #Mapping '/send_otp' to the send_otp view
    path('verify_otp', views.verify_otp, name='verify_otp'), #Mapping '/verify_otp' to the verify_otp view
    path('resetpassword', views.resetpassword, name='resetpassword'), #Mapping '/resetpassword' to the resetpassword view
    path('confirmpassword', views.confirmpassword, name='confirmpassword'),
    path('homepage', views.homepage, name='homepage'), #Mapping '/homepage' to the homepage view
    path('dashboard2nd', views.dashboard2nd, name='dashboard2nd'), #Mapping '/dashboard2nd' to the dashboard2nd view
    path('dashboard', views.dashboard, name='dashboard'), #Mapping '/dashboard' to the dashboard view

    path('upload', views.upload_file, name='upload_file'),
    path('summarize', views.summarize_text, name='summarize_text'),

    path('profile', views.profile, name='profile'), #Mapping '/profile' to the profile view
    path('test', views.test, name='test'), #Mapping '/test' to the test view
    path('mydocuments', views.mydocuments, name='mydocuments'), #Mapping '/mydocuments' to the mydocuments view
    path('mydocuments/<slug>', views.document_detail, name='document_detail'), #Mapping '/mydocuments/<slug>' to the document_detail view
    path('search', views.search, name='search'), #Mapping '/search' to the search view
    path('reactivate_account/<str:token>/', views.reactivate_account, name='reactivate_account'),
    #path('<str:slug>', views.document, name='document'), 
    #path('document', views.document, name='document'),
]
