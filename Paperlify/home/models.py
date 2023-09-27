from django.db import models
from django.utils import timezone

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Registration(models.Model):
    username = models.CharField(max_length=100, unique=True)
    fname = models.CharField(max_length=100, default='none')
    email = models.EmailField(unique=True, default='none')
    password = models.CharField(max_length=128, default='none')
    updatedOn = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
    

class DocumentUpload(models.Model):
    file = models.FileField()