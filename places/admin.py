"""
Обепечение для административной панели сайта
"""
from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib.auth.models import User
from .models import Place, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Класс для изображений в административной панели.
    """
    search_fields = ('place', ) 

    def has_module_permission(self, request):
        return request.user.is_superuser



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
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ImageInline,
    ]
