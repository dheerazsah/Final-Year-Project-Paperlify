from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# class Registration(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     fname = models.CharField(max_length=100, default='none')
#     email = models.EmailField(unique=True, default='none')
#     password = models.CharField(max_length=128, default='none')

#     class Meta:
#         db_table = 'user'

#     def __str__(self):
#         return self.username

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    
class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_name = models.FileField(max_length=100)
    doc_size = models.BigIntegerField() 
    doc_type = models.CharField(max_length=100)
    extracted_text = models.TextField(blank=True, null=True) 
    summarized_text = models.TextField(blank=True, null=True) 

    class Meta:
        db_table = 'document'

    def __str__(self):
        return self.doc_name

from django.contrib.auth.models import User 
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs'  # Specify the desired table name

    def __str__(self):
        return f"{self.user.username} - {self.activity} - {self.updated_on}"
    

    

    
