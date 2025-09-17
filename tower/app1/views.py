from django.shortcuts import render,get_object_or_404
from .forms import *
from .models import *
import pandas as pd
from django.http import JsonResponse, HttpResponseRedirect



def help(request):
    return render(request,'app1/help.html')

def base(request):
    return render(request,'app1/base.html')

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
    button_type = selected_values.get('button_type', '')
    selected_load_cases = selected_values.get('load_cases', [])
    
    # If coming directly from buttons without specific filters
    if not structure_id and 'go_button' in request.POST:
        structure_id = request.POST.get('structure_id')
        button_type = request.POST.get('go_button')
        load_case_values = request.POST.get('load_case_values', '')
        
        # Convert comma-separated string to list
        if load_case_values:
            selected_load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
        else:
            selected_load_cases = []
            
        if structure_id:
            selected_values = {
                'structure_id': structure_id,
                'button_type': button_type,
                'load_cases': selected_load_cases
            }
            request.session['selected_values'] = selected_values
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # Try to get the latest file from different models
            latest_file = None
            file_model = None
            
            # Check different file models in order of priority
            if tUploadedFile6.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile6.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile6'
            elif hUploadedFile1.objects.filter(structure=structure).exists():
                latest_file = hUploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'hUploadedFile1'
            elif tUploadedFile1.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile1'
            elif tUploadedFile2.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile2'
            elif tUploadedFile3.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile3'
            elif tUploadedFile4.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile4.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile4'
            elif tUploadedFile5.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile5.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile5'
            elif hUploadedFile2.objects.filter(structure=structure).exists():
                latest_file = hUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'hUploadedFile2'
            elif hUploadedFile3.objects.filter(structure=structure).exists():
                latest_file = hUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'hUploadedFile3'
            elif hUploadedFile4.objects.filter(structure=structure).exists():
                latest_file = hUploadedFile4.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'hUploadedFile4'
                
            elif tUploadedFile7.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile7.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile7'
                
            elif tUploadedFile8.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile8.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile8'
                
            elif tUploadedFile9.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile9.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile9'
                
            elif tUploadedFile10.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile10.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile10'
                
            elif tUploadedFile11.objects.filter(structure=structure).exists():
                latest_file = tUploadedFile11.objects.filter(structure=structure).latest('uploaded_at')
                file_model = 'tUploadedFile11'
            
            if not latest_file:
                raise Exception("No uploaded file found for this structure")
                
            df = pd.read_excel(latest_file.file.path, engine='openpyxl')

            # Filter by selected load cases if any are selected
            if selected_load_cases and 'Load Case Description' in df.columns:
                print(f"Filtering by load cases: {selected_load_cases}")
                df = df[df['Load Case Description'].isin(selected_load_cases)]
                print(f"Filtered dataframe shape: {df.shape}")

            # Prepare complete data for table display
            load_data = []
            for _, row in df.iterrows():
                row_data = {}
                for col in df.columns:
                    if pd.notna(row[col]):
                        if pd.api.types.is_numeric_dtype(df[col]):
                            row_data[col] = float(row[col])
                        else:
                            row_data[col] = str(row[col])
                    else:
                        row_data[col] = '' if pd.api.types.is_string_dtype(df[col]) else 0
                load_data.append(row_data)

            # Get unique values for display
            joint_labels = [str(label) for label in df['Attach. Joint Labels'].unique()] if 'Attach. Joint Labels' in df.columns else []
            set_numbers = [str(num) for num in df['Set No.'].dropna().unique()] if 'Set No.' in df.columns else []
            phase_numbers = [str(num) for num in df['Phase No.'].dropna().unique()] if 'Phase No.' in df.columns else []

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
        'load_data': load_data,
        'load_data_json': json.dumps(load_data),
        'selected_values': selected_values,
        'all_columns': list(df.columns) if structure_id and 'df' in locals() else [],
        'button_type': button_type
    })
    
import math
import json
from django.shortcuts import render

def calculation_view(request):
    if request.method == 'GET':
        # Get calculation data from request parameters
        calculation_data_json = request.GET.get('calculation_data')
        
        if calculation_data_json:
            try:
                calculation_data = json.loads(calculation_data_json)
                
                # Add resultant calculation to each record
                for record in calculation_data:
                    vert = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
                    trans = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
                    long = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
                    
                    # Calculate SQRT(Vert² + Trans² + Long²) for each record
                    resultant = math.sqrt(vert**2 + trans**2 + long**2)
                    record['Resultant (lbs)'] = round(resultant, 2)
                
                # Group data by Set No. (for display purposes)
                grouped_data = {}
                for record in calculation_data:
                    set_no = record.get('Set No.', 'Unknown')
                    if set_no not in grouped_data:
                        grouped_data[set_no] = []
                    grouped_data[set_no].append(record)
                
                # Calculate max values for each set and flag max resultant rows
                set_max_values = {}
                max_resultant_values = {}  # Store the actual values that created the max resultant
                max_resultant_indexes = {}  # Store indexes for JavaScript approach
                
                for set_no, records in grouped_data.items():
                    vert_values = [float(record.get('Structure Loads Vert. (lbs)', 0) or 0) for record in records]
                    trans_values = [float(record.get('Structure Loads Trans. (lbs)', 0) or 0) for record in records]
                    long_values = [float(record.get('Structure Loads Long. (lbs)', 0) or 0) for record in records]
                    resultant_values = [record['Resultant (lbs)'] for record in records]
                    
                    # Find the maximum resultant value
                    max_resultant = max(resultant_values)
                    max_index = resultant_values.index(max_resultant)
                    
                    # Store the actual values that created the max resultant
                    max_resultant_values[set_no] = {
                        'vert': vert_values[max_index],
                        'trans': trans_values[max_index],
                        'long': long_values[max_index],
                        'resultant': max_resultant
                    }
                    
                    # Store index for JavaScript approach
                    max_resultant_indexes[set_no] = max_index
                    
                    # Add a simple flag to each record (as a string to avoid underscore issues)
                    for i, record in enumerate(records):
                        if resultant_values[i] == max_resultant:
                            record['max_resultant_flag'] = 'yes'
                        else:
                            record['max_resultant_flag'] = 'no'
                    
                    set_max_values[set_no] = {
                        'max_vert': max(vert_values),
                        'max_trans': max(trans_values),
                        'max_long': max(long_values),
                        'max_resultant': max_resultant,
                        'count': len(records)
                    }
                
                # Calculate combined values across all sets using the actual values that created max resultants
                combined_vert = sum([values['vert'] for values in max_resultant_values.values()])
                combined_trans = sum([values['trans'] for values in max_resultant_values.values()])
                combined_long = sum([values['long'] for values in max_resultant_values.values()])
                
                # Calculate the SQRT formula for combined values
                combined_sqrt = math.sqrt(combined_vert**2 + combined_trans**2 + combined_long**2)
                
                # Prepare context for template
                context = {
                    'grouped_data': grouped_data,
                    'set_max_values': set_max_values,
                    'max_resultant_values': max_resultant_values,  # Add this for displaying actual values
                    'combined_vert': combined_vert,
                    'combined_trans': combined_trans,
                    'combined_long': combined_long,
                    'combined_sqrt': combined_sqrt,
                    'calculation_data': calculation_data,
                    'max_resultant_indexes': max_resultant_indexes,  # Add this for JavaScript
                    'calculation_data_json': json.dumps(calculation_data)  # Add this line

                }
                
                return render(request, 'app1/calculation.html', context)
                
            except json.JSONDecodeError:
                error = 'Invalid calculation data format'
        else:
            error = 'No calculation data provided'
    
    return render(request, 'app1/calculation.html', {'error': error or 'An error occurred during calculation'})


# views.py
import math
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LoadCondition, AttachmentLoad

def load_condition_view(request):
    calculation_data = []
    
    if request.method == 'POST':
        # Get calculation data from POST request
        calculation_data_json = request.POST.get('calculation_data')
        if calculation_data_json:
            try:
                calculation_data = json.loads(calculation_data_json)
            except json.JSONDecodeError:
                pass
    
    # Get all load conditions
    load_conditions = LoadCondition.objects.all().order_by('id')
    
    # Get all attachment loads grouped by load case
    attachment_loads = {}
    for lc in AttachmentLoad.LOAD_CASE_CHOICES:
        loads = AttachmentLoad.objects.filter(load_case=lc[0]).order_by('attachment')
        if loads.exists():
            attachment_loads[lc[0]] = {
                'name': lc[1],
                'loads': loads
            }
    
    # Group calculation data by Set No. for debug display
    grouped_calculation_data = {}
    if calculation_data:
        for record in calculation_data:
            set_no = record.get('Set No.', 'Unknown')
            if set_no not in grouped_calculation_data:
                grouped_calculation_data[set_no] = []
            grouped_calculation_data[set_no].append(record)
    
    # Calculate factored loads for each load condition
    factored_loads_by_condition = {}
    
    if calculation_data:
        # Apply overload factor for each load condition to each record
        for condition in load_conditions:
            factored_records = []
            
            # Process each record individually
            for record in calculation_data:
                # Create a copy of the record
                factored_record = record.copy()
                
                # Extract the correct load values from the record
                vert = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
                trans = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
                long = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
                
                # Apply overload factors - use Decimal for precise multiplication
                from decimal import Decimal
                factored_vert = Decimal(str(vert)) * Decimal(str(condition.vertical_factor))
                factored_trans = Decimal(str(trans)) * Decimal(str(condition.transverse_factor))
                factored_long = Decimal(str(long)) * Decimal(str(condition.longitudinal_factor))
                
                # Convert back to float for consistency
                factored_vert = float(factored_vert)
                factored_trans = float(factored_trans)
                factored_long = float(factored_long)
                
                # Update the record with factored values
                factored_record['Structure Loads Vert. (lbs)'] = round(factored_vert, 2)
                factored_record['Structure Loads Trans. (lbs)'] = round(factored_trans, 2)
                factored_record['Structure Loads Long. (lbs)'] = round(factored_long, 2)
                
                # Recalculate resultant
                factored_resultant = math.sqrt(factored_vert**2 + factored_trans**2 + factored_long**2)
                factored_record['Resultant (lbs)'] = round(factored_resultant, 2)
                
                factored_records.append(factored_record)
            
            # Group factored records by Set No.
            grouped_factored_data = {}
            for record in factored_records:
                set_no = record.get('Set No.', 'Unknown')
                if set_no not in grouped_factored_data:
                    grouped_factored_data[set_no] = []
                grouped_factored_data[set_no].append(record)
            
            factored_loads_by_condition[condition.description] = {
                'grouped_data': grouped_factored_data,
                'factors': {
                    'vertical': condition.vertical_factor,
                    'transverse': condition.transverse_factor,
                    'longitudinal': condition.longitudinal_factor
                }
            }
    
    context = {
        'load_conditions': load_conditions,
        'attachment_loads': attachment_loads,
        'calculation_data': calculation_data,
        'calculation_data_json': json.dumps(calculation_data),  # For JavaScript
        'factored_loads_by_condition': factored_loads_by_condition,
        'has_factored_loads': bool(factored_loads_by_condition),
        'grouped_calculation_data': grouped_calculation_data  # Add this for debug display
    }
    
    return render(request, 'app1/load_condition.html', context)


@csrf_exempt
def calculate_final_loads(request):
    if request.method == 'POST':
        try:
            # Get the calculation data from the previous step
            calculation_data = json.loads(request.POST.get('calculation_data', '[]'))
            
            # Get buffer configuration - per direction
            apply_buffer = request.POST.get('apply_buffer', 'false') == 'true'
            
            # Get buffer values for each direction
            vert_buffer = float(request.POST.get('vert_buffer', 0))
            trans_buffer = float(request.POST.get('trans_buffer', 0))
            long_buffer = float(request.POST.get('long_buffer', 0))
            
            # Get rounding values for each direction
            vert_rounding = int(request.POST.get('vert_rounding', 100))
            trans_rounding = int(request.POST.get('trans_rounding', 100))
            long_rounding = int(request.POST.get('long_rounding', 100))
            
            # Group by Set No.
            grouped_data = {}
            for record in calculation_data:
                set_no = record.get('Set No.', 'Unknown')
                if set_no not in grouped_data:
                    grouped_data[set_no] = []
                grouped_data[set_no].append(record)
            
            # Calculate max resultant for each set
            max_resultant_values = {}
            for set_no, records in grouped_data.items():
                resultant_values = []
                for i, record in enumerate(records):
                    vert = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
                    trans = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
                    long = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
                    resultant = math.sqrt(vert**2 + trans**2 + long**2)
                    resultant_values.append((i, resultant, vert, trans, long))
                
                # Find the max resultant
                max_index, max_resultant, max_vert, max_trans, max_long = max(
                    resultant_values, key=lambda x: x[1]
                )
                
                max_resultant_values[set_no] = {
                    'vert': max_vert,
                    'trans': max_trans,
                    'long': max_long,
                    'resultant': max_resultant
                }
            
            # Calculate the original sum values
            original_sum_vert = sum([values['vert'] for values in max_resultant_values.values()])
            original_sum_trans = sum([values['trans'] for values in max_resultant_values.values()])
            original_sum_long = sum([values['long'] for values in max_resultant_values.values()])
            original_sum_resultant = math.sqrt(original_sum_vert**2 + original_sum_trans**2 + original_sum_long**2)
            
            # Apply buffer and rounding only to the sum values if requested
            processed_sum_vert = original_sum_vert
            processed_sum_trans = original_sum_trans
            processed_sum_long = original_sum_long
            processed_sum_resultant = original_sum_resultant
            
            if apply_buffer:
                # Apply buffers to sum values
                processed_sum_vert += vert_buffer
                processed_sum_trans += trans_buffer
                processed_sum_long += long_buffer
                
                # Apply rounding to sum values
                if vert_rounding > 0:
                    processed_sum_vert = round(processed_sum_vert / vert_rounding) * vert_rounding
                if trans_rounding > 0:
                    processed_sum_trans = round(processed_sum_trans / trans_rounding) * trans_rounding
                if long_rounding > 0:
                    processed_sum_long = round(processed_sum_long / long_rounding) * long_rounding
                
                # Recalculate resultant after buffer and rounding
                processed_sum_resultant = math.sqrt(
                    processed_sum_vert**2 + processed_sum_trans**2 + processed_sum_long**2
                )
            
            # Prepare response
            response_data = {
                'success': True,
                'max_resultant_values': max_resultant_values,  # Original set values
                'processed_sum_values': {  # Processed sum values
                    'vert': processed_sum_vert,
                    'trans': processed_sum_trans,
                    'long': processed_sum_long,
                    'resultant': processed_sum_resultant
                },
                'original_sum_values': {  # Original sum values
                    'vert': original_sum_vert,
                    'trans': original_sum_trans,
                    'long': original_sum_long,
                    'resultant': original_sum_resultant
                },
                'apply_buffer': apply_buffer,
                'vert_buffer': vert_buffer,
                'trans_buffer': trans_buffer,
                'long_buffer': long_buffer,
                'vert_rounding': vert_rounding,
                'trans_rounding': trans_rounding,
                'long_rounding': long_rounding
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
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
        # Handle file upload form
        if 'file' in request.FILES:
            form = tUploadedFileForm1(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases1(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload1')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')  # You might need to create this view
    else:
        form = tUploadedFileForm1()

    structures_with_files1 = ListOfStructure.objects.filter(tuploaded_files1__isnull=False).distinct()
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload1.html', {
        'form': form,
        'structures_with_files1': structures_with_files1
    })


def extract_load_cases1(uploaded_file):
    try:
        # Delete existing load cases and groups (non-custom ones)
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")

def tower_deadend_view1(request):
    towers = TowerDeadend.objects.all()
    return render(request, 'app1/tower_deadend_view1.html', {'towers': towers})


def tower_deadend_view3(request):
    towers = TowerDeadend3.objects.all()
    return render(request, 'app1/tower_deadend_view3.html', {'towers': towers})

def tower_deadend_view4(request):
    towers = TowerDeadend4.objects.all()
    return render(request, 'app1/tower_deadend_view4.html', {'towers': towers})

def tower_deadend_view5(request):
    towers = TowerDeadend5.objects.all()
    return render(request, 'app1/tower_deadend_view5.html', {'towers': towers})


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
        # Handle file upload form
        if 'file' in request.FILES:
            form = tUploadedFileForm2(request.POST, request.FILES)  # Change here
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases3(uploaded_file)  # You may want a separate extractor or reuse with param
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload2')  # Change here
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')  # Change here
    else:
        form = tUploadedFileForm2()  # Change here

    structures_with_files2 = ListOfStructure.objects.filter(tuploaded_files2__isnull=False).distinct()  # change here
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')  # Change here
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload2.html', {             # Change here 
        'form': form,
        'structures_with_files2': structures_with_files2
    })
    

def extract_load_cases3(uploaded_file):
    try:
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")



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
        # Handle file upload form
        if 'file' in request.FILES:
            form = tUploadedFileForm3(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases33(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload3')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')  # You might need to create this view
    else:
        form = tUploadedFileForm3()

    structures_with_files3 = ListOfStructure.objects.filter(tuploaded_files3__isnull=False).distinct()
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload3.html', {
        'form': form,
        'structures_with_files3': structures_with_files3
    })


def extract_load_cases33(uploaded_file):
    try:
        # Delete existing load cases and groups (non-custom ones)
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")


def tupload4(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = tUploadedFileForm4(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases4(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload4')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')  # You might need to create this view
    else:
        form = tUploadedFileForm4()

    structures_with_files4 = ListOfStructure.objects.filter(tuploaded_files4__isnull=False).distinct()
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile4.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload4.html', {
        'form': form,
        'structures_with_files4': structures_with_files4
    })


def extract_load_cases4(uploaded_file):
    try:
        # Delete existing load cases and groups (non-custom ones)
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")


def tupload5(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = tUploadedFileForm5(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases5(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload5')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')  # You might need to create this view
    else:
        
        form = tUploadedFileForm5()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files5__isnull=False).distinct()
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile5.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload5.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def extract_load_cases5(uploaded_file):
    try:
        # Delete existing load cases and groups (non-custom ones)
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")


def tdeadend6(request):
    if request.method == 'POST':
        form = TDeadendForm6(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload6/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm6()

    return render(request, 'app1/tdeadend6.html', {'form': form})

def tupload6(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm6(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases6(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload6')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm6()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files6__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile6.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload6.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases6(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view6(request):
    h = TDeadend6.objects.all()
    return render(request, 'app1/t_deadend_view6.html', {'h': h})


def tdeadend7(request):
    if request.method == 'POST':
        form = TDeadendForm7(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload7/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm7()

    return render(request, 'app1/tdeadend7.html', {'form': form})

def tupload7(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm7(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases7(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload7')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm7()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files7__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile7.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload7.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases7(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view7(request):
    h = TDeadend7.objects.all()
    return render(request, 'app1/t_deadend_view7.html', {'h': h})



def tdeadend8(request):
    if request.method == 'POST':
        form = TDeadendForm8(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload8/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm8()

    return render(request, 'app1/tdeadend8.html', {'form': form})

def tupload8(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm8(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases8(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload8')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm8()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files8__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile8.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload8.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases8(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view8(request):
    h = TDeadend8.objects.all()
    return render(request, 'app1/t_deadend_view8.html', {'h': h})

def tdeadend9(request):
    if request.method == 'POST':
        form = TDeadendForm9(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload9/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm9()

    return render(request, 'app1/tdeadend9.html', {'form': form})

def tupload9(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm9(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases9(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload9')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm9()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files9__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile9.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload9.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases9(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view9(request):
    h = TDeadend9.objects.all()
    return render(request, 'app1/t_deadend_view9.html', {'h': h})


def tdeadend10(request):
    if request.method == 'POST':
        form = TDeadendForm10(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload10/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm10()

    return render(request, 'app1/tdeadend10.html', {'form': form})

def tupload10(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm10(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases10(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload10')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm10()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files10__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile10.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload10.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases10(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view10(request):
    h = TDeadend10.objects.all()
    return render(request, 'app1/t_deadend_view10.html', {'h': h})

def tdeadend11(request):
    if request.method == 'POST':
        form = TDeadendForm11(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tupload11/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = TDeadendForm11()

    return render(request, 'app1/tdeadend11.html', {'form': form})

def tupload11(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = TUDeadendForm11(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    textract_load_cases11(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('tupload11')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = TUDeadendForm11()

    structures_with_files = ListOfStructure.objects.filter(tuploaded_files11__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile11.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/tupload11.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def textract_load_cases11(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def t_deadend_view11(request):
    h = TDeadend11.objects.all()
    return render(request, 'app1/t_deadend_view11.html', {'h': h})


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
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload1.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def extract_load_cases(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
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
        form = HDeadendForm2(request.POST)    # ********** Here **********
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload2/')  # ********** Here **********
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = HDeadendForm2()                    # ********** Here **********

    return render(request, 'app1/hdeadend2.html', {'form': form})      # ********** Here **********

def hupload2(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = HUDeadendForm2(request.POST, request.FILES)  # Change here
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases2(uploaded_file)  # You may want a separate extractor or reuse with param
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('hupload2')  # Change here
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                    
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = HUDeadendForm2()  # Change here

    structures_with_files2 = ListOfStructure.objects.filter(huploaded_files2__isnull=False).distinct()  # change here
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')  # Change here
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload2.html', {             # Change here 
        'form': form,
        'structures_with_files2': structures_with_files2
    })


def extract_load_cases2(uploaded_file):
    try:
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
        df = pd.read_excel(uploaded_file.file.path, engine='openpyxl')
        
        if 'Load Case Description' not in df.columns:
            return
            
        load_cases = df['Load Case Description'].dropna().unique().tolist()
        
        grouped_cases = {}
        for case in load_cases:
            prefix = case.split(' ')[0] if ' ' in case else case
            grouped_cases.setdefault(prefix, []).append(case)
        
        for group_name, cases in grouped_cases.items():
            group = LoadCaseGroup.objects.create(
                name=group_name,
                structure=uploaded_file.structure,
                is_custom=False
            )
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
    except Exception as e:
        print(f"Error extracting load cases: {e}")


def hdeadend3(request):
    if request.method == 'POST':
        form = HDeadendForm3(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload3/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = HDeadendForm3()

    return render(request, 'app1/hdeadend3.html', {'form': form})

def hupload3(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = HUDeadendForm3(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    hextract_load_cases3(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('hupload3')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = HUDeadendForm3()

    structures_with_files = ListOfStructure.objects.filter(huploaded_files3__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload3.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def hextract_load_cases3(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def hdeadend4(request):
    if request.method == 'POST':
        form = HDeadendForm4(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/hupload4/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = HDeadendForm4()

    return render(request, 'app1/hdeadend4.html', {'form': form})

def hupload4(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = HUDeadendForm4(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    hextract_load_cases4(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('hupload4')
                except IntegrityError:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
        
        # Handle custom group creation
        elif 'create_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    
                    # Create custom group
                    custom_group = LoadCaseGroup.objects.create(
                        name=group_name,
                        structure=structure,
                        is_custom=True
                    )
                    
                    # Add selected cases to the custom group
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=custom_group,
                            structure=structure
                        )
                    
                    messages.success(request, f'Custom group "{group_name}" created successfully!')
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        # Handle the Go button POST request
        elif 'go_button' in request.POST:
            button_type = request.POST.get('go_button')
            load_case_values = request.POST.get('load_case_values', '')
            
            # Convert comma-separated string to list
            if load_case_values:
                load_cases = [case.strip() for case in load_case_values.split(',') if case.strip()]
            else:
                load_cases = []
                
            selected_values = {
                'button_type': button_type,  # Store which button was clicked
                'load_cases': load_cases,
                'structure_id': request.POST.get('structure_id')
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    else:
        form = HUDeadendForm4()

    structures_with_files = ListOfStructure.objects.filter(huploaded_files4__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile4.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # New: Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
            # New: Delete a custom group
            elif request.GET.get('delete_custom_group'):
                group_name = request.GET.get('group_name')
                if group_name:
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload4.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def hextract_load_cases4(uploaded_file):
    """Extract load cases from the uploaded Excel file and save to database"""
    try:
        # Delete only non-custom load cases for this structure
        LoadCase.objects.filter(
            structure=uploaded_file.structure, 
            group__is_custom=False
        ).delete()
        LoadCaseGroup.objects.filter(
            structure=uploaded_file.structure, 
            is_custom=False
        ).delete()
        
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
                structure=uploaded_file.structure,
                is_custom=False
            )
            
            for case_name in cases:
                LoadCase.objects.create(
                    name=case_name,
                    group=group,
                    structure=uploaded_file.structure
                )
                
    except Exception as e:
        print(f"Error extracting load cases: {e}")
        
        
def h_deadend_view4(request):
    h = HDeadend4.objects.all()
    return render(request, 'app1/h_deadend_view4.html', {'h': h})

        
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


def h_deadend_view3(request):
    h = HDeadend3.objects.all()
    return render(request, 'app1/h_deadend_view3.html', {'h': h})