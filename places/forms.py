from django import forms
from tinymce.widgets import TinyMCE
from .models import Place


class PlaceForm(forms.ModelForm):

    description_long = forms.CharField(widget=TinyMCE())

    class Meta:
        fields= '__all__'
        model = Place