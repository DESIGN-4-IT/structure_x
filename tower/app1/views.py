from django.shortcuts import render,get_object_or_404
from .forms import *
from .models import *
import pandas as pd
from django.http import JsonResponse, HttpResponseRedirect



def help(request):
    return render(request,'app1/help.html')


from django.http import JsonResponse

from django.db import IntegrityError

def deadend(request):
    if request.method == 'POST':
        form = MonopoleDeadendForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'status': 'success'})
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
                return JsonResponse({'status': 'error', 'errors': form.errors})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = MonopoleDeadendForm()

    return render(request, 'app1/deadend.html', {'form': form})







def monopole_deadend_view(request):
    monopoles = MonopoleDeadend.objects.all()
    return render(request, 'app1/monopole_deadend_view.html', {'monopoles': monopoles})


def monopole_deadend_view1(request):
    monopoles = MonopoleDeadend1.objects.all()
    return render(request, 'app1/monopole_deadend_view1.html', {'monopoles': monopoles})

def monopole_deadend_view4(request):
    monopoles = MonopoleDeadend4.objects.all()
    return render(request, 'app1/monopole_deadend_view4.html', {'monopoles': monopoles})

def mdeadend(request):
    if request.method == 'POST':
        form = MonopoleDeadendForm1(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MonopoleDeadendForm1()

    return render(request, 'app1/mdeadend.html', {'form': form})

def mdeadend4(request):
    if request.method == 'POST':
        form = MonopoleDeadendForm4(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MonopoleDeadendForm4()

    return render(request, 'app1/mdeadend4.html', {'form': form})

def hdeadend(request):
    return render(request,'app1/hdeadend.html')




def tdeadend(request):
    if request.method == 'POST':
        form = TowerDeadendForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'status': 'success'})
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
                return JsonResponse({'status': 'error', 'errors': form.errors})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = TowerDeadendForm()

    return render(request, 'app1/tdeadend.html', {'form': form})

def tdeadend1(request):
    return render(request,'app1/tdeadend1.html')


from django.db import IntegrityError

def upload1(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('upload1')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = UploadedFileForm()

    files = UploadedFile1.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/upload1.html', {'form': form, 'files': files})

def upload2(request):
    if request.method == 'POST':
        form = UploadedFileForm2(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('upload2')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = UploadedFileForm2()

    files = UploadedFile3.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/upload2.html', {'form': form, 'files': files})

def hupload(request):
    if request.method == 'POST':
        form = UploadedFileForm1(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('hupload')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = UploadedFileForm1()

    files = UploadedFile2.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/hupload.html', {'form': form, 'files': files})


def mupload4(request):
    if request.method == 'POST':
        form = UploadedFileForm4(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('mupload4')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = UploadedFileForm4()

    files = UploadedFile4.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/upload4.html', {'form': form, 'files': files})

from django.shortcuts import render
from django.http import JsonResponse
from .models import ListOfStructure, UploadedFile1
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse
from .models import ListOfStructure, UploadedFile1
import pandas as pd
import os

def drop1(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/drop1.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = UploadedFile1.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = UploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def drop2(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/drop2.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = UploadedFile3.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = UploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def hdrop(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/hdrop.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = UploadedFile2.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = UploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def drop4(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/drop4.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = UploadedFile4.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = UploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def chart(request):
    return render(request,'app1/chart.html')

def data(request):
    return render(request,'app1/data.html')

import json



from django.templatetags.static import static


def hdata1(request):
    # Get selected values from session
    selected_values = request.session.get('selected_values', {})
    structure_id = selected_values.get('structure_id')

    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
            df = pd.read_excel(latest_file.file.path, engine='openpyxl')

            # Initialize filtered data
            filtered_data = df

            # Filter by joint labels if selected
            selected_joints = selected_values.get('joint_labels', [])
            if selected_joints:
                filtered_data = filtered_data[filtered_data['Attach. Joint Labels'].isin(selected_joints)]

            # Filter by set/phase if selected
            selected_set_phase = selected_values.get('set_phase', [])
            if selected_set_phase:
                # Create a mask for filtering
                mask = pd.Series(False, index=filtered_data.index)
                
                for value in selected_set_phase:
                    # Parse the set-phase value (format: "set-phase-{set}-{phase}")
                    parts = value.split('-')
                    if len(parts) >= 4:  # Ensure we have both set and phase
                        set_num = parts[2]
                        phase_num = parts[3]
                        
                        # Apply filter for both set and phase
                        set_mask = (filtered_data['Set No.'].astype(str) == set_num)
                        phase_mask = (filtered_data['Phase No.'].astype(str) == phase_num)
                        mask |= (set_mask & phase_mask)
                    elif len(parts) == 3:  # Only set number provided
                        set_num = parts[2]
                        mask |= (filtered_data['Set No.'].astype(str) == set_num)

                filtered_data = filtered_data[mask]

            # Filter by load cases if selected
            selected_load_cases = selected_values.get('load_cases', [])
            if selected_load_cases and 'Load Case Description' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['Load Case Description'].isin(selected_load_cases)]

            # Prepare complete data for table display - include ALL columns
            load_data = []
            for _, row in filtered_data.iterrows():
                row_data = {}
                # Add all columns from the dataframe
                for col in filtered_data.columns:
                    if pd.notna(row[col]):
                        # Convert numeric values to appropriate types
                        if pd.api.types.is_numeric_dtype(filtered_data[col]):
                            row_data[col] = float(row[col])
                        else:
                            row_data[col] = str(row[col])
                    else:
                        row_data[col] = '' if pd.api.types.is_string_dtype(filtered_data[col]) else 0
                load_data.append(row_data)

            # Get unique values for display
            joint_labels = [str(label) for label in filtered_data['Attach. Joint Labels'].unique()]
            set_numbers = [str(num) for num in filtered_data['Set No.'].dropna().unique()]
            phase_numbers = [str(num) for num in filtered_data['Phase No.'].dropna().unique()]

        except Exception as e:
            joint_labels = []
            set_numbers = []
            phase_numbers = []
            load_data = []
            print(f"Error processing Excel file: {str(e)}")
    else:
        joint_labels = []
        set_numbers = []
        phase_numbers = []
        load_data = []

    return render(request, 'app1/hdata1.html', {
        'joint_labels': joint_labels,
        'set_numbers': set_numbers,
        'phase_numbers': phase_numbers,
        'load_data': load_data,  # Pass the actual data, not just JSON
        'load_data_json': json.dumps(load_data),
        'selected_values': selected_values,
        'all_columns': list(df.columns) if structure_id and 'df' in locals() else []  # Pass all column names
    })
    
    
from django.shortcuts import render, redirect
from .models import ListOfStructure
from .forms import StructureForm

# View to display all structures
def list_structures(request):
    structures = ListOfStructure.objects.all()
    return render(request, 'app1/home.html', {'structures': structures})

# View to add a new structure
def add_structure(request):
    if request.method == 'POST':
        form = StructureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StructureForm()
    return render(request, 'app1/add_structure.html', {'form': form})


def delete_structure(request, structure_id):
    structure = get_object_or_404(ListOfStructure, id=structure_id)
    structure.delete()
    return redirect('home')



def tupload1(request):
    if request.method == 'POST':
        form = tUploadedFileForm1(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('tupload1')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = tUploadedFileForm1()

    files = tUploadedFile1.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/tupload1.html', {'form': form, 'files': files})

def tower_deadend_view1(request):
    towers = TowerDeadend.objects.all()
    return render(request, 'app1/tower_deadend_view1.html', {'towers': towers})


def tdrop1(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/tdrop1.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = tUploadedFile1.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = tUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



def tupload2(request):
    if request.method == 'POST':
        form = tUploadedFileForm2(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('tupload2')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = tUploadedFileForm2()

    files = tUploadedFile2.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/tupload2.html', {'form': form, 'files': files})


def tdrop2(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/tdrop2.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = tUploadedFile2.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = tUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# In tower only tdeadend3 and tupload3 are used we have 
#    path('tdeadend4/',views.tdeadend4,name='tdeadend4'),
#    path('tdeadend5/',views.tdeadend5,name='tdeadend5'),
#    path('tupload4/',views.tupload4,name='tupload4'),
#    path('tupload5/',views.tupload5,name='tupload5'),
#    path('tdrop4/',views.tdrop4,name='tdrop4'),
#    path('tdrop5/',views.tdrop5,name='tdrop5'),

def tdeadend3(request):
    if request.method == 'POST':
        form = TowerDeadendForm3(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload3/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TowerDeadendForm3()

    return render(request, 'app1/tdeadend3.html', {'form': form})

def tdeadend4(request):
    if request.method == 'POST':
        form = TowerDeadendForm4(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload4/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TowerDeadendForm4()

    return render(request, 'app1/tdeadend4.html', {'form': form})


def tdeadend5(request):
    if request.method == 'POST':
        form = TowerDeadendForm5(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload5/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TowerDeadendForm5()

    return render(request, 'app1/tdeadend5.html', {'form': form})

def tupload3(request):
    if request.method == 'POST':
        form = tUploadedFileForm3(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('tupload3')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = tUploadedFileForm3()

    files = tUploadedFile3.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/tupload3.html', {'form': form, 'files': files})


def tupload4(request):
    if request.method == 'POST':
        form = tUploadedFileForm4(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('tupload4')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = tUploadedFileForm4()

    files = tUploadedFile4.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/tupload4.html', {'form': form, 'files': files})


def tupload5(request):
    if request.method == 'POST':
        form = tUploadedFileForm5(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('tupload5')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = tUploadedFileForm5()

    files = tUploadedFile5.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/tupload5.html', {'form': form, 'files': files})



def tdrop3(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/tdrop3.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = tUploadedFile3.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = tUploadedFile3.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def tdrop4(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/tdrop4.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = tUploadedFile4.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = tUploadedFile4.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def tdrop5(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/tdrop5.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = tUploadedFile5.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile5.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = tUploadedFile5.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = tUploadedFile5.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.contrib import messages



def hdeadend1(request):
    if request.method == 'POST':
        form = HDeadendForm1(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload1/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = HDeadendForm1()

    return render(request, 'app1/hdeadend1.html', {'form': form})

def hupload1(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = HUDeadendForm1(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('hupload1')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            selected_values = {
                'set_phase': request.POST.getlist('set_phase_values'),
                'joint_labels': request.POST.getlist('joint_label_values'),
                'load_cases': request.POST.getlist('load_case_values'),
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = HUDeadendForm1()

    structures_with_files = ListOfStructure.objects.filter(huploaded_files1__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
            df = pd.read_excel(latest_file.file.path, engine='openpyxl')

            if request.GET.get('get_set_phase'):
                # Process set/phase data
                set_phase_data = df[['Set No.', 'Phase No.']].dropna().drop_duplicates()
                data = set_phase_data.to_dict('records')
                columns = {'Set No.': 'Set No.', 'Phase No.': 'Phase No.'}
                return JsonResponse({'data': data, 'columns': columns})

            elif request.GET.get('get_joint_labels'):
                # Process joint labels
                joint_labels = df['Attach. Joint Labels'].dropna().unique().tolist()
                return JsonResponse({'values': joint_labels})
                
            elif request.GET.get('get_load_cases'):
                # Process load cases - extract unique load cases
                if 'Load Case Description' in df.columns:
                    load_cases = df['Load Case Description'].dropna().unique().tolist()
                    return JsonResponse({'values': load_cases})
                else:
                    return JsonResponse({'error': 'Load Case Description column not found'}, status=400)
                    
            elif request.GET.get('get_grouped_load_cases'):
                # Process grouped load cases
                if 'Load Case Description' in df.columns:
                    load_cases = df['Load Case Description'].dropna().unique().tolist()
                    
                    # Group load cases by their prefix (e.g., Hurricane, NESC, Rule)
                    grouped_cases = {}
                    for case in load_cases:
                        # Extract the prefix (first word before space)
                        if ' ' in case:
                            prefix = case.split(' ')[0]
                        else:
                            prefix = case
                            
                        if prefix not in grouped_cases:
                            grouped_cases[prefix] = []
                        grouped_cases[prefix].append(case)
                    
                    return JsonResponse({'groups': grouped_cases})
                else:
                    return JsonResponse({'error': 'Load Case Description column not found'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload1.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def extract_load_cases(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete existing load cases for this structure
        LoadCase.objects.filter(structure=uploaded_file.structure).delete()
        LoadCaseGroup.objects.filter(structure=uploaded_file.structure).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        # Group load cases by their prefix
        grouped_cases = {}
        for case in load_cases:
            if ' ' in case:
                prefix = case.split(' ')[0]
            else:
                prefix = case
                
            if prefix not in grouped_cases:
                grouped_cases[prefix] = []
            grouped_cases[prefix].append(case)
        
        # Save to database
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")


def hdrop1(request):
    # Get data for Attachments Joint Labels
    if 'get_joint_labels' in request.GET and 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        try:
            file = hUploadedFile1.objects.get(structure_id=structure_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            
            # Check for common column names that might contain joint labels
            possible_columns = ['Attach. Joint Labels', 'Attachment Joint Labels', 'Joint Labels']
            target_column = None
            
            for col in possible_columns:
                if col in df.columns:
                    target_column = col
                    break
            
            if target_column:
                values = df[target_column].dropna().astype(str).unique().tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'error': 'No joint labels column found'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # Get data for Set/Phase
    if 'get_set_phase' in request.GET and 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        try:
            file = hUploadedFile1.objects.get(structure_id=structure_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            
            # Check for required columns
            required_columns = {
                'description': ['Load Case Description', 'Description', 'Load Description'],
                'set_no': ['Set No.', 'Set Number', 'Set'],
                'phase_no': ['Phase No.', 'Phase Number', 'Phase']
            }
            
            found_columns = {}
            for field, possible_names in required_columns.items():
                for name in possible_names:
                    if name in df.columns:
                        found_columns[field] = name
                        break
            
            if len(found_columns) == 3:
                result = df[list(found_columns.values())].dropna().to_dict('records')
                return JsonResponse({'data': result, 'columns': found_columns})
            else:
                return JsonResponse({'error': 'Required columns not found'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # Original hdrop1 functionality remains the same
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/hdrop1.html', {'structures': structures})


    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = hUploadedFile1.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = hUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = hUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = hUploadedFile1.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)




def hdeadend2(request):
    if request.method == 'POST':
        form = HDeadendForm2(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload2/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = HDeadendForm2()

    return render(request, 'app1/hdeadend2.html', {'form': form})

def hupload2(request):
    if request.method == 'POST':
        form = HUDeadendForm2(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('hupload2')
            except IntegrityError:
                form.add_error('structure', 'A file has already been uploaded for this structure.')
    else:
        form = HUDeadendForm2()

    files = hUploadedFile2.objects.all().order_by('-uploaded_at')[:2]  # Limit to 2 recent uploads

    return render(request, 'app1/hupload2.html', {'form': form, 'files': files})


def hdrop2(request):
    # Page load: return all structures
    if request.method == "GET" and not request.GET:
        structures = ListOfStructure.objects.all()
        return render(request, 'app1/hdrop2.html', {'structures': structures})

    # AJAX: Get files of a selected structure
    if 'structure_id' in request.GET:
        structure_id = request.GET.get('structure_id')
        files = hUploadedFile2.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = hUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = hUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            columns = [str(col).strip() for col in df.columns if str(col).strip() not in ['', 'nan']]
            return JsonResponse({'columns': columns})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read columns: {str(e)}"}, status=400)

    # AJAX: Get values from selected column
    if 'file_id' in request.GET and 'column_name' in request.GET:
        file_id = request.GET.get('file_id')
        column_name = request.GET.get('column_name')
        try:
            file = hUploadedFile2.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            if column_name in df.columns:
                values = df[column_name].dropna().astype(str).tolist()
                return JsonResponse({'values': values})
            else:
                return JsonResponse({'values': []})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read values: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



def h_deadend_view1(request):
    h = HDeadend1.objects.all()
    return render(request, 'app1/h_deadend_view1.html', {'h': h})


def h_deadend_view2(request):
    h = HDeadend2.objects.all()
    return render(request, 'app1/h_deadend_view2.html', {'h': h})