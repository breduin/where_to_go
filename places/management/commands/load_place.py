"""
Команда для загрузки локаций.
"""
import os
import json
from urllib.parse import urlparse
from io import BytesIO
import requests
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.db.utils import IntegrityError

from places.utilities import get_random_string
from places.models import Place, Image


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
            r = requests.get(json_url)
            try:
                place_json = r.json()
            except json.JSONDecodeError:
                self.stdout.write("Ошибка декодирования JSON. Проверьте URL и целостность JSON-файла.")
                exit()

            self.stdout.write(f"Загружается локация {place_json['title']}")
            # Создаём локацию
            try:
                place, pcreated = Place.objects.get_or_create(
                                title=place_json['title'],
                                # В качестве slug берём случайную строку
                                # TODO Можно зациклить с проверкой есть ли уже такой slug в записях
                                slug=get_random_string(),
                                description_short=place_json["description_short"],
                                description_long=place_json["description_long"],
                                lng=place_json["coordinates"]["lng"],
                                lat=place_json["coordinates"]["lat"]
                                )
                place_status = 'записана'
            except IntegrityError:
                to_load_yes_or_no = ''
                pcreated = False

            # Если такая запись есть, спрашиваем, загружать ли картинки по списку
            # (это могут быть дополнительные картинки, которые не были ранее загружены)
            # Если да, то берём проверенный выше Place и цепляем картинки к нему.
            if not pcreated:
                self.stdout.write('Такая запись уже есть.')
                to_load_yes_or_no = input('Загрузить картинки из данного JSON-файла? (y/n)')
                if to_load_yes_or_no.lower() not in ['y', 'yes', 'yeap', 'д', 'да', 'ага']:
                    exit()
                else:
                    place = Place.objects.get(title=place_json['title'])
                    place_status = 'обновлена'

            # Загружаем картинки по списку url-ов
            images_urls = place_json["imgs"]
            for image_url in images_urls:
                im = requests.get(image_url)
                image_raw = ImageFile.open(BytesIO(im.content))
                image_file_name=os.path.basename(urlparse(image_url).path)
                self.stdout.write(f'Загружен файл {image_file_name}')
                image = Image(place=place)
                image.image.save(image_file_name, image_raw)

            self.stdout.write(self.style.SUCCESS(f'Успешно {place_status} локация {place.title}'))
