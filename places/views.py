"""
Представления для приложения places.
"""

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from places.models import Place


def start_page(request):
    """
    Представление для главной страницы, выводит карту и список локаций.
    """
    places = Place.objects.all()

    places_on_map = {
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
            "detailsUrl": reverse('place_details', args=[place.pk]),
          }
        }
        places_on_map["features"].append(props)

  
    context = {
      'places': places_on_map,
      }
    return render(request, 'frontend/index.html', context)

def get_place_details(request, **kwargs):
    """
    Возвращает JSON с информацией о локации с данным pk.
    """
    pk = kwargs['pk']

    place = get_object_or_404(Place, pk=pk)

    images_list = []
    for image in place.images.all():
        images_list.append(image.image.url)

    place_details = {
        "title": place.title,
        "imgs": images_list,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
            }
     }

    response = JsonResponse(place_details, safe=False,
                            json_dumps_params={'indent': 2,
                                               'ensure_ascii': False,
                                              }
                            )

    return response
