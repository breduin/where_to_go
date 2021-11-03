"""
Test of models


Name of test classes:
Test{Model name}

Name of test functions: 
test_{field name}_{attrubute name to be tested}
or
test_{class method name}
or
test_meta_{Meta class option}
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Place, Image

class TestPlace(TestCase):
    """
    Тест модели Place
    """

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Place.objects.create(title='TestLocation',
                             slug='test-location',
                             description_short='Test short description',
                             description_long='Test long long description',
                             lng='34.987987',
                             lat='55.7887689'
                            )

    # Testing 'title' field
    def test_title_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('title').verbose_name
        self.assertEqual(tested_property,'Название')

    def test_title_max_length(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('title').max_length
        self.assertEqual(tested_property, 256)

    # Testing 'slug' field
    def test_slug_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('slug').verbose_name
        self.assertEqual(tested_property,'Обозначение')

    # Testing 'description_short' field
    def test_description_short_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('description_short').verbose_name
        self.assertEqual(tested_property,'Краткое описание')

    def test_description_short_max_length(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('description_short').max_length
        self.assertEqual(tested_property, 512)

    # Testing 'description_long' field
    def test_description_long_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('description_long').verbose_name
        self.assertEqual(tested_property,'Детальное писание')

    def test_description_long_internal_type(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('description_long').get_internal_type()
        self.assertEqual(tested_property,'TextField')

    # Testing 'lng' field
    def test_lng_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('lng').verbose_name
        self.assertEqual(tested_property,'Долгота')

    def test_lng_max_length(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('lng').max_length
        self.assertEqual(tested_property, 17)

    # Testing 'lat' field
    def test_lat_verbose_name(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('lat').verbose_name
        self.assertEqual(tested_property,'Широта')

    def test_lat_max_length(self):
        place = Place.objects.get(id=1)
        tested_property = place._meta.get_field('lat').max_length
        self.assertEqual(tested_property, 17)


class TestImage(TestCase):
    """
    Тест модели Image
    """

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Place.objects.create(title='TestLocation',
                             slug='test-location',
                             description_short='Test short description',
                             description_long='Test long long description',
                             lng='34.987987',
                             lat='55.7887689'
                            )
        place = Place.objects.get(id=1)
        Image.objects.create(image=SimpleUploadedFile(name='iq.jpg',
                                                      content=open('media/images/iq.jpg', 'rb').read(),
                                                      content_type='image/jpeg'),
                             place=place,
                             position=1)

    # Testing 'image' field
    def test_image_verbose_name(self):
        image = Image.objects.get(id=1)
        tested_property = image._meta.get_field('image').verbose_name
        self.assertEqual(tested_property,'Изображение')

    # Testing 'place' field
    def test_place_verbose_name(self):
        image = Image.objects.get(id=1)
        tested_property = image._meta.get_field('place').verbose_name
        self.assertEqual(tested_property,'Локация')    

    def test_place_related_model(self):
        image = Image.objects.get(id=1)
        tested_property = str(image._meta.get_field('place').related_model)
        self.assertEqual(tested_property,"<class 'places.models.Place'>")
