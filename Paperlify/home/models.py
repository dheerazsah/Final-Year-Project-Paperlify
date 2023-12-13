
#Importing the models from Django for defining database models
from django.db import models
#Importing the User model from Django for user authentication 
from django.contrib.auth.models import User
#Importing AbstractUser for creating a custom user model 
from django.contrib.auth.models import AbstractUser
#Importing the slugify function for generating slugs from text
from django.utils.text import slugify
#Importing the timezone module for handling date and time
from django.utils import timezone

#Importing modules for generating random strings
#Using random.choices()
import string 
import random

#Custom User model extending Abstract User
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) #EmailField for storing the user's email, set as unique
    otp = models.CharField(max_length=6, null=True, blank=True) #CharField with a maximum length of 6, storing a one-time password (OTP), can be null or blank
    otp_created_at = models.DateTimeField(null=True, blank=True) #DateTimeField, capturing the timestamp when the OTP is created, can be null or blank

    #Many-to-many relationship with groups is implemented
    groups = models.ManyToManyField(
        'auth.Group', #Allowing a user to belong to multiple groups
        related_name='custom_user_set', #Provide aliases for querying related objects
        related_query_name='custom_user', #Provide aliases for querying related objects
        blank=True, #Allows a user to belong to no groups (optional).
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', #Describes the purpose of the field, explaining the impact on user permissions
    )

    #Many-to-Many relationship with auth.Permission, granting specific permissions to a user
    user_permissions = models.ManyToManyField(
        'auth.Permission', #Granting specific permissions to a user
        related_name='custom_user_set', 
        related_query_name='custom_user', 
        blank=True,
        help_text='Specific permissions for this user.',
    )

#Function to generate a random string of length N 
def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k =N)) #Generating a random string of length N using random.choices
    return res #Returning generated random string

#Function to generate a unique slug for FileUpload model
def generate_slug(text):
    new_slug = slugify(text) #Generating a new slug using the slugify function
    if FileUpload.objects.filter(slug = new_slug).exists(): #Checking if the generated slug already exists in ileUploal model
        generate_slug(text + generate_random_string(5))  #If it does, recursively call generate_slug function with an appended random string
    return new_slug #Return final unique slug

#Model for File Upload with various fields 
class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #ForeignKey to the User model, representing the user who uploaded the file
    #doc_name = models.FileField(max_length=100)
    doc_name = models.TextField(max_length=100) #TextField with a maximum length of 100 characters, storing the name of the uploaded document
    doc_size = models.BigIntegerField() #BigIntegerField for storing the size of the document
    doc_type = models.CharField(max_length=100) #CharField with a maximum length of 100 characters, representing the type of the document
    extracted_text = models.TextField(blank=True, null=True) #TextField allowing storage of extracted text from the document (optional and can be null)
    summarized_text = models.TextField(blank=True, null=True) #TextField for storing summarized content from the document (optional and can be null)
    slug = models.SlugField(max_length=1000, null=True, blank=True) #SlugField with a maximum length of 1000 characters, used for generating a unique URL
    #created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now) #DateTimeField storing the timestamp when the document was created, with a default value of the current time
    updated_at = models.DateTimeField(auto_now=True) #DateTimeField set to auto_now, updating the timestamp whenever the document is modified.

    #Specifying the desired table name for the file uploads 
    class Meta:
        db_table = 'document'

    #__str__ method returns the doc_name for a human-readable representation of the FileUpload model instances
    def __str__(self):
        return self.doc_name
    
    #Override save method to generate and assign a unique slug
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.doc_name) #Sets slug field using generate_slug function based on doc_name before saving
        super(FileUpload, self).save(*args, **kwargs) #Calls original save method using super to preserve standard save behavior

#Model for User Activity Log
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #ForeignKey to the User model, indicating the associated user for the activity log
    activity = models.CharField(max_length=100) #CharField storing the type of activity with a maximum length of 100 characters
    ip_address = models.GenericIPAddressField() #GenericIPAddressField to store the IP address associated with the activity
    updated_on = models.DateTimeField(auto_now_add=True) #DateTimeField set to auto_now_add, capturing the timestamp when the log entry is created.

    #Specifying the desired table name for the activity
    class Meta:
        db_table = 'logs'

    #__str__ method creates a string representation of UserActivityLog instance, combining the data 
    def __str__(self):
        return f"{self.user.username} - {self.activity} - {self.updated_on}"
    
# class Registration(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     fname = models.CharField(max_length=100, default='none')
#     email = models.EmailField(unique=True, default='none')
#     password = models.CharField(max_length=128, default='none')

#     class Meta:
#         db_table = 'user'

#     def __str__(self):
#         return self.username
    

    

    
