from django.db import models


class Place(models.Model):
    """
    Модель для экскурсии 
    """
    title = models.CharField(max_length=256)
    description_short = models.CharField(max_length=512)
    description_long = models.TextField()
    lng = models.CharField(max_length=17)
    lat = models.CharField(max_length=17)

    def __str__(self):
        return self.title


class Image(models.Model):
    """
    Модель картинок для экскурсии 
    """
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.pk} {self.title}"