from django import forms
from .models import *

class StructureForm(forms.ModelForm):
    class Meta:
        model = ListOfStructure
        fields = ['structure']
        
class StructureGroupForm(forms.ModelForm):
    structures = forms.ModelMultipleChoiceField(
        queryset=ListOfStructure.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'multi-select-dropdown'
        }),
        required=True
    )

    class Meta:
        model = StructureGroup
        fields = ['name', 'structures']
    

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
        
class TDeadendFormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TowerDeadend   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendFormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True

class TowerDeadendForm3(forms.ModelForm):
    class Meta:
        model = TowerDeadend3                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm3, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend3.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)

        
class TDeadend3FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TowerDeadend3   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend3FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class TowerDeadendForm4(forms.ModelForm):
    class Meta:
        model = TowerDeadend4                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm4, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend4.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)


class TDeadend4FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TowerDeadend4   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend4FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class TowerDeadendForm5(forms.ModelForm):
    class Meta:
        model = TowerDeadend5                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TowerDeadendForm5, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TowerDeadend5.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)


class TDeadend5FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TowerDeadend5   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend5FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class tUploadedFileForm1(forms.ModelForm):
    class Meta:
        model = tUploadedFile1
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    

class tUploadedUpdateForm1(forms.Form):
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile1.objects.filter(structure=structure).exists():
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
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
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile2.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class tUploadedUpdateForm2(forms.Form):
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile2.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile2.objects.filter(structure=structure).exists():
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class tUploadedFileForm3(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile3               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile3.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class tUploadedFileForm4(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile4               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile4.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class tUploadedFileForm5(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile5               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile5.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

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
        
class HDeadendForm1UpdateForm(forms.ModelForm):
    class Meta:
        model = HDeadend1
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm1UpdateForm, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
    

class HUDeadendForm1(forms.ModelForm):
    class Meta:
        model = hUploadedFile1
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        # Or keep it as a fallback for when structure is not hardcoded
        used_structures = hUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class HUDeadendUpdateForm1(forms.Form):
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = hUploadedFile1.objects.values_list('structure_id', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not hUploadedFile1.objects.filter(structure=structure).exists():
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

    
class HDeadendForm2(forms.ModelForm):
    class Meta:
        model = HDeadend2                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm2, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = HDeadend2.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class HDeadendForm2UpdateForm(forms.ModelForm):   # here
    class Meta:
        model = HDeadend2   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm2UpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
    
class HUDeadendForm2(forms.ModelForm):     # *****************
    class Meta:
        model = hUploadedFile2               # *****************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        used_structures = hUploadedFile2.objects.values_list('structure_id', flat=True)       # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class HUDeadendUpdateForm2(forms.Form):        # *****************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = hUploadedFile2.objects.values_list('structure_id', flat=True)    # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not hUploadedFile2.objects.filter(structure=structure).exists():   # *****************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class HDeadendForm3(forms.ModelForm):
    class Meta:
        model = HDeadend3                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm3, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = HDeadend3.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class HDeadendForm3UpdateForm(forms.ModelForm):   # here
    class Meta:
        model = HDeadend3   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm3UpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class HUDeadendForm3(forms.ModelForm):     # *****************
    class Meta:
        model = hUploadedFile3               # *****************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        used_structures = hUploadedFile3.objects.values_list('structure_id', flat=True)       # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class HUDeadendUpdateForm3(forms.Form):        # *****************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = hUploadedFile3.objects.values_list('structure_id', flat=True)    # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not hUploadedFile3.objects.filter(structure=structure).exists():   # *****************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class HDeadendForm4(forms.ModelForm):
    class Meta:
        model = HDeadend4                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm4, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = HDeadend4.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
class HDeadendForm4UpdateForm(forms.ModelForm):   # here
    class Meta:
        model = HDeadend4   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(HDeadendForm4UpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class HUDeadendForm4(forms.ModelForm):     # *****************
    class Meta:
        model = hUploadedFile4               # *****************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        used_structures = hUploadedFile4.objects.values_list('structure_id', flat=True)       # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

class HUDeadendUpdateForm4(forms.Form):        # *****************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = hUploadedFile4.objects.values_list('structure_id', flat=True)    # *****************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not hUploadedFile4.objects.filter(structure=structure).exists():   # *****************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class TDeadendForm6(forms.ModelForm):
    class Meta:
        model = TDeadend6                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm6, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend6.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)


class TDeadend6FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend6   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend6FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
    
class TUDeadendForm6(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile6               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile6.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TDeadend7FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend7   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend7FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class TDeadend8FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend8   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend8FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class TDeadend9FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend9   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend9FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
class TDeadend10FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend10   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend10FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True
        
        
class TDeadend11FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = TDeadend11   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadend11FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True

class TDeadendForm7(forms.ModelForm):
    class Meta:
        model = TDeadend7                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm7, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend7.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class TUDeadendForm7(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile7               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile7.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TDeadendForm8(forms.ModelForm):
    class Meta:
        model = TDeadend8                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm8, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend8.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class TUDeadendForm8(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile8               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile8.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TDeadendForm9(forms.ModelForm):
    class Meta:
        model = TDeadend9                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm9, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend9.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class TUDeadendForm9(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile9               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile9.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TDeadendForm10(forms.ModelForm):
    class Meta:
        model = TDeadend10               # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm10, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend10.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class TUDeadendForm10(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile10               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile10.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TDeadendForm11(forms.ModelForm):
    class Meta:
        model = TDeadend11                # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(TDeadendForm11, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = TDeadend11.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class TUDeadendForm11(forms.ModelForm):   # *************
    class Meta:
        model = tUploadedFile11               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = tUploadedFile11.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadendForm(forms.ModelForm):
    class Meta:
        model = MonopoleDeadend
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm, self).__init__(*args, **kwargs)
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a MonopoleDeadend
        used_structures = MonopoleDeadend.objects.values_list('structure', flat=True)
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
     
class MDeadend1FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MonopoleDeadend   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend1FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True   
        
class UploadedFileForm(forms.ModelForm):   # *************
    class Meta:
        model = UploadedFile1               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = UploadedFile1.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    


class UploadedFileForm2(forms.ModelForm):   # *************
    class Meta:
        model = UploadedFile22               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = UploadedFile22.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

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
    
    
class MDeadendForm5(forms.ModelForm):
    class Meta:
        model = MDeadend5              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm5, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend5.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm5(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile5               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile5.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    

class MDeadendForm6(forms.ModelForm):
    class Meta:
        model = MDeadend6             # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm6, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend6.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm6(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile6               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile6.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    

class MDeadendForm7(forms.ModelForm):
    class Meta:
        model = MDeadend7              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm7, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend7.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm7(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile7               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile7.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadendForm8(forms.ModelForm):
    class Meta:
        model = MDeadend8             # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm8, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend8.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm8(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile8               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile8.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadendForm9(forms.ModelForm):
    class Meta:
        model = MDeadend9              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm9, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend9.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm9(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile9               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile9.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    

class MDeadendForm10(forms.ModelForm):
    class Meta:
        model = MDeadend10              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm10, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend10.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm10(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile10               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile10.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    


class MDeadendForm11(forms.ModelForm):
    class Meta:
        model = MDeadend11              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm11, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend11.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm11(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile11               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile11.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadendForm12(forms.ModelForm):
    class Meta:
        model = MDeadend12              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm12, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend12.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm12(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile12               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile12.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadendForm13(forms.ModelForm):
    class Meta:
        model = MDeadend13              # *************** Here ***********
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadendForm13, self).__init__(*args, **kwargs)          # *************** Here ***********
        self.fields['structure'].empty_label = "Select Structure"

        # Show only structures that don't already have a TowerDeadend
        used_structures = MDeadend13.objects.values_list('structure', flat=True)     # *************** Here ***********
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        
    
class MUDeadendForm13(forms.ModelForm):   # *************
    class Meta:
        model = mUploadedFile13               # *************
        fields = ('structure', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the filtering if we're hardcoding the structure in the view
        used_structures = mUploadedFile13.objects.values_list('structure_id', flat=True)   # *************
        self.fields['structure'].queryset = ListOfStructure.objects.exclude(id__in=used_structures)
        self.fields['structure'].empty_label = "Select Structure"
        # Make the field not required since we're setting it in the view
        self.fields['structure'].required = False

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MDeadend5FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend5   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend5FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True   
        
        
class MDeadend6FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend6   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend6FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend7FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend7   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend7FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend8FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend8   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend8FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend9FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend9   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend9FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend10FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend10   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend10FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend11FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend11   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend11FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend12FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend12   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend12FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class MDeadend13FormUpdateForm(forms.ModelForm):   # here
    class Meta:
        model = MDeadend13   # here
        fields = ['structure', 'num_3_phase_circuits', 'num_shield_wires', 'num_1_phase_circuits', 'num_communication_cables']

    def __init__(self, *args, **kwargs):
        super(MDeadend13FormUpdateForm, self).__init__(*args, **kwargs)   # here
        self.fields['structure'].empty_label = "Select Structure"
        # Make structure field read-only for update
        self.fields['structure'].disabled = True  
        
        
class TUDeadendUpdateForm1(forms.Form):       # Change here
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile1.objects.values_list('structure_id', flat=True)  # Change here
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file 
    
    
class TUDeadendUpdateForm2(forms.Form):       # Change here
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile2.objects.values_list('structure_id', flat=True)  # Change here
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file 
    
    
class TUDeadendUpdateForm3(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile3.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile3.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class TUDeadendUpdateForm4(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile4.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile4.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TUDeadendUpdateForm5(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile5.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile5.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class TUDeadendUpdateForm6(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile6.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile6.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TUDeadendUpdateForm7(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile7.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile7.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TUDeadendUpdateForm8(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile8.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile8.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TUDeadendUpdateForm9(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile9.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile9.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class TUDeadendUpdateForm10(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile10.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile10.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class TUDeadendUpdateForm11(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = tUploadedFile11.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not tUploadedFile11.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm1(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = UploadedFile1.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not UploadedFile1.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm2(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = UploadedFile22.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not UploadedFile22.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm5(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile5.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile5.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

    
    
class MUDeadendUpdateForm6(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile6.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile6.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm7(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile7.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile7.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class MUDeadendUpdateForm8(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile8.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile8.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
class MUDeadendUpdateForm9(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile9.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile9.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm10(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile10.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile10.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    

class MUDeadendUpdateForm11(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile11.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile11.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm12(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile12.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile12.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file
    
    
class MUDeadendUpdateForm13(forms.Form):    # ************
    structure = forms.ModelChoiceField(
        queryset=ListOfStructure.objects.none(),
        empty_label="Select Structure to Update",
        required=True
    )
    
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show structures that have uploaded files
        used_structures = mUploadedFile13.objects.values_list('structure_id', flat=True)   # ************
        self.fields['structure'].queryset = ListOfStructure.objects.filter(id__in=used_structures)

    def clean(self):
        cleaned_data = super().clean()
        structure = cleaned_data.get('structure')
        
        if structure and not mUploadedFile13.objects.filter(structure=structure).exists():   # ************
            raise ValidationError("No uploaded file found for this structure.")
        
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ['.xls', '.xlsx']:
                raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")
        return uploaded_file

    
    
    
from django import forms
from .models import LoadCondition

class LoadConditionForm(forms.ModelForm):
    class Meta:
        model = LoadCondition
        fields = '__all__'
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': '°F'
            }),
            'ice_radial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Radial (in)'
            }),
            'wind_pressure': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Pressure (psf)'
            }),
            'angle_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Angle Factor'
            }),
            'transverse_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Transverse Factor'
            }),
            'vertical_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Vertical Factor'
            }),
            'longitudinal_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Longitudinal Factor'
            }),
        }