from django import forms
from .models import *

class StructureForm(forms.ModelForm):
    class Meta:
        model = ListOfStructure
        fields = ['structure']
        
        

class MonopoleDeadendForm(forms.ModelForm):
    class Meta:
        model = MonopoleDeadend
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MonopoleDeadendForm, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a MonopoleDeadend
        used_structures = MonopoleDeadend.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)




import os
from django.core.exceptions import ValidationError

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile1
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = UploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

