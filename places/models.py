from django.db import models

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length=256)
    description_short = models.CharField(max_length=512)
    description_long = models.TextField()
    lng = models.CharField(max_length=17)
    lat = models.CharField(max_length=17)

    def __str__(self):
        return self.title