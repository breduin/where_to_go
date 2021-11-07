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

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.db.utils import IntegrityError

from ...utilities import get_random_string
from ...models import Place, Image, coordinates_validator


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

            # Получаем JSON по url из аргумента команды
            try:
                r = requests.get(json_url)
            except Exception as e:
                logger.error(f'Ошибка соединения с сервером {e}. Адрес {json_url}')
                self.stdout.write(f"При попытке соединения с сервером возникла ошибка {e}")
                exit()

            # Проверка запроса
            if not r.ok:
                logger.error(f'Ошибка соединения с сервером. Адрес {json_url}')
                self.stdout.write("Ошибка соединения с сервером. Возможно, файл перемещён. Проверьте правильность URL и попробуйте соединиться позже.")
                exit()
                
            try:
                place_details = r.json()
            except json.JSONDecodeError:
                logger.error(f'Ошибка декодирования JSON. Файл получен из {json_url}')
                self.stdout.write("Ошибка декодирования JSON. Проверьте URL и целостность JSON-файла.")
                exit()            
            
            if 'error' in place_details:
                logger.error(f'Ответ сервера в теле JSON содержит "error". Файл получен из {json_url}')
                raise requests.exceptions.HTTPError(decoded_response['error'])

            # Валидация координат
            longitude = place_details["coordinates"]["lng"]
            latitude = place_details["coordinates"]["lat"]
            if not all([bool(re.match(coordinates_validator.regex, longitude)), 
                    bool(re.match(coordinates_validator.regex, latitude))
                    ]):
                self.stdout.write(f"Получено: долгота '{longitude}' и широта '{latitude}'.")    
                self.stdout.write("Координаты не соответствуют формату '55.1234567' или '-134.1234567'. Локация не загружена.")
                exit()

            self.stdout.write(f"Загружается локация {place_details['title']}")
            # Создаём локацию
            try:
                place, pcreated = Place.objects.get_or_create(
                                title=place_details['title'],
                                # В качестве slug берём случайную строку
                                # TODO Можно зациклить с проверкой есть ли уже такой slug в записях
                                slug=get_random_string(),
                                defaults={
                                'description_short': place_details["description_short"],
                                'description_long': place_details["description_long"],
                                'lng': longitude,
                                'lat': latitude
                                }
                                )
                place_status = 'записана'
            except IntegrityError:
                to_load_yes_or_no = ''
                pcreated = False

            # Если такая запись есть, спрашиваем, загружать ли картинки по списку
            if not pcreated:
                self.stdout.write('Такая запись уже есть.')
                to_load_yes_or_no = input('Загрузить картинки из данного JSON-файла? (y/n)')
                if to_load_yes_or_no.lower() not in ['y', 'yes', 'yeap', 'д', 'да', 'ага']:
                    exit()
                else:
                    place = Place.objects.get(title=place_details['title'])
                    place_status = 'обновлена'

            # Загружаем картинки по списку url-ов
            images_urls = place_details["imgs"]
            for image_url in images_urls:
                im = requests.get(image_url)
                image_raw = ImageFile.open(BytesIO(im.content))
                image_file_name=os.path.basename(urlparse(image_url).path)
                self.stdout.write(f'Загружен файл {image_file_name}')
                image = Image(place=place)
                image.image.save(image_file_name, image_raw)

            self.stdout.write(self.style.SUCCESS(f'Успешно {place_status} локация {place.title}'))
