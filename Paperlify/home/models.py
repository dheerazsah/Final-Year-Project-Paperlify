from django.db import models
from django.utils import timezone


# class Registration(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     fname = models.CharField(max_length=100, default='none')
#     email = models.EmailField(unique=True, default='none')
#     password = models.CharField(max_length=128, default='none')

#     class Meta:
#         db_table = 'user'

#     def __str__(self):
#         return self.username
    
class FileUpload(models.Model):
    doc_name = models.FileField(max_length=100)
    doc_size = models.BigIntegerField() 
    doc_type = models.CharField(max_length=100)
    extracted_text = models.TextField(blank=True, null=True) 
    summarized_text = models.TextField(blank=True, null=True) 

    class Meta:
        db_table = 'document'

    def __str__(self):
        return self.doc_name

    

    

    
