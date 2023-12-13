#Importing necessary modules from Django for admin functionality
from django.contrib import admin

#Importing models for UserActivityLog from the current app for registration in the Django admin
from .models import UserActivityLog
#Registering UserActivityLog model
admin.site.register(UserActivityLog)

#Importing models for FileUpload from the current app for registration in the Django admin
from .models import FileUpload
#Registering FileUpload model
admin.site.register(FileUpload)