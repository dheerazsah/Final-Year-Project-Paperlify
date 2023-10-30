from django.contrib import admin

# Register your models here.
from .models import UserActivityLog
admin.site.register(UserActivityLog)