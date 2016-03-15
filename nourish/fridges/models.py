from django.db import models

# Create your models here.
class Fridge(models.Model):
    text = models.TextField(default='')

class Item(models.Model):
    text = models.TextField(default='')
    fridge = models.ForeignKey(Fridge, default=None)
