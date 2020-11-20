from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    comments = models.IntegerField()
    author = models.CharField(max_length=100)
    large_category = models.CharField(max_length=20)
    small_category = models.CharField(max_length=20)
    publisher = models.CharField(max_length=100)
    img = models.CharField(max_length=50)
    price = models.FloatField()
    rate = models.IntegerField()