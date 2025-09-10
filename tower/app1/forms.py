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


class MonopoleDeadendForm1(forms.ModelForm):
    class Meta:
        model = MonopoleDeadend1
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MonopoleDeadendForm1, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a MonopoleDeadend
        used_structures = MonopoleDeadend1.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
        
class MonopoleDeadendForm4(forms.ModelForm):
    class Meta:
        model = MonopoleDeadend4
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MonopoleDeadendForm4, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a MonopoleDeadend
        used_structures = MonopoleDeadend4.objects.values_list('structure', flat=True)
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

class UploadedFileForm2(forms.ModelForm):
    class Meta:
        model = UploadedFile3
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = UploadedFile3.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class UploadedFileForm1(forms.ModelForm):
    class Meta:
        model = UploadedFile2
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = UploadedFile2.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
    
class UploadedFileForm4(forms.ModelForm):
    class Meta:
        model = UploadedFile4
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = UploadedFile4.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    

# *******************  Tower ********************


class TowerDeadendForm(forms.ModelForm):
    class Meta:
        model = TowerDeadend
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)

class TowerDeadendForm3(forms.ModelForm):
    class Meta:
        model = TowerDeadend3
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm3, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend3.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class TowerDeadendForm4(forms.ModelForm):
    class Meta:
        model = TowerDeadend4
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm4, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend4.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class TowerDeadendForm5(forms.ModelForm):
    class Meta:
        model = TowerDeadend5
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm5, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend5.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class tUploadedFileForm1(forms.ModelForm):
    class Meta:
        model = tUploadedFile1
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = tUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    

class tUploadedFileForm2(forms.ModelForm):
    class Meta:
        model = tUploadedFile2
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = tUploadedFile2.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class tUploadedFileForm3(forms.ModelForm):
    class Meta:
        model = tUploadedFile3
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = tUploadedFile3.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class tUploadedFileForm4(forms.ModelForm):
    class Meta:
        model = tUploadedFile4
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = tUploadedFile4.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class tUploadedFileForm5(forms.ModelForm):
    class Meta:
        model = tUploadedFile5
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = tUploadedFile5.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
    
class HDeadendForm1(forms.ModelForm):
    class Meta:
        model = HDeadend1
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm1, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = HDeadend1.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
        
    
class HUDeadendForm1(forms.ModelForm):
    class Meta:
        model = hUploadedFile1
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = hUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class HDeadendForm2(forms.ModelForm):
    class Meta:
        model = HDeadend2
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm2, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = HDeadend2.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
        
    
class HUDeadendForm2(forms.ModelForm):
    class Meta:
        model = hUploadedFile2  # Change here
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_structures = hUploadedFile2.objects.values_list('structure_id', flat=True)  # Change here
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file