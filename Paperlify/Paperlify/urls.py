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
from django.contrib import admin #Importing the admin module for Django admin functionality
from django.urls import path, include #Importing functions for defining URL patterns of the app
from django.conf import settings #Importing the settings module to access project settings
from django.conf.urls.static import static #Importing static function to serve static files

#URL patterns for the entire project
urlpatterns = [
    path('admin/', admin.site.urls), #Mapping '/admin/' to the Django admin site
    path('', include('home.urls')), #Including URLs defined in home app
] 

#Conditionally adding URL patterns for serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #Adding patterns for serving static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Adding patterns for serving media files
