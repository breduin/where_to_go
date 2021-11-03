"""
Формы для приложения Place
"""
from django import forms
from tinymce.widgets import TinyMCE
from .models import Place


class PlaceForm(forms.ModelForm):
    """
    Форма для локации (Place).
    """

    description_long = forms.CharField(widget=TinyMCE())

    class Meta:
        fields= '__all__'
        model = Place
