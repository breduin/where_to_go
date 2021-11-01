# Куда пойти

*Веб-приложение, которое покажет тебе на карте самые красивые и необычные места поблизости, о которых ты, возможно, даже и не подозревал. Конечно же, ты можешь добавить свои любимые локации. Фотографии и описание, удобная навигация - всё для того, чтобы провести время с пользой.*

![Скриншот приложения](where_to_go_screenshot.png)

Демо-версия: http://tolegu.pythonanywhere.com/

Добавление новых локаций, фотографий и описаний ты можешь осуществлять через удобную админку, она здесь: http://tolegu.pythonanywhere.com/admin/

## Установка

Приложение является свободным, ты можешь установить его и пользоваться. Для этого тебе понадобятся:
1. Python 3.6+ [см. как установить (англ.)](https://realpython.com/installing-python/), а [здесь для Debian-based (рус.)](http://userone.ru/?q=node/41).
2. Django 3.x [см. как установить (рус.)](https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/development_environment).

Необходимые библиотеки для Django указаны в файле requirements.txt.

Фронтенд представляет собой готовый шаблон. В качестве карты используется [Openstreetmap](https://www.openstreetmap.org). Для работы шаблона используются следующие javascript- и css-библиотеки:
* [Leaflet](https://leafletjs.com/) — отрисовка карты
* [loglevel](https://www.npmjs.com/package/loglevel) для логгирования
* [Bootstrap](https://getbootstrap.com/) — CSS библиотека
* [Vue.js](https://ru.vuejs.org/) — реактивные шаблоны на фронтенде

Всё включено и настроено :)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).

