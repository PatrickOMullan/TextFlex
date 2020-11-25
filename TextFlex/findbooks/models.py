from django.db import models

# Create your models here.
class Term(models.Model):
    title = models.CharField()
    Img = models.ImageField()
    