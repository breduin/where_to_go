from django.db import models


class Place(models.Model):
    """
    Модель для экскурсии 
    """
    title = models.CharField(max_length=256)
    slug = models.SlugField()
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
    image = models.ImageField(upload_to='images')
    place = models.ForeignKey(Place, 
                              on_delete=models.CASCADE,
                              related_name='images'                              
                              )

    def __str__(self):
        return f"{self.pk} {self.place.title}"