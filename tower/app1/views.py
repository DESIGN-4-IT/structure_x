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




def tdeadend_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TowerDeadend, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadendFormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tower_deadend_view1/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadendFormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def tdeadend1(request):
    return render(request,'app1/tdeadend1.html')


from django.db import IntegrityError


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
        files = UploadedFile22.objects.filter(structure_id=structure_id)
        file_data = [{'id': f.id, 'name': os.path.basename(f.file.name)} for f in files]
        return JsonResponse({'files': file_data})

    # ✅ NEW: Get full Excel data
    if 'file_id' in request.GET and 'get_full_excel' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile22.objects.get(id=file_id)
            df = pd.read_excel(file.file.path, engine='openpyxl')
            rows = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
            return JsonResponse({'rows': rows})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read file: {str(e)}"}, status=400)

    # AJAX: Get columns of selected file
    if 'file_id' in request.GET and 'get_columns' in request.GET:
        file_id = request.GET.get('file_id')
        try:
            file = UploadedFile22.objects.get(id=file_id)
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
            file = UploadedFile22.objects.get(id=file_id)
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
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["POST"])
@csrf_exempt # Consider removing this and passing the CSRF token in AJAX
def store_set_phase_combinations(request):
    """
    Handles the AJAX request to store the created Set-Phase combinations
    along with their 'Ahead' or 'Back' status in the session.
    """
    try:
        # Load the JSON data sent from the frontend
        data = json.loads(request.body)
        
        # The data should contain the list of combinations and the status
        combinations_to_add = data.get('combinations', [])
        status = data.get('status') # 'Ahead' or 'Back'
        
        if not combinations_to_add or status not in ['Ahead', 'Back']:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'}, status=400)

        # Get the current active combinations from the session
        # Initialize if it doesn't exist
        selected_values = request.session.get('selected_values', {})
        active_combinations = selected_values.get('active_combinations', [])

        # Process the new combinations: Add the status
        new_active_combinations = []
        for combo in combinations_to_add:
      
            combo_with_status = f"{combo}-{status}" 
            new_active_combinations.append(combo_with_status)

        active_combinations.extend(new_active_combinations)

        # Update the session with the new list
        request.session['selected_values']['active_combinations'] = active_combinations
        request.session.modified = True

        return JsonResponse({
            'status': 'success', 
            'message': f'Successfully stored {len(combinations_to_add)} combinations as {status}.',
            'new_combinations': new_active_combinations
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Error storing combinations: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def hdata1(request):
                               # **********8
    available_models = TowerModel.objects.all().order_by('name')
    selected_model_id = request.session.get('selected_model_id')
    
    if request.method == 'POST' and 'selected_model' in request.POST:
        selected_model_id = request.POST.get('selected_model')
        if selected_model_id:
            request.session['selected_model_id'] = selected_model_id
        else:
            # Clear selection if "None" is selected
            request.session.pop('selected_model_id', None)
    
    # Handle new model upload
    if request.method == 'POST' and 'tower_model_file' in request.FILES:
        model_name = request.POST.get('model_name', 'Unnamed Model')
        model_file = request.FILES['tower_model_file']
        
        # Validate file type
        if model_file.name.endswith(('.glb', '.gltf')):
            new_model = TowerModel.objects.create(
                name=model_name,
                model_file=model_file
            )
            # Optionally select the newly uploaded model
            request.session['selected_model_id'] = new_model.id
    
    # Get selected model if any
    selected_model = None
    if selected_model_id:
        try:
            selected_model = TowerModel.objects.get(id=selected_model_id)
        except TowerModel.DoesNotExist:
            pass                                       # **********8
    # Get selected values from session
    selected_values = request.session.get('selected_values', {})
    active_combinations = selected_values.get('active_combinations', [])
    structure_id = selected_values.get('structure_id')
    button_type = selected_values.get('button_type', '')
    
    
    # Keep only the canvas container logic
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # Try to get the latest file from different models
            latest_file = None
            file_models = [
                tUploadedFile6, hUploadedFile1, tUploadedFile1, tUploadedFile2,
                tUploadedFile3, tUploadedFile4, tUploadedFile5, hUploadedFile2,
                hUploadedFile3, hUploadedFile4, tUploadedFile7, tUploadedFile8,
                tUploadedFile9, tUploadedFile10, tUploadedFile11, UploadedFile1,
                UploadedFile22, mUploadedFile5, mUploadedFile6, mUploadedFile7,
                mUploadedFile8, mUploadedFile9, mUploadedFile10, mUploadedFile11
            ]
            
            for model in file_models:
                if model.objects.filter(structure=structure).exists():
                    latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
                    break
            
            if not latest_file:
                raise Exception("No uploaded file found for this structure")
                
            df = pd.read_excel(latest_file.file.path, engine='openpyxl')

            # Get selected load cases from session to filter data
            selected_load_cases = selected_values.get('load_cases', [])
            if selected_load_cases and 'Load Case Description' in df.columns:
                df = df[df['Load Case Description'].isin(selected_load_cases)]

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
    
    # NEW: Initialize session storage for selections
    if 'selected_values' not in request.session:
        request.session['selected_values'] = {}
    
    # Initialize empty arrays if they don't exist
    if 'selected_joints' not in request.session['selected_values']:
        request.session['selected_values']['selected_joints'] = []
    
    if 'active_combinations' not in request.session['selected_values']:
        request.session['selected_values']['active_combinations'] = []
    
    # Get current selections from session
    selected_joints = request.session['selected_values'].get('selected_joints', [])
    # IMPORTANT: The active_combinations now includes the 'Ahead'/'Back' status
    active_combinations = request.session['selected_values'].get('active_combinations', [])
    
    # Build filter criteria
    filter_criteria = {}
    
    # Store joint labels if any are selected
    if selected_joints:
        filter_criteria['joint_labels'] = selected_joints
    
    # Store set-phase combinations if any are active
    set_phase_pairs = []
    if active_combinations:
        for combo in active_combinations:
            if isinstance(combo, str):
                # New, correct format: "1-2-Ahead"
                # We need the first two parts ("1" and "2")
                set_phase_pairs.append(combo.split('-')[:2])
            elif isinstance(combo, dict):
                # Handle potential LEGACY dictionary format (e.g., {'set': 1, 'phase': 2})
                # If your old format was different, adjust this logic.
                set_val = str(combo.get('set'))
                phase_val = str(combo.get('phase'))
                if set_val and phase_val:
                    set_phase_pairs.append([set_val, phase_val])
                # NOTE: If you don't need to support the legacy dict format, you can
                # just add a 'pass' or continue to skip it.
            # else: skip other unexpected data types

    if set_phase_pairs:
        filter_criteria['set_phase_combinations'] = set_phase_pairs
    
    # Store filter criteria in session
    request.session['selected_values']['filter_criteria'] = filter_criteria
    request.session.modified = True

    return render(request, 'app1/hdata1.html', {
        'available_models': available_models,   # **********8
        'selected_model': selected_model,        # **********8
        'joint_labels': joint_labels,
        'set_numbers': set_numbers,
        'phase_numbers': phase_numbers,
        'load_data': load_data,
        'load_data_json': json.dumps(load_data),
        'selected_values': selected_values,
        'all_columns': list(df.columns) if structure_id and 'df' in locals() else [],
        'button_type': button_type,
        'structure_id': structure_id,
        'filter_criteria': filter_criteria,
        'selected_joints': selected_joints,  # NEW: Pass to template
        'active_combinations': active_combinations,  # NEW: Pass to template
    })
    
# Add this function to your views.py
def update_selection_session(request):
    """Update session with current selections"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            selected_joints = request.POST.getlist('selected_joints[]')
            active_combinations_json = request.POST.get('active_combinations', '[]')
            
            try:
                active_combinations = json.loads(active_combinations_json)
            except json.JSONDecodeError:
                active_combinations = []
            
            # Ensure Set and Phase values are consistently stored as strings,
            # potentially converting numbers to their integer string representation if they are whole.
            normalized_combinations = []
            for combo in active_combinations:
                normalized_combo = {}
                for key, value in combo.items():
                    if isinstance(value, (int, float)):
                        # If it's a whole number, store as integer string '2' instead of '2.0'
                        if value == int(value):
                            normalized_combo[key] = str(int(value))
                        else:
                            normalized_combo[key] = str(value)
                    else:
                        normalized_combo[key] = str(value).strip() # Ensure no leading/trailing spaces
                normalized_combinations.append(normalized_combo)

            if 'selected_values' not in request.session:
                request.session['selected_values'] = {}
            
            request.session['selected_values']['selected_joints'] = selected_joints
            request.session['selected_values']['active_combinations'] = normalized_combinations # Use normalized combinations
            
            filter_criteria = {}
            if selected_joints:
                filter_criteria['joint_labels'] = selected_joints
            if normalized_combinations:
                filter_criteria['set_phase_combinations'] = normalized_combinations # Use normalized combinations
            
            request.session['selected_values']['filter_criteria'] = filter_criteria
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'selected_joints': selected_joints,
                'active_combinations': normalized_combinations, # Return normalized combinations
                'filter_criteria': filter_criteria
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def apply_previous_selection_filter(structure_id, filter_criteria, selected_load_cases=None):
    """Apply filter based on previous page selection (Set+Phase or Joint Label)"""
    if not structure_id or not filter_criteria:
        return []
    
    try:
        structure = ListOfStructure.objects.get(id=structure_id)
        
        latest_file = None
        file_models = [
            tUploadedFile6, hUploadedFile1, tUploadedFile1, tUploadedFile2,
            tUploadedFile3, tUploadedFile4, tUploadedFile5, hUploadedFile2,
            hUploadedFile3, hUploadedFile4, tUploadedFile7, tUploadedFile8,
            tUploadedFile9, tUploadedFile10, tUploadedFile11, UploadedFile1,
            UploadedFile22, mUploadedFile5, mUploadedFile6, mUploadedFile7,
            mUploadedFile8, mUploadedFile9, mUploadedFile10, mUploadedFile11
        ]
        
        for model in file_models:
            if model.objects.filter(structure=structure).exists():
                latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
                break
        
        if not latest_file:
            print("DEBUG: No latest file found.") # Added debug
            return []
            
        df = pd.read_excel(latest_file.file.path, engine='openpyxl')
        
        print(f"DEBUG: Original dataframe shape: {df.shape}")
        print(f"DEBUG: Filter criteria: {filter_criteria}")
        print(f"DEBUG: Selected load cases: {selected_load_cases}")
        
        if selected_load_cases and 'Load Case Description' in df.columns:
            df = df[df['Load Case Description'].isin(selected_load_cases)]
            print(f"DEBUG: After load case filter: {df.shape}")
        
        if 'joint_labels' in filter_criteria and filter_criteria['joint_labels']:
            joint_labels = [str(label).strip() for label in filter_criteria['joint_labels']] # Ensure stripping
            print(f"DEBUG: Filtering by joint labels: {joint_labels}")
            if 'Attach. Joint Labels' in df.columns:
                df['Attach. Joint Labels'] = df['Attach. Joint Labels'].astype(str).str.strip() # Strip whitespace
                df = df[df['Attach. Joint Labels'].isin(joint_labels)]
                print(f"DEBUG: After joint filter: {df.shape}")
        
        if 'set_phase_combinations' in filter_criteria and filter_criteria['set_phase_combinations']:
            combinations = filter_criteria['set_phase_combinations']
            print(f"DEBUG: Filtering by combinations: {combinations}")
            
            # Prepare dataframe columns for robust comparison
            df_set_col_exists = 'Set No.' in df.columns
            df_phase_col_exists = 'Phase No.' in df.columns

            if df_set_col_exists:
                df['Set No._norm'] = df['Set No.'].apply(lambda x: str(int(x)) if pd.notna(x) and x == int(x) else str(x) if pd.notna(x) else '').str.strip()
            if df_phase_col_exists:
                df['Phase No._norm'] = df['Phase No.'].apply(lambda x: str(int(x)) if pd.notna(x) and x == int(x) else str(x) if pd.notna(x) else '').str.strip()
            
            combination_mask = pd.Series([False] * len(df))
            
            for combination in combinations:
                # Retrieve the normalized values from the session
                set_val = combination.get('set', '')
                phase_val = combination.get('phase', '')
                
                print(f"DEBUG: Looking for Set: '{set_val}', Phase: '{phase_val}'")
                
                # Apply filters using the new normalized columns
                set_filter = (df['Set No._norm'] == set_val) if df_set_col_exists else pd.Series([False] * len(df))
                phase_filter = (df['Phase No._norm'] == phase_val) if df_phase_col_exists else pd.Series([False] * len(df))
                
                combo_filter = set_filter & phase_filter
                
                matching_count = combo_filter.sum()
                print(f"DEBUG: Records matching Set '{set_val}' AND Phase '{phase_val}': {matching_count}")
                
                if matching_count > 0:
                    print(f"DEBUG: Sample matching records:")
                    matching_records = df[combo_filter].head(3)
                    for _, record in matching_records.iterrows():
                        print(f"  - Set: {record.get('Set No.', 'N/A')}, Phase: {record.get('Phase No.', 'N/A')}, Load Case: {record.get('Load Case Description', 'N/A')}")
                
                combination_mask = combination_mask | combo_filter
            
            if combination_mask.any():
                df = df[combination_mask]
                print(f"DEBUG: After combination filter: {df.shape}")
            else:
                print(f"DEBUG: No records matched any combination in the remaining data.")
                return [] # No records matched after all filters
        
        # Original logic for returning filtered data records
        filtered_data = []
        for _, row in df.iterrows():
            row_data = {}
            for col in df.columns:
                # Exclude temporary normalized columns from final output
                if col.endswith('_norm'):
                    continue 

                # Handle NaN values and data types for output
                val = row[col]
                if pd.isna(val):
                    row_data[col] = '' if pd.api.types.is_string_dtype(df[col]) else 0
                elif pd.api.types.is_numeric_dtype(df[col]):
                    row_data[col] = float(val)
                else:
                    row_data[col] = str(val)
            filtered_data.append(row_data)
        
        print(f"DEBUG: Final filtered records count: {len(filtered_data)}")
        return filtered_data
            
    except Exception as e:
        print(f"Error applying filter: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return []
    
def load_cases_page(request):
    """New dedicated page for Load Cases Selection and Load Values"""
    # Get selected values from session
    selected_values = request.session.get('selected_values', {})
    structure_id = selected_values.get('structure_id')
    selected_load_cases = selected_values.get('load_cases', [])
    
    # NEW: Get filter criteria from previous page
    filter_criteria = selected_values.get('filter_criteria', {})
    
    # Handle load cases selection via AJAX only
    if request.method == 'POST' and 'load_cases_selection' in request.POST:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            selected_load_cases = request.POST.getlist('selected_load_cases')
            # Store selected load cases in session
            if 'selected_values' not in request.session:
                request.session['selected_values'] = {}
            request.session['selected_values']['load_cases'] = selected_load_cases
            request.session.modified = True
            
            # Return JSON response for AJAX requests
            return JsonResponse({'success': True, 'selected_cases': selected_load_cases})
    
    # NEW: Handle filter by previous selection
    if request.method == 'POST' and 'filter_by_previous' in request.POST:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print(f"DEBUG: Filtering by previous selection - Criteria: {filter_criteria}")
            print(f"DEBUG: Current selected load cases: {selected_load_cases}")
            
            # Apply filter criteria to get filtered data - ONLY use currently selected load cases
            filtered_data = apply_previous_selection_filter(structure_id, filter_criteria, selected_load_cases)
            
            # DO NOT update the selected_load_cases in session - keep user's current selection
            # Only return the filtered data for display
            
            print(f"DEBUG: Filtered data count: {len(filtered_data)}")
            
            return JsonResponse({
                'success': True, 
                'filtered_data': filtered_data,  # Return the actual data
                'filter_criteria': filter_criteria,
                'record_count': len(filtered_data),
                'current_selected_cases': selected_load_cases  # Return current selection for reference
            })


    
    # AJAX handlers (moved from hdata1)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return handle_load_cases_ajax(request)
    
    # Data processing for Load Values display
    load_data = []
    available_load_cases = []
    all_columns = []
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # Try to get the latest file from different models
            latest_file = None
            file_models = [
                tUploadedFile6, hUploadedFile1, tUploadedFile1, tUploadedFile2,
                tUploadedFile3, tUploadedFile4, tUploadedFile5, hUploadedFile2,
                hUploadedFile3, hUploadedFile4, tUploadedFile7, tUploadedFile8,
                tUploadedFile9, tUploadedFile10, tUploadedFile11, UploadedFile1,
                UploadedFile22, mUploadedFile5, mUploadedFile6, mUploadedFile7,
                mUploadedFile8, mUploadedFile9, mUploadedFile10, mUploadedFile11
            ]
            
            for model in file_models:
                if model.objects.filter(structure=structure).exists():
                    latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
                    break
            
            if latest_file:
                df = pd.read_excel(latest_file.file.path, engine='openpyxl')

                # Get available load cases for selection
                if 'Load Case Description' in df.columns:
                    available_load_cases = df['Load Case Description'].dropna().unique().tolist()

                # NEW: Apply filter criteria if available and no specific load cases selected
                if not selected_load_cases and filter_criteria:
                    filtered_load_cases = apply_previous_selection_filter(structure_id, filter_criteria)
                    if filtered_load_cases and 'Load Case Description' in df.columns:
                        df = df[df['Load Case Description'].isin(filtered_load_cases)]
                # Existing: Filter by selected load cases if any are selected
                elif selected_load_cases and 'Load Case Description' in df.columns:
                    df = df[df['Load Case Description'].isin(selected_load_cases)]

                # Prepare complete data for table display
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

                all_columns = list(df.columns)

        except Exception as e:
            print(f"Error processing Excel file: {str(e)}")

    # Handle calculation request
    if request.method == 'GET' and 'calculation_data' in request.GET:
        try:
            calculation_data = json.loads(request.GET.get('calculation_data', '[]'))
            return render(request, 'app1/calculation_results.html', {
                'calculation_data': calculation_data,
                'structure_id': structure_id
            })
        except json.JSONDecodeError:
            pass

    return render(request, 'app1/load_cases.html', {
        'load_data': load_data,
        'load_data_json': json.dumps(load_data),
        'selected_values': selected_values,
        'all_columns': all_columns,
        'available_load_cases': available_load_cases,
        'selected_load_cases': selected_load_cases,
        'structure_id': structure_id,
        'filter_criteria': filter_criteria,  # NEW: Pass filter criteria to template
    })
    
def get_filtered_load_data(request):
    """Get filtered load data based on selected load cases"""
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    structure_id = request.GET.get('structure_id')
    selected_load_cases = request.GET.getlist('selected_load_cases') or []
    
    if not structure_id:
        return JsonResponse({'error': 'Structure ID is required'}, status=400)
    
    try:
        structure = ListOfStructure.objects.get(id=structure_id)
        load_data = []
        all_columns = []
        
        # Try to get the latest file from different models
        latest_file = None
        file_models = [
            tUploadedFile6, hUploadedFile1, tUploadedFile1, tUploadedFile2,
            tUploadedFile3, tUploadedFile4, tUploadedFile5, hUploadedFile2,
            hUploadedFile3, hUploadedFile4, tUploadedFile7, tUploadedFile8,
            tUploadedFile9, tUploadedFile10, tUploadedFile11, UploadedFile1,
            UploadedFile22, mUploadedFile5, mUploadedFile6, mUploadedFile7,
            mUploadedFile8, mUploadedFile9, mUploadedFile10, mUploadedFile11
        ]
        
        for model in file_models:
            if model.objects.filter(structure=structure).exists():
                latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
                break
        
        if latest_file:
            df = pd.read_excel(latest_file.file.path, engine='openpyxl')

            # Filter by selected load cases if any are selected
            if selected_load_cases and 'Load Case Description' in df.columns:
                df = df[df['Load Case Description'].isin(selected_load_cases)]

            # Prepare complete data for table display
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

            all_columns = list(df.columns)
            
            return JsonResponse({
                'load_data': load_data,
                'all_columns': all_columns,
                'record_count': len(load_data)
            })
        else:
            return JsonResponse({'error': 'No file found for this structure'}, status=404)
            
    except ListOfStructure.DoesNotExist:
        return JsonResponse({'error': 'Structure not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def handle_load_cases_ajax(request):
    """Handle all AJAX requests for load cases (moved from hdata1)"""
    structure_id = request.GET.get('structure_id') or request.POST.get('structure_id')
    
    if not structure_id:
        return JsonResponse({'error': 'Structure ID is required'}, status=400)
        
    try:
        structure = ListOfStructure.objects.get(id=structure_id)
        
        # Handle custom group creation
        if request.method == 'POST' and 'create_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases')
            
            if group_name and selected_cases:
                custom_group = LoadCaseGroup.objects.create(
                    name=group_name,
                    structure=structure,
                    is_custom=True
                )
                
                for case_name in selected_cases:
                    LoadCase.objects.create(
                        name=case_name,
                        group=custom_group,
                        structure=structure
                    )
                
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Group name and cases are required'})
        
        # Handle custom group deletion
        elif request.method == 'POST' and 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name:
                LoadCaseGroup.objects.filter(
                    structure=structure, 
                    name=group_name, 
                    is_custom=True
                ).delete()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Group name is required'})
        
        # Handle custom group update
        elif request.method == 'POST' and 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name:
                groups = LoadCaseGroup.objects.filter(
                    structure=structure,
                    name=old_group_name,
                    is_custom=True
                )
                
                if not groups.exists():
                    return JsonResponse({'success': False, 'error': f'Group "{old_group_name}" not found'})
                
                for group in groups:
                    group.name = new_group_name
                    group.save()
                
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Old and new group names are required'})
        
        # Handle GET requests for load case data
        elif request.method == 'GET':
            # Get filtered load data for table
            if request.GET.get('get_filtered_load_data'):
                return get_filtered_load_data(request)
            
            # Get imported load cases
            elif request.GET.get('get_load_cases'):
                return get_imported_load_cases(structure)
            
            # Get grouped load cases
            elif request.GET.get('get_grouped_load_cases'):
                return get_grouped_load_cases(structure)
            
            # Get custom groups
            elif request.GET.get('get_custom_groups_for_selection'):
                return get_custom_groups(structure)
    
    except ListOfStructure.DoesNotExist:
        return JsonResponse({'error': 'Structure not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_imported_load_cases(structure):
    """Get imported load cases from Excel files"""
    latest_file = None
    file_models = [
        hUploadedFile1, tUploadedFile6, tUploadedFile1, tUploadedFile2,
        tUploadedFile3, tUploadedFile4, tUploadedFile5, hUploadedFile2,
        hUploadedFile3, hUploadedFile4, tUploadedFile7, tUploadedFile8,
        tUploadedFile9, tUploadedFile10, tUploadedFile11, UploadedFile1,
        UploadedFile22, mUploadedFile5, mUploadedFile6, mUploadedFile7,
        mUploadedFile8, mUploadedFile9, mUploadedFile10, mUploadedFile11
    ]
    
    for model in file_models:
        if model.objects.filter(structure=structure).exists():
            latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
            break
    
    if latest_file:
        df = pd.read_excel(latest_file.file.path, engine='openpyxl')
        if 'Load Case Description' in df.columns:
            load_cases = df['Load Case Description'].dropna().unique().tolist()
            return JsonResponse({'values': load_cases})
    
    return JsonResponse({'error': 'No load cases found'}, status=404)

def get_grouped_load_cases(structure):
    """Get grouped load cases from Excel files"""
    latest_file = None
    file_models = [hUploadedFile1, tUploadedFile6, tUploadedFile1]
    
    for model in file_models:
        if model.objects.filter(structure=structure).exists():
            latest_file = model.objects.filter(structure=structure).latest('uploaded_at')
            break
    
    if latest_file:
        df = pd.read_excel(latest_file.file.path, engine='openpyxl')
        if 'Load Case Description' in df.columns:
            load_cases = df['Load Case Description'].dropna().unique().tolist()
            
            # Group load cases by prefix
            grouped_cases = {}
            for case in load_cases:
                if ' ' in case:
                    prefix = case.split(' ')[0]
                else:
                    prefix = case
                    
                if prefix not in grouped_cases:
                    grouped_cases[prefix] = []
                grouped_cases[prefix].append(case)
            
            return JsonResponse({'groups': grouped_cases})
    
    return JsonResponse({'error': 'No grouped load cases found'}, status=404)

def get_custom_groups(structure):
    """Get custom groups from database"""
    custom_groups = LoadCaseGroup.objects.filter(
        structure=structure, 
        is_custom=True
    ).prefetch_related('load_cases')
    
    groups_data = {}
    for group in custom_groups:
        groups_data[group.name] = [case.name for case in group.load_cases.all()]
    
    return JsonResponse({'custom_groups': groups_data})


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
                
                # Add resultant calculation and unique ID to each record
                for index, record in enumerate(calculation_data):
                    vert = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
                    trans = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
                    long = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
                    
                    # Calculate SQRT(Vert² + Trans² + Long²) for each record
                    resultant = math.sqrt(vert**2 + trans**2 + long**2)
                    record['Resultant'] = round(resultant, 2)
                    # Add unique ID for checkbox identification
                    record['record_id'] = f"record_{index}"
                    
                    # Add clean keys for template access
                    record['Structure_Loads_Vert'] = vert
                    record['Structure_Loads_Trans'] = trans
                    record['Structure_Loads_Long'] = long
                    # Store Set No. in data attribute
                    record['Set_No'] = record.get('Set No.', 'Unknown')
                
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
                    resultant_values = [record['Resultant'] for record in records]
                    
                    # Find the maximum resultant value
                    max_resultant = max(resultant_values)
                    max_index = resultant_values.index(max_resultant)
                    
                    # Store the actual values that created the max resultant
                    max_resultant_values[set_no] = {
                        'vert': vert_values[max_index],
                        'trans': trans_values[max_index],
                        'long': long_values[max_index],
                        'resultant': max_resultant,
                        'record_id': records[max_index]['record_id']  # Add record ID
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
    
    # Add record_id and clean keys to calculation data for template access
    for index, record in enumerate(calculation_data):
        record['record_id'] = f"record_{index}"
        # Add clean keys for template access
        record['Structure_Loads_Vert'] = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
        record['Structure_Loads_Trans'] = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
        record['Structure_Loads_Long'] = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
        record['Resultant'] = float(record.get('Resultant (lbs)', 0) or 0)
        # Store Set No. in data attribute
        record['Set_No'] = record.get('Set No.', 'Unknown')
    
    # Group calculation data by Set No. for debug display
    grouped_calculation_data = {}
    if calculation_data:
        for record in calculation_data:
            set_no = record.get('Set No.', 'Unknown')
            if set_no not in grouped_calculation_data:
                grouped_calculation_data[set_no] = []
            grouped_calculation_data[set_no].append(record)
    
    # Calculate factored loads for each load condition (initially for all records)
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
                },
                'all_records': factored_records  # Store all records for JavaScript filtering
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
    groups = StructureGroup.objects.all()
    return render(request, 'app1/home.html', {'structures': structures, 'groups': groups})

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

def add_group(request):
    if request.method == 'POST':
        form = StructureGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StructureGroupForm()
    return render(request, 'app1/add_group.html', {'form': form})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def rename_structure_group(request, group_id):
    """
    Renames a StructureGroup and returns JSON response.
    """
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            new_name = data.get('new_name')
            
            if not new_name:
                return JsonResponse({'status': 'error', 'message': 'Group name is required.'}, status=400)
            
            # Import your model
            from .models import StructureGroup
            
            group = get_object_or_404(StructureGroup, id=group_id)
            group.name = new_name
            group.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Group renamed successfully.', 
                'new_name': new_name
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def delete_structure(request, structure_id):
    structure = get_object_or_404(ListOfStructure, id=structure_id)
    structure.delete()
    return redirect('home')

@csrf_exempt
def delete_structure_group(request, group_id):
    """
    Permanently deletes a StructureGroup and returns JSON response.
    """
    if request.method == 'DELETE':
        group = get_object_or_404(StructureGroup, id=group_id)
        group.delete()  # Permanently delete the group
        return JsonResponse({'status': 'success', 'message': 'Group deleted successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

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

def tdeadend3_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TowerDeadend3, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend3FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tower_deadend_view3/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend3FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend3_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


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

def tdeadend4_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TowerDeadend4, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend4FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tower_deadend_view4/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend4FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend4_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

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


def tdeadend5_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TowerDeadend5, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend5FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/tower_deadend_view5/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend5FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend5_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

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

def tdeadend6_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend6, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend6FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view6/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend6FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend6_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

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

def tdeadend7_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend7, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend7FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view7/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend7FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend7_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def tdeadend8_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend8, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend8FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view8/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend8FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend8_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def tdeadend9_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend9, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend9FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view9/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend9FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend9_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def tdeadend10_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend10, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend10FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view10/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend10FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend10_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def tdeadend11_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(TDeadend11, pk=pk)  # Here
    
    if request.method == 'POST':
        form = TDeadend11FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/t_deadend_view11/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend11FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/tdeadend11_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

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
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # Initialize variables
    structure = None
    existing_data = False
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = HDeadend1.objects.filter(structure=structure).exists()
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/hdeadend1.html', {
                'form': HDeadendForm1(),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data
            })
        
        form = HDeadendForm1(request.POST)
        if form.is_valid():
            try:
                # Force the structure from URL parameter
                instance = form.save(commit=False)
                if structure:
                    instance.structure = structure
                instance.save()
                
                # Store structure info in session for upload page
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type
                request.session['circuit_structure_id'] = instance.id
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}')
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
    else:
        # GET request - create empty form
        form = HDeadendForm1()

    return render(request, 'app1/hdeadend1.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data
    })


def hdeadend1_update(request, pk):
    hdeadend = get_object_or_404(HDeadend1, pk=pk)

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = HDeadendForm1UpdateForm(request.POST, instance=hdeadend)
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}'
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm1UpdateForm(instance=hdeadend)

    return render(request, 'app1/hdeadend1_update.html', {
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })



def hupload1(request):
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if circuit data exists
            circuit_data_exists = HDeadend1.objects.filter(structure=structure).exists()
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        return HttpResponseRedirect(f'/hdeadend1/?structure_id={structure_id}&structure_type={structure_type}')
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = hUploadedFile1.objects.filter(structure=structure).exists()
            
            if existing_file_check:
                return render(request, 'app1/hupload1.html', {
                    'form': HUDeadendForm1(),
                    'structures_with_files': ListOfStructure.objects.filter(huploaded_files1__isnull=False).distinct(),
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = HUDeadendForm1(request.POST, request.FILES)
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases(instance)
                    
                    # Clear session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    request.session.pop('circuit_structure_id', None)
                    
                    # Redirect to show updated state
                    return HttpResponseRedirect(f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}')
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # NEW: Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = hUploadedFile1.objects.filter(structure=structure).exists()
        form = HUDeadendForm1()
        
    structures_with_files = ListOfStructure.objects.filter(huploaded_files1__isnull=False).distinct()

    # Handle AJAX requests for data (GET requests only)
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
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload1.html', {
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
    })

def hupload1_update(request):
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm1(request.POST, request.FILES)
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile1.objects.get(structure=structure)
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases(uploaded_file)
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload1_update')
                
            except hUploadedFile1.DoesNotExist:
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm1()

    return render(request, 'app1/hupload1_update.html', {
        'form': form
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

def hdeadend2_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(HDeadend2, pk=pk)  # Here
    
    if request.method == 'POST':
        form = HDeadendForm2UpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/h_deadend_view2/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm2UpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/hdeadend2_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def hupload2(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = HUDeadendForm2(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    extract_load_cases2(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('hupload2')
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
        
        # ADD: Handle custom group deletion (POST)
        elif 'delete_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse({'success': False, 'error': 'Structure ID and group name are required for deletion'})
        
        # ADD: Handle custom group update (POST)
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            structure_id = request.POST.get('structure_id')  # Optional
            
            if not old_group_name or not new_group_name:
                return JsonResponse({'success': False, 'error': 'Old and new group names are required'})
            
            try:
                if structure_id:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    groups = LoadCaseGroup.objects.filter(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                else:
                    groups = LoadCaseGroup.objects.filter(
                        name=old_group_name,
                        is_custom=True
                    )
                
                if not groups.exists():
                    return JsonResponse({'success': False, 'error': f'Group "{old_group_name}" not found'})
                
                for group in groups:
                    group.name = new_group_name
                    group.save()
                
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
        form = HUDeadendForm2()

    structures_with_files2 = ListOfStructure.objects.filter(huploaded_files2__isnull=False).distinct()
    
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')
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
                
            # REMOVE: Delete custom group via GET (we use POST now)
            # elif request.GET.get('delete_custom_group'):
            #     group_name = request.GET.get('group_name')
            #     if group_name:
            #         LoadCaseGroup.objects.filter(
            #             structure=structure, 
            #             name=group_name, 
            #             is_custom=True
            #         ).delete()
            #         return JsonResponse({'success': True})
            #     return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload2.html', {
        'form': form,
        'structures_with_files2': structures_with_files2
    })
    
    
from django.contrib.messages import get_messages
  
def hupload2_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """

    if request.method == 'POST':
        form = HUDeadendUpdateForm2(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile2.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases2(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload2_update')    # Change here 
                
            except hUploadedFile2.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm2()         # Change here 

    return render(request, 'app1/hupload2_update.html', {         # Change here 
        'form': form
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

def hdeadend3_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(HDeadend3, pk=pk)  # Here
    
    if request.method == 'POST':
        form = HDeadendForm3UpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/h_deadend_view3/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm3UpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/hdeadend3_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


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
        
        # Handle custom group deletion (POST) - ADD THIS
        elif 'delete_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse({'success': False, 'error': 'Structure ID and group name are required for deletion'})
        
        # Handle custom group update (POST) - ADD THIS
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            structure_id = request.POST.get('structure_id')  # Optional
            
            if not old_group_name or not new_group_name:
                return JsonResponse({'success': False, 'error': 'Old and new group names are required'})
            
            try:
                if structure_id:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    groups = LoadCaseGroup.objects.filter(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                else:
                    groups = LoadCaseGroup.objects.filter(
                        name=old_group_name,
                        is_custom=True
                    )
                
                if not groups.exists():
                    return JsonResponse({'success': False, 'error': f'Group "{old_group_name}" not found'})
                
                for group in groups:
                    group.name = new_group_name
                    group.save()
                
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
                
            # Remove the GET-based delete functionality since we're using POST now
            # elif request.GET.get('delete_custom_group'):
            #     group_name = request.GET.get('group_name')
            #     if group_name:
            #         LoadCaseGroup.objects.filter(
            #             structure=structure, 
            #             name=group_name, 
            #             is_custom=True
            #         ).delete()
            #         return JsonResponse({'success': True})
            #     return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload3.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })
    
    
def hupload3_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm3(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile3.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                hextract_load_cases3(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload3_update')    # Change here 
                
            except hUploadedFile3.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm3()         # Change here 

    return render(request, 'app1/hupload3_update.html', {         # Change here 
        'form': form
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

def hdeadend4_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(HDeadend4, pk=pk)  # Here
    
    if request.method == 'POST':
        form = HDeadendForm4UpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/h_deadend_view4/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm4UpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/hdeadend4_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

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
        
        # ADD: Handle custom group deletion (POST)
        elif 'delete_custom_group' in request.POST:
            structure_id = request.POST.get('structure_id')
            group_name = request.POST.get('group_name')
            
            if structure_id and group_name:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    LoadCaseGroup.objects.filter(
                        structure=structure, 
                        name=group_name, 
                        is_custom=True
                    ).delete()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse({'success': False, 'error': 'Structure ID and group name are required for deletion'})
        
        # ADD: Handle custom group update (POST)
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            structure_id = request.POST.get('structure_id')  # Optional
            
            if not old_group_name or not new_group_name:
                return JsonResponse({'success': False, 'error': 'Old and new group names are required'})
            
            try:
                if structure_id:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    groups = LoadCaseGroup.objects.filter(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                else:
                    groups = LoadCaseGroup.objects.filter(
                        name=old_group_name,
                        is_custom=True
                    )
                
                if not groups.exists():
                    return JsonResponse({'success': False, 'error': f'Group "{old_group_name}" not found'})
                
                for group in groups:
                    group.name = new_group_name
                    group.save()
                
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
                
            # REMOVE: Delete custom group via GET (we use POST now)
            # elif request.GET.get('delete_custom_group'):
            #     group_name = request.GET.get('group_name')
            #     if group_name:
            #         LoadCaseGroup.objects.filter(
            #             structure=structure, 
            #             name=group_name, 
            #             is_custom=True
            #         ).delete()
            #         return JsonResponse({'success': True})
            #     return JsonResponse({'success': False, 'error': 'Group name not provided'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'app1/hupload4.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })
    
    
def hupload4_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm4(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile4.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                hextract_load_cases4(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload4_update')    # Change here 
                
            except hUploadedFile4.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm4()         # Change here 

    return render(request, 'app1/hupload4_update.html', {         # Change here 
        'form': form
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





# Monopole

def mdeadend1(request):
    if request.method == 'POST':
        form = MDeadendForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload1/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm()

    return render(request, 'app1/mdeadend1.html', {'form': form})

def mdeadend1_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MonopoleDeadend, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend1FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/monopole_deadend_view/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend1FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend1_update.html', {'form': form, 'hdeadend': hdeadend}) # Here

def monopole_deadend_view(request):
    monopoles = MonopoleDeadend.objects.all()
    return render(request, 'app1/monopole_deadend_view.html', {'monopoles': monopoles})



def upload1(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = UploadedFileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases1(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload1')
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
        form = UploadedFileForm()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files1__isnull=False).distinct()  
      
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = UploadedFile1.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/upload1.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases1(uploaded_file):
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




def upload2(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = UploadedFileForm2(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases2(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload2')
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
        form = UploadedFileForm2()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files22__isnull=False).distinct()  
      
    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = UploadedFile22.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/upload2.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases2(uploaded_file):
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
        
        
        
def mdeadend5(request):
    if request.method == 'POST':
        form = MDeadendForm5(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload5/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm5()

    return render(request, 'app1/mdeadend5.html', {'form': form})

def mupload5(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm5(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases5(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload5')
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
        form = MUDeadendForm5()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files5__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile5.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload5.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases5(uploaded_file):
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
        
        
def m_deadend_view5(request):
    h = MDeadend5.objects.all()
    return render(request, 'app1/m_deadend_view5.html', {'h': h})


def mdeadend6(request):
    if request.method == 'POST':
        form = MDeadendForm6(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload6/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm6()

    return render(request, 'app1/mdeadend6.html', {'form': form})

def mupload6(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm6(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases6(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload6')
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
        form = MUDeadendForm6()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files6__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile6.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload6.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases6(uploaded_file):
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
        
        
def m_deadend_view6(request):
    h = MDeadend6.objects.all()
    return render(request, 'app1/m_deadend_view6.html', {'h': h})




def mdeadend7(request):
    if request.method == 'POST':
        form = MDeadendForm7(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload7/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm7()

    return render(request, 'app1/mdeadend7.html', {'form': form})

def mupload7(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm7(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases7(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload7')
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
        form = MUDeadendForm7()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files7__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile7.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload7.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases7(uploaded_file):
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
        
        
def m_deadend_view7(request):
    h = MDeadend7.objects.all()
    return render(request, 'app1/m_deadend_view7.html', {'h': h})


def mdeadend8(request):
    if request.method == 'POST':
        form = MDeadendForm8(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload8/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm8()

    return render(request, 'app1/mdeadend8.html', {'form': form})

def mupload8(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm8(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases8(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload8')
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
        form = MUDeadendForm8()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files8__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile8.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload8.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases8(uploaded_file):
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
        
        
def m_deadend_view8(request):
    h = MDeadend8.objects.all()
    return render(request, 'app1/m_deadend_view8.html', {'h': h})



def mdeadend9(request):
    if request.method == 'POST':
        form = MDeadendForm9(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload9/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm9()

    return render(request, 'app1/mdeadend9.html', {'form': form})

def mupload9(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm9(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases9(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload9')
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
        form = MUDeadendForm9()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files9__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile9.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload9.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases9(uploaded_file):
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
        
        
def m_deadend_view9(request):
    h = MDeadend9.objects.all()
    return render(request, 'app1/m_deadend_view9.html', {'h': h})


def mdeadend10(request):
    if request.method == 'POST':
        form = MDeadendForm10(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload10/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm10()

    return render(request, 'app1/mdeadend10.html', {'form': form})

def mupload10(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm10(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases10(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload10')
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
        form = MUDeadendForm10()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files10__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile10.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload10.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases10(uploaded_file):
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
        
        
def m_deadend_view10(request):
    h = MDeadend10.objects.all()
    return render(request, 'app1/m_deadend_view10.html', {'h': h})



def mdeadend11(request):
    if request.method == 'POST':
        form = MDeadendForm11(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload11/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm11()

    return render(request, 'app1/mdeadend11.html', {'form': form})

def mupload11(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm11(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases11(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload11')
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
        form = MUDeadendForm11()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files11__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile11.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload11.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases11(uploaded_file):
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
        
        
def m_deadend_view11(request):
    h = MDeadend11.objects.all()
    return render(request, 'app1/m_deadend_view11.html', {'h': h})



def mdeadend12(request):
    if request.method == 'POST':
        form = MDeadendForm12(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload12/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm12()

    return render(request, 'app1/mdeadend12.html', {'form': form})

def mupload12(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm12(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases12(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload12')
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
        form = MUDeadendForm12()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files12__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile12.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload12.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases12(uploaded_file):
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
        
        
def m_deadend_view12(request):
    h = MDeadend12.objects.all()
    return render(request, 'app1/m_deadend_view12.html', {'h': h})



def mdeadend13(request):
    if request.method == 'POST':
        form = MDeadendForm13(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/mupload13/')  # Redirect after successful save
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
        # if error: fall through to render form with errors

    else:
        form = MDeadendForm13()

    return render(request, 'app1/mdeadend13.html', {'form': form})

def mupload13(request):
    if request.method == 'POST':
        # Handle file upload form
        if 'file' in request.FILES:
            form = MUDeadendForm13(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    
                    # Extract load cases from the uploaded file
                    mextract_load_cases13(uploaded_file)
                    
                    messages.success(request, 'File uploaded successfully!')
                    return redirect('mupload13')
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
        form = MUDeadendForm13()

    structures_with_files = ListOfStructure.objects.filter(muploaded_files13__isnull=False).distinct()

    # Handle AJAX requests for data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile13.objects.filter(structure=structure).latest('uploaded_at')
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

    return render(request, 'app1/mupload13.html', {
        'form': form,
        'structures_with_files': structures_with_files
    })


def mextract_load_cases13(uploaded_file):
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
        
        
def m_deadend_view13(request):
    h = MDeadend13.objects.all()
    return render(request, 'app1/m_deadend_view13.html', {'h': h})


def mdeadend5_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend5, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend5FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view5/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend5FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend5_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend6_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend6, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend6FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view6/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend6FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend6_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend7_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend7, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend7FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view7/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend7FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend7_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend8_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend8, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend8FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view8/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend8FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend8_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend9_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend9, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend9FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view9/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend9FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend9_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend10_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend10, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend10FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view10/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend10FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend10_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend11_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend11, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend11FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view11/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend11FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend11_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend12_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend12, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend12FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view12/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend12FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend12_update.html', {'form': form, 'hdeadend': hdeadend}) # Here


def mdeadend13_update(request, pk):    # Here
    # Get the existing record or return 404
    hdeadend = get_object_or_404(MDeadend13, pk=pk)  # Here
    
    if request.method == 'POST':
        form = MDeadend13FormUpdateForm(request.POST, instance=hdeadend)  # Here
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/m_deadend_view13/')  # Here
            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend13FormUpdateForm(instance=hdeadend)   # Here

    return render(request, 'app1/mdeadend13_update.html', {'form': form, 'hdeadend': hdeadend}) # Here



    
def tupload1_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm1(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile1.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases1(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload1_update')    # Change here 
                
            except tUploadedFile1.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm1()         # Change here 

    return render(request, 'app1/tupload1_update.html', {         # Change here 
        'form': form
    })
    

def tupload2_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm2(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile2.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases3(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload2_update')    # Change here 
                
            except tUploadedFile2.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm2()         # Change here 

    return render(request, 'app1/tupload2_update.html', {         # Change here 
        'form': form
    })
    
    
    
def tupload3_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm3(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile3.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases33(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload3_update')    # Change here 
                
            except tUploadedFile3.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm3()         # Change here 

    return render(request, 'app1/tupload3_update.html', {         # Change here 
        'form': form
    })
    
    
    
def tupload4_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm4(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile4.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases4(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload4_update')    # Change here 
                
            except tUploadedFile4.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm4()         # Change here 

    return render(request, 'app1/tupload4_update.html', {         # Change here 
        'form': form
    })
    
    
def tupload5_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm5(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile5.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases5(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload5_update')    # Change here 
                
            except tUploadedFile5.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm5()         # Change here 

    return render(request, 'app1/tupload5_update.html', {         # Change here 
        'form': form
    })
    
    
def tupload6_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm6(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile6.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases6(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload6_update')    # Change here 
                
            except tUploadedFile6.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm6()         # Change here 

    return render(request, 'app1/tupload6_update.html', {         # Change here 
        'form': form
    })
    
def tupload7_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm7(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile7.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases7(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload7_update')    # Change here 
                
            except tUploadedFile7.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm7()         # Change here 

    return render(request, 'app1/tupload7_update.html', {         # Change here 
        'form': form
    })
    
    
def tupload8_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm8(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile8.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases8(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload8_update')    # Change here 
                
            except tUploadedFile8.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm8()         # Change here 

    return render(request, 'app1/tupload8_update.html', {         # Change here 
        'form': form
    })
    
    
def tupload9_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm9(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile9.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases9(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload9_update')    # Change here 
                
            except tUploadedFile9.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm9()         # Change here 

    return render(request, 'app1/tupload9_update.html', {         # Change here 
        'form': form
    })
    
def tupload10_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm10(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile10.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases10(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload10_update')    # Change here 
                
            except tUploadedFile10.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm10()         # Change here 

    return render(request, 'app1/tupload10_update.html', {         # Change here 
        'form': form
    })
    
def tupload11_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = TUDeadendUpdateForm11(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile11.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases11(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload11_update')    # Change here 
                
            except tUploadedFile11.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm11()         # Change here 

    return render(request, 'app1/tupload11_update.html', {         # Change here 
        'form': form
    })
    
    
    
def mupload1_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm1(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = UploadedFile1.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases1(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload1_update')    # Change here 
                
            except UploadedFile1.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm1()         # Change here 

    return render(request, 'app1/mupload1_update.html', {         # Change here 
        'form': form
    })
    
    
    
def mupload2_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm2(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = UploadedFile22.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases2(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload2_update')    # Change here 
                
            except UploadedFile22.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm2()         # Change here 

    return render(request, 'app1/mupload2_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload5_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm5(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile5.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases5(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload5_update')    # Change here 
                
            except mUploadedFile5.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm5()         # Change here 

    return render(request, 'app1/mupload5_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload6_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm6(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile6.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases6(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload6_update')    # Change here 
                
            except mUploadedFile6.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm6()         # Change here 

    return render(request, 'app1/mupload6_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload7_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm7(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile7.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases7(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload7_update')    # Change here 
                
            except mUploadedFile7.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm7()         # Change here 

    return render(request, 'app1/mupload7_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload8_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm8(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile8.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases8(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload8_update')    # Change here 
                
            except mUploadedFile8.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm8()         # Change here 

    return render(request, 'app1/mupload8_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload9_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm9(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile9.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases9(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload9_update')    # Change here 
                
            except mUploadedFile9.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm9()         # Change here 

    return render(request, 'app1/mupload9_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload10_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm10(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile10.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases10(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload10_update')    # Change here 
                
            except mUploadedFile10.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm10()         # Change here 

    return render(request, 'app1/mupload10_update.html', {         # Change here 
        'form': form
    })
    
def mupload11_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm11(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile11.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases11(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload11_update')    # Change here 
                
            except mUploadedFile11.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm11()         # Change here 

    return render(request, 'app1/mupload11_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload12_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm12(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile12.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases12(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload12_update')    # Change here 
                
            except mUploadedFile12.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm12()         # Change here 

    return render(request, 'app1/mupload12_update.html', {         # Change here 
        'form': form
    })
    
    
def mupload13_update(request):   # Change here 
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = MUDeadendUpdateForm13(request.POST, request.FILES)   # Change here 
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile13.objects.get(structure=structure)  # Change here 
                
                # Delete the old file from storage
                uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases13(uploaded_file)       # Change here 
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload13_update')    # Change here 
                
            except mUploadedFile13.DoesNotExist:       # Change here 
                messages.error(request, 'No uploaded file found for this structure.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm13()         # Change here 

    return render(request, 'app1/mupload13_update.html', {         # Change here 
        'form': form
    })