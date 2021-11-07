"""
Модели (структура БД) приложения places
"""
from django.core.validators import RegexValidator
from django.db import models


# Валидатор для координат
coordinates_validator = RegexValidator(regex=r'^-?[1]?\d{1,2}\.\d{0,14}$',
                             message="Географические координаты должны быть в формате: "
                                     "'55.1234567' или '-134.1234567'.")

class Place(models.Model):
    """
    Модель для экскурсии (локации)
    """
    title = models.CharField(max_length=256,
                             verbose_name='Название',
                             unique=True
                             )
    slug = models.SlugField(verbose_name='Обозначение',
                            unique=True, 
                            help_text='Напишите уникальное условное обозначение локации, например "moscow-legends2021"'
                            )
    description_short = models.CharField(max_length=512,
                                         verbose_name='Краткое описание',
                                         null=True,
                                         blank=True
                                         )
    description_long = models.TextField(verbose_name='Детальное описание',
                                        null=True,
                                        blank=True
                                        )
    lng = models.CharField(max_length=17,
                           verbose_name='Долгота',
                           validators=[coordinates_validator],
                           )
    lat = models.CharField(max_length=17,
                           verbose_name='Широта',
                           validators=[coordinates_validator],
                           )

    def __str__(self):
        return self.title

    class Meta:
        """
        Мета-опции класса Place
        """
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
        """
        Мета-опции класса Image
        """
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['position']
