"""
Модели (структура БД) приложения places
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from tinymce.models import HTMLField


# Валидатор для координат
lng_validator_message = 'Долгота должна быть в диапазоне от -180 до 180'
lng_validators = [
    MinValueValidator(-180, lng_validator_message),
    MaxValueValidator(180, lng_validator_message)
                 ]
lat_validator_message = 'Широта должна быть в диапазоне от -90 до 90'
lat_validators = [
    MinValueValidator(-90, lat_validator_message),
    MaxValueValidator(90, lat_validator_message)
                 ] 

class Place(models.Model):
    """
    Модель для экскурсии (локации)
    """
    title = models.CharField(max_length=256,
                             verbose_name='Название',
                             default='',
                             )
    slug = models.SlugField(verbose_name='Обозначение',
                            unique=True, 
                            help_text='Напишите уникальное условное обозначение локации, например "moscow-legends2021"'
                            )
    description_short = models.TextField(verbose_name='Краткое описание',
                                         blank=True,
                                         default=''
                                        )
    description_long = HTMLField(verbose_name='Детальное описание',
                                 blank=True,
                                 default=''
                                 )
    lng = models.DecimalField(max_digits=17, 
                              decimal_places=14,
                              verbose_name='Долгота',
                              validators=lng_validators,
                             )
    lat = models.DecimalField(max_digits=17, 
                              decimal_places=14,
                              verbose_name='Широта',
                              validators=lat_validators,
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
                                        blank=True,
                                        db_index=True
                                        )


    def __str__(self):
        return f"{self.position} {self.place.title}"

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['position']
