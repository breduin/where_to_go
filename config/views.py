from django.shortcuts import render, get_object_or_404
from places.models import Place
from django.http import HttpResponse, JsonResponse


def start_page(request):
    """
    Представление для главной страницы, выводит карту и список локаций.
    """
    places = Place.objects.all()

    places_json = {
      "type": "FeatureCollection",
        "features": []
    }
    for place in places:
         
        props = {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [place.lng, place.lat]
          },
          "properties": {
            "title": place.title,
            "placeId": place.slug,
            "detailsUrl": "",
          }
        }
        places_json["features"].append(props)

    context ={}
    context['places'] = places_json
    return render(request, 'frontend/index.html', context)

def get_place_info(request, **kwargs):
    try:
        pk = kwargs['pk']
    except KeyError():
        return HttpResponse('Локация с таким id не найдена. Проверьте запрос.')
    
    place = get_object_or_404(Place, pk=pk)

    # Собираем картинки для текущей локации в список
    images_list = []
    for image in place.images.all():
        images_list.append(image.image.url)

    # Формируем словарь данных о локации.
    place_info = {
        "title": place.title,
        "imgs": images_list,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng, 
            "lat": place.lat
            }
     }

    # Формируем JSON ответ.
    response = JsonResponse(place_info, safe=False,
                            json_dumps_params={'indent': 2, 
                                               'ensure_ascii': False,
                                              }
                            )

    return response
