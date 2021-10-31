from django.contrib import admin
from .models import Place, Image
from .forms import PlaceForm
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin


admin.site.register(Image)


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['thumbnail',]

    def thumbnail(self, obj):
        return format_html('<img src="{url}" height={height} />',
            url = obj.image.url,
            height=100
            )
    thumbnail.short_description = "Предпросмотр"



@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    def get_form(self, request, obj=None, **kwargs):
        return PlaceForm
