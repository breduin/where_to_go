"""
Команда для загрузки локаций.
"""
import os
import json
import re
from urllib.parse import urlparse
from io import BytesIO
import requests
from loguru import logger
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.db.utils import IntegrityError
from django.utils.text import slugify

from ...models import Place, Image, lat_validators, lng_validators


logger.add('logs/load_places.log', format="{time} {level} {message}", rotation="1 MB", level='ERROR')

class Command(BaseCommand):
    """
    Команда оболочки Django, загружает JSON с параметрами
    локации и записывает локацию в БД.
    Запускается так:
    ./management.py load_place <str: url json-файла>
    """
    help = 'Imports JSON files and creates places.'

    def add_arguments(self, parser):
        """
        Добавляет аргумент команды в словарь options.
        """
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Загружает JSON файл, создает и записывает в БД объект Place.
        """
        for json_url in options['urls']:

            r = requests.get(json_url)

            r.raise_for_status()
            place_details = r.json()          
            
            if 'error' in place_details:
                logger.error(f'Ответ сервера в теле JSON содержит "error". Файл получен из {json_url}')
                raise requests.exceptions.HTTPError(place_details['error'])

            longitude = Decimal(place_details["coordinates"]["lng"])
            latitude = Decimal(place_details["coordinates"]["lat"])
            for lng_validator, lat_validator in zip(lng_validators, lat_validators):
                lng_validator(longitude)
                lat_validator(latitude)

            self.stdout.write(f"Загружается локация {place_details['title']}")

            try:
                place, pcreated = Place.objects.get_or_create(
                                slug=slugify(place_details['title'], allow_unicode=True),
                                defaults={
                                'title': place_details['title'],
                                'description_short': place_details["description_short"],
                                'description_long': place_details["description_long"],
                                'lng': longitude,
                                'lat': latitude
                                }
                                )
                place_status = 'записана'
            except IntegrityError:
                pcreated = False

            if not pcreated:
                self.stdout.write('Такая запись уже есть.')
                to_load_yes_or_no = input('Загрузить картинки из данного JSON-файла? (y/n)')
                if to_load_yes_or_no.lower() not in ['y', 'yes', 'yeap', 'д', 'да', 'ага']:
                    continue
                else:
                    place = Place.objects.get(title=place_details['title'])
                    place_status = 'обновлена'

            images_urls = place_details["imgs"]
            for image_url in images_urls:
                im = requests.get(image_url)
                image_raw = ImageFile.open(BytesIO(im.content))
                image_file_name=os.path.basename(urlparse(image_url).path)
                self.stdout.write(f'Загружен файл {image_file_name}')
                image = Image(place=place)
                image.image.save(image_file_name, image_raw)

            self.stdout.write(self.style.SUCCESS(f'Успешно {place_status} локация {place.title}'))
