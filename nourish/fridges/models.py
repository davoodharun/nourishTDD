from django.db import models

# Create your models here.
class Store(models.Model):
    text = models.TextField(default='')

class Item(models.Model):
    text = models.TextField(default='')
    store = models.ForeignKey(Store, default=None)
