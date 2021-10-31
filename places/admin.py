from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html


admin.site.register(Image)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    # TODO place thumbnail column before position column
    # fields = ('position', 'thumbnail', )
    readonly_fields = ['thumbnail',]

    def thumbnail(self, obj):
        return format_html('<img src="{url}" height={height} />',
            url = obj.image.url,
            height=200
            )
    thumbnail.short_description = "Предпросмотр"



@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
