from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    """
    Модель для экскурсии (локации) 
    """
    title = models.CharField(max_length=256, 
                             verbose_name='Название',
                             )
    slug = models.SlugField(verbose_name='Обозначение')
    description_short = models.CharField(max_length=512, 
                                         verbose_name='Краткое описание',
                                         )
    description_long = models.TextField(verbose_name='Детальное писание')
    lng = models.CharField(max_length=17, 
                           verbose_name='Долгота',
                           )
    lat = models.CharField(max_length=17, 
                           verbose_name='Широта',
                           )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class Image(models.Model):
    """
    Модель картинок для локации
    """
    image = models.ImageField(upload_to='images', 
                              verbose_name='Изображение'
                              )
    place = models.ForeignKey(Place, 
                              on_delete=models.CASCADE,
                              related_name='images',
                              verbose_name='Локация'                              
                              )
    position = models.SmallIntegerField(verbose_name='Позиция',
                                        default=0,
                                        )                              


    def __str__(self):
        return f"{self.position} {self.place.title}"
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['position']