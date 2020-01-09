from django.db import models
from datetime import datetime


# Create your models here.
class UserProfile(models.Model):
    uuid = models.CharField(max_length=36)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, null=True)
    job_title = models.CharField(max_length=100, null=True)
    creator = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(default=datetime.utcnow)
    
    class Meta:
        app_label = 'webapp'
        db_table = 'user_profile'
