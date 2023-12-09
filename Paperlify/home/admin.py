from django.contrib import admin

# Register your models here.
from .models import UserActivityLog
admin.site.register(UserActivityLog)

from .models import FileUpload
admin.site.register(FileUpload)