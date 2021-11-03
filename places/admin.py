"""
Обепечение для административной панели сайта
"""
from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Place, Image
from .forms import PlaceForm


admin.site.register(Image)


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    """
    Класс для панели редактирования картинок на одной странице
    с редактированием локации.
    """
    model = Image
    extra = 0
    readonly_fields = ['thumbnail',]

    @staticmethod
    def thumbnail(obj):
        """
        Выводит миниатюру для предпросмотра.

        Высота миниатюры задаётся параметром height. Ширина миниатюры
        устанавливается браузером автоматически из пропорций оригинала.
        """
        return format_html('<img src="{url}" height={height} />',
            url = obj.image.url,
            height=100
            )
    thumbnail.short_description = "Предпросмотр"



@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """
    Класс для отображения локации в административной панели.
    """
    search_fields = ('title', )
    inlines = [
        ImageInline,
    ]
    form = PlaceForm
