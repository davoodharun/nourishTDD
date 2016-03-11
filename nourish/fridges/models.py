from django.db import models

# Create your models here.
class Storage(models.Model):
    text = models.TextField(default='')