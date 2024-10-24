from django import forms
from .models import ListOfStructure

class StructureForm(forms.ModelForm):
    class Meta:
        model = ListOfStructure
        fields = ['structure']
