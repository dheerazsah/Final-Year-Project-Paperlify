from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.utils.text import slugify

#Generating ramdom settings 
#Using random.choices()
import string 
import random

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


def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase + 
                            string.digits, k =N))
    return res

def generate_slug(text):
    new_slug = slugify(text)
    if FileUpload.objects.filter(slug = new_slug).exists():
        generate_slug(text + generate_random_string(5))
    return new_slug

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #doc_name = models.FileField(max_length=100)
    doc_name = models.TextField(max_length=100)
    doc_size = models.BigIntegerField() 
    doc_type = models.CharField(max_length=100)
    extracted_text = models.TextField(blank=True, null=True) 
    summarized_text = models.TextField(blank=True, null=True) 
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    timeStamp = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'document'

    def __str__(self):
        return self.doc_name
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.doc_name)
        super(FileUpload, self).save(*args, **kwargs)

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
    

    

    
