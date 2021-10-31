from django.shortcuts import render, get_object_or_404
from places.models import Place
from django.http import HttpResponse


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

        # Собираем картинки для текущей локации в список
        images_list = []
        for image in place.images.all():
            images_list.append(image.image.url)
         
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

def get_place(request, **kwargs):
    pk = kwargs['pk']
    place = get_object_or_404(Place, pk=pk)
    response = HttpResponse(f'{place.title}') if place else HttpResponse('')
    return response
