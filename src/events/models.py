from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.TextField()
    description = models.TextField()
    start_date = models.TextField()
    end_date = models.TextField()
    
