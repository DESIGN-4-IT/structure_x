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




import time
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import ListOfStructure, TowerDeadend
from .forms import TowerDeadendForm

def tdeadend(request):
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [Tower Circuit Definition Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TowerDeadend.objects.filter(structure=structure).exists()
            
            # Get the latest record if data exists
            if existing_data:
                existing_circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing TowerDeadend data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TowerDeadend.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TowerDeadend data found for structure ID: {structure_id}")
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Pass session data to upload page with circuit_id
            circuit_id = existing_circuit_data.id if existing_circuit_data else None
            if circuit_id:
                return HttpResponseRedirect(
                    f'/tupload1/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={circuit_id}'
                    f'&popup_actions={",".join(request.session.get("active_popups", []))}'
                )
            else:
                return HttpResponseRedirect(
                    f'/tupload1/?structure_id={structure_id}&structure_type={structure_type}'
                    f'&popup_actions={",".join(request.session.get("active_popups", []))}'
                )
        else:
            return redirect('home')
    
    # 🔥 CRITICAL FIX: Check if this is a redirect from a successful POST
    # If we have circuit_id in GET params and data exists, show the existing data view
    if request.method == 'GET' and request.GET.get('circuit_id'):
        try:
            circuit_id = request.GET.get('circuit_id')
            existing_circuit_data = TowerDeadend.objects.get(id=circuit_id)
            existing_data = True
            
            # Force re-check existing data to ensure we show the right view
            if structure_id:
                existing_data = TowerDeadend.objects.filter(structure_id=structure_id).exists()
                if existing_data:
                    existing_circuit_data = TowerDeadend.objects.filter(structure_id=structure_id).latest('id')
            
            print(f"DEBUG [Redirect with circuit_id] - Showing existing data view for circuit_id: {circuit_id}")
        except (TowerDeadend.DoesNotExist, ValueError):
            pass
    
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # If data already exists, prevent saving new data
        if existing_data:
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Data already exists for this structure.'
                })
            return render(request, 'app1/tdeadend.html', {
                'form': TowerDeadendForm(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'existing_circuit_data': existing_circuit_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', '')
            })
        
        form = TowerDeadendForm(request.POST)
        if form.is_valid():
            try:
                # Force the structure from URL parameter
                instance = form.save(commit=False)
                if structure:
                    instance.structure = structure
                instance.save()
                
                # 🔥 IMPORTANT: Immediately update existing_data flag
                existing_data = True
                existing_circuit_data = instance
                
                # Store structure info in session for upload page
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type
                request.session['circuit_structure_id'] = instance.id
                
                # Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TowerDeadend',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [Tower Circuit Definition] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # For AJAX request, return success response with redirect URL
                if is_ajax:
                    # 🔥 Return a redirect URL instead of success message
                    return JsonResponse({
                        'status': 'success_redirect',
                        'redirect_url': f'/tdeadend/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={instance.id}&refresh=true',
                        'message': 'Data saved successfully',
                        'structure_id': structure_id,
                        'structure_type': structure_type,
                        'circuit_id': instance.id
                    })
                
                # 🔥 For non-AJAX request, redirect back to same page with circuit_id
                # This ensures the page shows existing data view after refresh
                return HttpResponseRedirect(
                    f'/tdeadend/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={instance.id}&refresh=true'
                )
                
            except IntegrityError:
                error_msg = 'Data already added for this structure.'
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'errors': {'__all__': [error_msg]}
                    })
                form.add_error('structure', error_msg)
            except Exception as e:
                error_msg = f'Error saving data: {str(e)}'
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'errors': {'__all__': [error_msg]}
                    })
                form.add_error(None, error_msg)
        else:
            # Form is invalid
            print(f"DEBUG [Tower Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            
            # For AJAX request, return errors in JSON format
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                })
    
    else:
        # GET request - create form
        # Check if we should show popup immediately (after redirect from successful save)
        show_popup_immediately = request.GET.get('refresh') == 'true'
        
        if existing_data and existing_circuit_data:
            form = TowerDeadendForm(instance=existing_circuit_data)
            
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TowerDeadend',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Tower Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
            
            # 🔥 If we're coming from a successful save, show popup immediately
            if show_popup_immediately:
                print(f"DEBUG [Show Popup Immediately] - Redirected from successful save")
        else:
            # Create empty form for new data
            form = TowerDeadendForm()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [Tower GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")
        print(f"  Show popup immediately: {show_popup_immediately}")

    return render(request, 'app1/tdeadend.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'existing_circuit_data': existing_circuit_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
        'show_popup_immediately': show_popup_immediately,  # 🔥 Pass this to template
    })

def tdeadend_update(request, pk):
    tdeadend = get_object_or_404(TowerDeadend, pk=pk)

    selected_structure = tdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadendFormUpdateForm(request.POST, instance=tdeadend)
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload1/?structure_id={structure_id}&structure_type={structure_type}'
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadendFormUpdateForm(instance=tdeadend)

    return render(request, 'app1/tdeadend_update.html', {
        'form': form,
        'tdeadend': tdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })


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
@csrf_exempt
def store_set_phase_combinations(request):
    try:
        # Load the JSON data sent from the frontend
        data = json.loads(request.body)
        
        # The data should contain the list of combinations and the status
        combinations_to_add = data.get('combinations', [])
        status = data.get('status')  # 'Ahead' or 'Back' only now
        
        print(f"DEBUG store_set_phase_combinations: Received {len(combinations_to_add)} combinations: {combinations_to_add}")
        print(f"DEBUG: Status: {status}")
        
        # MODIFIED: Remove 'Both' from valid status options
        if not combinations_to_add or status not in ['Ahead', 'Back']:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'}, status=400)

        # Get the current active combinations from the session
        selected_values = request.session.get('selected_values', {})
        active_combinations = selected_values.get('active_combinations', [])
        
        print(f"DEBUG: Existing active_combinations before extend: {len(active_combinations)} items")
        
        # Process the new combinations: Add the status
        new_active_combinations = []
        for combo in combinations_to_add:
            combo_with_status = f"{combo}-{status}"
            if combo_with_status not in active_combinations:  # Prevent duplicates
                new_active_combinations.append(combo_with_status)
            else:
                print(f"DEBUG: Skipped duplicate combination: {combo_with_status}")
        
        active_combinations.extend(new_active_combinations)
        
        print(f"DEBUG: Added {len(new_active_combinations)} new combinations. Total active_combinations: {len(active_combinations)}")
        print(f"DEBUG: Final active_combinations: {active_combinations}")
        
        # Update the session
        request.session['selected_values']['active_combinations'] = active_combinations
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Successfully stored {len(new_active_combinations)} new combinations as {status}.',
            'new_combinations': new_active_combinations
        })
    except json.JSONDecodeError:
        print("DEBUG: JSON decode error")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Error storing combinations: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def debug_session_selections(session_data):
    """Helper to debug session data"""
    print("\n🔍 SESSION DATA DEBUG:")
    print(f"Structure Type: {session_data.get('selected_structure_type')}")
    
    popup_selections = session_data.get('popup_selections', {})
    print(f"Popup Selections: {popup_selections}")
    
    circuit_def = session_data.get('circuit_definition', {})
    print(f"Circuit Definition: {circuit_def}")
    
    # Print all stored models for reference
    from .models import TowerModel
    all_models = TowerModel.objects.all()
    print(f"\n📦 AVAILABLE MODELS IN DATABASE ({all_models.count()} total):")
    for model in all_models:
        print(f"  - {model.name}: {model.structure_type}/{model.attachment_points}/{model.configuration}/{model.circuit_type}")

def find_matching_model(session_data):
    """
    Find a 3D model that matches ALL session selections including complete circuit definition
    """
    from .models import TowerModel
    
    # Extract data from session
    structure_type = session_data.get('selected_structure_type')
    popup_selections = session_data.get('popup_selections', {})
    circuit_definition = session_data.get('circuit_definition', {})
    
    # Get attachment points and configuration from popups
    attachment_points = popup_selections.get('attachment_points')
    configuration = popup_selections.get('configuration')
    
    # DEBUG: Print all selection data
    print(f"\n🎯 DEBUG [find_matching_model] - User Selections:")
    print(f"  Structure Type: {structure_type}")
    print(f"  Attachment Points: {attachment_points}")
    print(f"  Configuration: {configuration}")
    print(f"  Circuit Definition: {circuit_definition}")
    
    # Convert to integers safely
    num_3_phase = 0
    num_1_phase = 0
    
    try:
        num_3_phase = int(circuit_definition.get('num_3_phase_circuits', 0) or 0)
    except (ValueError, TypeError):
        num_3_phase = 0
        
    try:
        num_1_phase = int(circuit_definition.get('num_1_phase_circuits', 0) or 0)
    except (ValueError, TypeError):
        num_1_phase = 0
    
    # CORRECT CIRCUIT TYPE CALCULATION FOR TRANSMISSION LINE STRUCTURES:
    # Priority: 3-Phase Circuits > 1-Phase Circuits
    # Shield wires and comm cables typically don't count as separate circuits
    
    if num_3_phase >= 3:
        circuit_type = 'tc'  # Triple Circuit
    elif num_3_phase == 2:
        circuit_type = 'dc'  # Double Circuit
    elif num_3_phase == 1:
        circuit_type = 'sc'  # Single Circuit
    elif num_1_phase >= 3:
        circuit_type = 'tc'  # Triple Circuit (1-phase bundles)
    elif num_1_phase == 2:
        circuit_type = 'dc'  # Double Circuit (1-phase bundles)
    elif num_1_phase == 1:
        circuit_type = 'sc'  # Single Circuit (1-phase bundle)
    else:
        circuit_type = 'sc'  # Default to Single Circuit
    
    print(f"  Calculated Circuit Type: {circuit_type}")
    print(f"    Based on: 3-Phase Circuits={num_3_phase}, 1-Phase Circuits={num_1_phase}")
    
    # Try to find EXACT match first
    matching_model = TowerModel.objects.filter(
        structure_type=structure_type,
        attachment_points=attachment_points,
        configuration=configuration,
        circuit_type=circuit_type
    ).first()
    
    if matching_model:
        print(f"  ✓ Found EXACT match: {matching_model.name}")
        return matching_model
    
    print(f"  ⚠ No exact match found, trying naming convention...")
    
    # FIXED NAMING CONVENTION MAPPING:
    # Structure type prefix
    if structure_type == 'hframes':
        prefix = "HFrame"
    elif structure_type == 'towers':
        prefix = "Tower"
    elif structure_type == 'monopoles':
        prefix = "MP"
    else:
        prefix = structure_type.capitalize() if structure_type else ""
    
    # FIXED: Attachment points mapping (DE vs Tan)
    if attachment_points == 'deadend':
        attachment_code = "DE"
    elif attachment_points == 'tangent':
        attachment_code = "Tan"
    else:
        attachment_code = ""
    
    # FIXED: Configuration mapping (Vert vs Horiz)
    if configuration == 'vertical':
        config_code = "Vert"
    elif configuration == 'horizontal':
        config_code = "Horiz"
    elif configuration == 'delta':
        config_code = "Delta"
    elif configuration == 'hetic':
        config_code = "Hetic"
    else:
        config_code = configuration.capitalize() if configuration else ""
    
    # Circuit type code
    circuit_code = circuit_type.upper()  # SC, DC, TC
    
    # Generate the expected name based on your naming pattern
    expected_name = f"{prefix}_{attachment_code}_{config_code}_{circuit_code}"
    print(f"  Looking for model with name pattern: {expected_name}")
    
    # FIRST: Try to find by exact name
    exact_name_match = TowerModel.objects.filter(name__iexact=expected_name).first()
    if exact_name_match:
        print(f"  ✓ Found EXACT name match: {exact_name_match.name}")
        return exact_name_match
    
    # SECOND: Try to find by name containing all parts
    name_query = TowerModel.objects.all()
    
    # Add filters based on name parts
    if prefix:
        name_query = name_query.filter(name__icontains=prefix)
    if attachment_code:
        name_query = name_query.filter(name__icontains=attachment_code)
    if config_code:
        name_query = name_query.filter(name__icontains=config_code)
    if circuit_code:
        name_query = name_query.filter(name__icontains=circuit_code)
    
    # Get all matching by name
    name_matches = list(name_query)
    
    if name_matches:
        print(f"  Found {len(name_matches)} name matches:")
        for match in name_matches:
            print(f"    - {match.name} ({match.structure_type}/{match.attachment_points}/{match.configuration}/{match.circuit_type})")
        return name_matches[0]
    
    # THIRD: Try fuzzy matching
    print(f"  Trying fuzzy matching...")
    all_models = TowerModel.objects.all()
    best_match = None
    best_score = 0
    
    for model in all_models:
        score = 0
        
        # Check structure type (most important - 30 points)
        if model.structure_type == structure_type:
            score += 30
        
        # Check attachment points (25 points)
        if model.attachment_points == attachment_points:
            score += 25
        
        # Check configuration (25 points)
        if model.configuration == configuration:
            score += 25
        
        # Check circuit type (20 points)
        if model.circuit_type == circuit_type:
            score += 20
        
        # Check name contains expected parts
        model_name_upper = model.name.upper()
        expected_parts = [prefix.upper(), attachment_code.upper(), config_code.upper(), circuit_code]
        for part in expected_parts:
            if part and part in model_name_upper:
                score += 5
        
        if score > best_score:
            best_score = score
            best_match = model
    
    if best_match and best_score >= 50:
        print(f"  ✓ Found BEST fuzzy match: {best_match.name} (score: {best_score})")
        print(f"    Details: {best_match.structure_type}/{best_match.attachment_points}/{best_match.configuration}/{best_match.circuit_type}")
        return best_match
    
    # FINAL FALLBACK: Get first model of the correct structure type
    print(f"  ⚠ Falling back to first {structure_type} model")
    fallback = TowerModel.objects.filter(structure_type=structure_type).first()
    if fallback:
        print(f"  Using: {fallback.name}")
    return fallback

def hdata1(request):
    # DEBUG: Print all session data at the start of hdata1
    debug_session_selections(request.session)
    
    print(f"\n📊 DEBUG [hdata1 Page] - Detailed session data:")
    print(f"  1. Home Page Data:")
    print(f"     Structure Type: {request.session.get('selected_structure_type')}")
    print(f"     Structure ID: {request.session.get('selected_structure_id')}")
    print(f"     Active Popups: {request.session.get('active_popups', [])}")
    print(f"     Popup Selections: {request.session.get('popup_selections', {})}")
    
    print(f"  2. Circuit Definition Data:")
    circuit_definition = request.session.get('circuit_definition', {})
    print(f"     Num 3-Phase Circuits: {circuit_definition.get('num_3_phase_circuits')}")
    print(f"     Num Shield Wires: {circuit_definition.get('num_shield_wires')}")
    print(f"     Num 1-Phase Circuits: {circuit_definition.get('num_1_phase_circuits')}")
    print(f"     Num Communication Cables: {circuit_definition.get('num_communication_cables')}")
    print(f"     Circuit Model: {circuit_definition.get('circuit_model')}")
    print(f"     Circuit ID: {circuit_definition.get('circuit_id')}")
    
    print(f"  3. Selection Values:")
    print(f"     Selected Values: {request.session.get('selected_values', {})}")
    
    # ================== FIX 1: ADD TYPE CHECK FOR selected_values ==================
    # Get selected values from session - ensure it's always a dictionary
    selected_values = request.session.get('selected_values', {})
    
    # FIX: Ensure selected_values is a dictionary, not a list
    if isinstance(selected_values, list):
        print(f"⚠️ WARNING: selected_values is a list with {len(selected_values)} items, converting to dict")
        print(f"   List content: {selected_values}")
        request.session['selected_values'] = {}
        selected_values = {}
    # ===============================================================================
    
    # Find matching model based on all selections
    matching_model = find_matching_model(request.session)
    print(f"\n🔍 DEBUG [hdata1] - Matching Results:")
    if matching_model:
        print(f"  ✓ Found matching model: {matching_model.name}")
        print(f"    ID: {matching_model.id}")
        print(f"    Type: {matching_model.structure_type}")
        print(f"    Attachment: {matching_model.attachment_points}")
        print(f"    Configuration: {matching_model.configuration}")
        print(f"    Circuit: {matching_model.circuit_type}")
    else:
        print(f"  ⚠ No matching model found")

    available_models = TowerModel.objects.all().order_by('name')
    selected_model_id = request.session.get('selected_model_id')
    
    # AUTO-SELECT matched model if available
    if matching_model:
        selected_model_id = matching_model.id
        request.session['selected_model_id'] = selected_model_id
        request.session['matched_model_id'] = matching_model.id
        print(f"  🎯 AUTO-SELECTING matched model ID: {selected_model_id} ({matching_model.name})")
    elif selected_model_id:
        # Keep existing selection if no match found
        print(f"  🔄 Keeping existing selection ID: {selected_model_id}")
    
    # Handle POST requests for model selection
    if request.method == 'POST':
        # Handle manual model selection
        if 'selected_model' in request.POST:
            selected_model_id = request.POST.get('selected_model')
            if selected_model_id:
                request.session['selected_model_id'] = selected_model_id
                print(f"  🔄 User manually selected model ID: {selected_model_id}")
                
                # Clear matched model flag since user made manual choice
                if 'matched_model_id' in request.session:
                    del request.session['matched_model_id']
            else:
                # Clear selection if "None" is selected
                request.session.pop('selected_model_id', None)
                # If user cleared selection, revert to matched model
                if matching_model:
                    selected_model_id = matching_model.id
                    request.session['selected_model_id'] = selected_model_id
                    request.session['matched_model_id'] = matching_model.id
                    print(f"  🔄 User cleared selection, reverting to matched model")
        
        # Handle new model upload
        if 'tower_model_file' in request.FILES:
            model_name = request.POST.get('model_name', 'Unnamed Model')
            model_file = request.FILES['tower_model_file']
            
            # Validate file type
            if model_file.name.endswith(('.glb', '.gltf')):
                # Get categorization from form
                structure_type = request.POST.get('structure_type')
                attachment_points = request.POST.get('attachment_points')
                configuration = request.POST.get('configuration')
                circuit_type = request.POST.get('circuit_type')
                
                new_model = TowerModel.objects.create(
                    name=model_name,
                    model_file=model_file,
                    structure_type=structure_type,
                    attachment_points=attachment_points,
                    configuration=configuration,
                    circuit_type=circuit_type
                )
                
                # Optionally select the newly uploaded model
                request.session['selected_model_id'] = new_model.id
                selected_model_id = new_model.id
                print(f"  📤 New model uploaded and selected: {new_model.name} (ID: {new_model.id})")
    
    # Get selected model if any
    selected_model = None
    if selected_model_id:
        try:
            selected_model = TowerModel.objects.get(id=selected_model_id)
            print(f"  📊 Current selected model: {selected_model.name} (ID: {selected_model.id})")
            print(f"    Details: {selected_model.structure_type}/{selected_model.attachment_points}/{selected_model.configuration}/{selected_model.circuit_type}")
        except TowerModel.DoesNotExist:
            print(f"  ❌ Selected model ID {selected_model_id} not found")
            selected_model = None
            
    # ENSURE we always have a selected model
    if not selected_model:
        if matching_model:
            selected_model = matching_model
            print(f"  🆘 Fallback to matching model: {selected_model.name}")
        elif available_models.exists():
            selected_model = available_models.first()
            print(f"  ⚠ No match found, selecting first available: {selected_model.name}")
        else:
            print(f"  ⚠ No models available in database")
    
    # Store model info in session for frontend
    if selected_model:
        request.session['selected_model_url'] = selected_model.get_file_url()
        request.session['selected_model_name'] = selected_model.name
        request.session['selected_model_details'] = {
            'structure_type': selected_model.structure_type,
            'attachment_points': selected_model.attachment_points,
            'configuration': selected_model.configuration,
            'circuit_type': selected_model.circuit_type
        }
    
    # Get all session data to pass to template - UPDATED with type check
    # Note: selected_values is already defined above with type checking
    active_combinations = selected_values.get('active_combinations', [])
    structure_id = selected_values.get('structure_id')
    button_type = selected_values.get('button_type', '')
    
    # Get circuit definition data from session
    circuit_definition = request.session.get('circuit_definition', {})
    
    # Process structure data if structure_id exists
    joint_labels = []
    set_numbers = []
    phase_numbers = []
    load_data = []
    df_columns = []
    
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
            df_columns = list(df.columns)

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
            df_columns = []
            print(f"Error processing Excel file: {str(e)}")
    
    # ================== FIX 2: ENSURE selected_values IS A DICT ==================
    # Initialize session storage for selections
    if 'selected_values' not in request.session:
        request.session['selected_values'] = {}
    
    # FIX: Ensure selected_values is always a dictionary
    if not isinstance(request.session.get('selected_values'), dict):
        print(f"⚠️ WARNING: selected_values in session is not a dict, resetting")
        request.session['selected_values'] = {}
    # =============================================================================
    
    # Initialize empty arrays if they don't exist
    if 'selected_joints' not in request.session['selected_values']:
        request.session['selected_values']['selected_joints'] = []
    
    if 'active_combinations' not in request.session['selected_values']:
        request.session['selected_values']['active_combinations'] = []
    
    # Get current selections from session
    selected_joints = request.session['selected_values'].get('selected_joints', [])
    active_combinations = request.session['selected_values'].get('active_combinations', [])
    
    # Build filter criteria
    filter_criteria = {}

    # Store joint labels if any are selected
    if selected_joints:
        filter_criteria['joint_labels'] = selected_joints

    # Store set-phase combinations if any are active - UPDATED to always use dicts
    set_phase_pairs = []
    if active_combinations:
        for combo in active_combinations:
            if isinstance(combo, str):
                # Format: "1-2-Ahead" -> extract set and phase
                parts = combo.split('-')
                if len(parts) >= 2:
                    set_phase_pairs.append({'set': parts[0], 'phase': parts[1]})
            elif isinstance(combo, dict):
                # Handle dictionary format (normalize values to strings)
                set_val = str(combo.get('set', ''))
                phase_val = str(combo.get('phase', ''))
                if set_val and phase_val:
                    set_phase_pairs.append({'set': set_val, 'phase': phase_val})

    if set_phase_pairs:
        filter_criteria['set_phase_combinations'] = set_phase_pairs
    
    # Store filter criteria in session
    request.session['selected_values']['filter_criteria'] = filter_criteria
    request.session.modified = True

    # Calculate total circuits for display
    total_circuits = 0
    if circuit_definition:
        num_3_phase = int(circuit_definition.get('num_3_phase_circuits', 0) or 0)
        num_1_phase = int(circuit_definition.get('num_1_phase_circuits', 0) or 0)
        total_circuits = num_3_phase + num_1_phase

    # Prepare context data including all session information
    context = {
        # Model selection context
        'available_models': available_models,
        'selected_model': selected_model,
        'matching_model': matching_model,
        
        # Structure data context
        'joint_labels': joint_labels,
        'set_numbers': set_numbers,
        'phase_numbers': phase_numbers,
        'load_data': load_data,
        'load_data_json': json.dumps(load_data),
        'all_columns': df_columns,
        
        # Selection context
        'selected_values': selected_values,  # This is now guaranteed to be a dict
        'button_type': button_type,
        'structure_id': structure_id,
        'filter_criteria': filter_criteria,
        'selected_joints': selected_joints,
        'active_combinations': active_combinations,
        
        # Session data from Home Page and Circuit Definition
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_structure_id': request.session.get('selected_structure_id', ''),
        'session_active_popups': request.session.get('active_popups', []),
        'session_popup_selections': request.session.get('popup_selections', {}),
        'session_circuit_definition': circuit_definition,
        'session_total_circuits': total_circuits,
        
        # Model matching info
        'matched_model_info': {
            'structure_type': matching_model.structure_type if matching_model else None,
            'attachment_points': matching_model.attachment_points if matching_model else None,
            'configuration': matching_model.configuration if matching_model else None,
            'circuit_type': matching_model.circuit_type if matching_model else None,
        } if matching_model else None,
        
        # Selection comparison for debugging
        'selection_comparison': {
            'user_structure': request.session.get('selected_structure_type'),
            'user_attachment': request.session.get('popup_selections', {}).get('attachment_points'),
            'user_configuration': request.session.get('popup_selections', {}).get('configuration'),
            'model_structure': selected_model.structure_type if selected_model else None,
            'model_attachment': selected_model.attachment_points if selected_model else None,
            'model_configuration': selected_model.configuration if selected_model else None,
            'is_matched': selected_model == matching_model if selected_model and matching_model else False
        } if selected_model else {}
    }
    
    print(f"\n✅ [hdata1] Context prepared:")
    print(f"  Selected Model: {selected_model.name if selected_model else 'None'}")
    print(f"  Matching Model: {matching_model.name if matching_model else 'None'}")
    print(f"  Models Match: {selected_model == matching_model if selected_model and matching_model else False}")
    print(f"  selected_values type: {type(selected_values)}")
    print(f"  selected_values content: {selected_values}")
    
    return render(request, 'app1/hdata1.html', context)

# Add this function to your views.py
def update_selection_session(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            selected_joints = request.POST.getlist('selected_joints[]')
            active_combinations_json = request.POST.get('active_combinations', '[]')
            
            try:
                active_combinations = json.loads(active_combinations_json)
            except json.JSONDecodeError:
                active_combinations = []
            
            print(f"DEBUG update_selection_session: Received {len(active_combinations)} raw combinations: {active_combinations}")  # NEW: Log raw input
            
            # Normalize combinations for consistent filtering
            normalized_combinations = []
            for combo in active_combinations:
                normalized_combo = {}
                for key, value in combo.items():
                    if isinstance(value, (int, float)):
                        if value == int(value):
                            normalized_combo[key] = str(int(value))
                        else:
                            normalized_combo[key] = str(value)
                    else:
                        normalized_combo[key] = str(value).strip()
                normalized_combinations.append(normalized_combo)
            
            print(f"DEBUG: Normalized to {len(normalized_combinations)} combinations: {normalized_combinations}")  # NEW: Log normalized output
            
            if 'selected_values' not in request.session:
                request.session['selected_values'] = {}
            
            request.session['selected_values']['selected_joints'] = selected_joints
            request.session['selected_values']['active_combinations'] = normalized_combinations  # Note: This overwrites with dicts
            
            # Build filter criteria
            filter_criteria = {}
            if selected_joints:
                filter_criteria['joint_labels'] = selected_joints
            if normalized_combinations:
                filter_criteria['set_phase_combinations'] = normalized_combinations
            
            request.session['selected_values']['filter_criteria'] = filter_criteria
            request.session.modified = True
            
            print(f"DEBUG: Updated session with {len(normalized_combinations)} combinations. Filter criteria: {filter_criteria}")  # NEW: Log final session update
            
            return JsonResponse({
                'success': True,
                'selected_joints': selected_joints,
                'active_combinations': normalized_combinations,
                'filter_criteria': filter_criteria
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def apply_previous_selection_filter(structure_id, filter_criteria, selected_load_cases=None):
    """Apply filter criteria and return data with grouping support"""
    try:
        structure = ListOfStructure.objects.get(id=structure_id)
        
        # Try to get the latest file
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
            print("DEBUG: No file found for structure")
            return []
        
        df = pd.read_excel(latest_file.file.path, engine='openpyxl')
        
        # Apply filter criteria
        filtered_df = df.copy()
        
        print(f"DEBUG: Original DataFrame shape: {df.shape}")
        print(f"DEBUG: Filter criteria: {filter_criteria}")
        print(f"DEBUG: Selected load cases: {selected_load_cases}")
        
        # NEW: Debug what values actually exist in the DataFrame
        if 'Set No.' in df.columns and 'Phase No.' in df.columns:
            unique_sets = df['Set No.'].dropna().unique()
            unique_phases = df['Phase No.'].dropna().unique()
            print(f"DEBUG: Unique Set values in data: {sorted([str(x) for x in unique_sets])}")
            print(f"DEBUG: Unique Phase values in data: {sorted([str(x) for x in unique_phases])}")
        
        if 'Load Case Description' in df.columns:
            unique_load_cases = df['Load Case Description'].dropna().unique()
            print(f"DEBUG: Unique Load Cases in data: {sorted([str(x) for x in unique_load_cases])}")
        
        # If no filter criteria and no selected load cases, return all data
        if not filter_criteria and not selected_load_cases:
            print("DEBUG: No filters applied, returning all data")
            # Convert to list of dictionaries
            result_data = []
            for _, row in filtered_df.iterrows():
                row_data = {}
                for col in filtered_df.columns:
                    if pd.notna(row[col]):
                        if pd.api.types.is_numeric_dtype(filtered_df[col]):
                            row_data[col] = float(row[col])
                        else:
                            row_data[col] = str(row[col])
                    else:
                        row_data[col] = '' if pd.api.types.is_string_dtype(filtered_df[col]) else 0
                result_data.append(row_data)
            return result_data
        
        # Filter by joint labels if present
        if filter_criteria and 'joint_labels' in filter_criteria and filter_criteria['joint_labels']:
            if 'Joint Label' in df.columns:
                # Convert joint labels to strings for comparison
                joint_labels = [str(label) for label in filter_criteria['joint_labels']]
                print(f"DEBUG: Filtering by joint labels: {joint_labels}")
                filtered_df = filtered_df[filtered_df['Joint Label'].astype(str).isin(joint_labels)]
                print(f"DEBUG: After joint filter: {filtered_df.shape}")
        
        # Filter by set+phase combinations if present - FIXED VERSION
        if filter_criteria and 'set_phase_combinations' in filter_criteria and filter_criteria['set_phase_combinations']:
            if 'Set No.' in df.columns and 'Phase No.' in df.columns:
                print(f"DEBUG: Filtering by {len(filter_criteria['set_phase_combinations'])} set+phase combinations")
                
                # Create a list to store filtered dataframes
                filtered_dfs = []
                
                for i, combo in enumerate(filter_criteria['set_phase_combinations']):
                    # Convert filter values to handle both integer and float representations
                    set_value = str(combo.get('set', ''))
                    phase_value = str(combo.get('phase', ''))
                    
                    # NEW: Handle float values in Excel data (e.g., '9' should match '9.0')
                    # Try to convert to float and then compare both string representations
                    try:
                        set_float = float(set_value)
                        phase_float = float(phase_value)
                        
                        # Create multiple comparison options
                        set_match = (
                            (filtered_df['Set No.'].astype(str) == set_value) |  # Exact string match
                            (filtered_df['Set No.'].astype(str) == str(set_float)) |  # Float string match
                            (filtered_df['Set No.'].astype(float) == set_float)  # Numeric match
                        )
                        
                        phase_match = (
                            (filtered_df['Phase No.'].astype(str) == phase_value) |  # Exact string match
                            (filtered_df['Phase No.'].astype(str) == str(phase_float)) |  # Float string match
                            (filtered_df['Phase No.'].astype(float) == phase_float)  # Numeric match
                        )
                        
                    except (ValueError, TypeError):
                        # If conversion fails, use string comparison only
                        set_match = (filtered_df['Set No.'].astype(str) == set_value)
                        phase_match = (filtered_df['Phase No.'].astype(str) == phase_value)
                    
                    print(f"DEBUG: Combination {i}: Looking for Set='{set_value}' (also trying as float), Phase='{phase_value}' (also trying as float)")
                    
                    # Filter for this specific combination
                    combo_filtered = filtered_df[set_match & phase_match]
                    
                    print(f"DEBUG: Found {len(combo_filtered)} records for this combination")
                    
                    if not combo_filtered.empty:
                        filtered_dfs.append(combo_filtered)
                        # Show sample of what was found
                        sample = combo_filtered[['Set No.', 'Phase No.', 'Load Case Description']].head(3)
                        print(f"DEBUG: Sample of found records:\n{sample.to_string()}")
                
                # Combine all filtered dataframes
                if filtered_dfs:
                    filtered_df = pd.concat(filtered_dfs, ignore_index=True)
                    print(f"DEBUG: After set+phase filter: {filtered_df.shape}")
                    
                    # Show final sample
                    if 'Set No.' in filtered_df.columns and 'Phase No.' in filtered_df.columns and 'Load Case Description' in filtered_df.columns:
                        sample_data = filtered_df[['Set No.', 'Phase No.', 'Load Case Description']].head(5)
                        print(f"DEBUG: Final sample of filtered data:\n{sample_data.to_string()}")
                else:
                    filtered_df = filtered_df.iloc[0:0]  # Empty dataframe
                    print(f"DEBUG: No matches found for any set+phase combinations")
        
        # Filter by selected load cases if provided
        if selected_load_cases and 'Load Case Description' in filtered_df.columns:
            print(f"DEBUG: Filtering by {len(selected_load_cases)} selected load cases: {selected_load_cases}")
            
            # Check which load cases actually exist in the current filtered data
            existing_load_cases = filtered_df['Load Case Description'].unique()
            print(f"DEBUG: Load cases in current filtered data: {sorted([str(x) for x in existing_load_cases])}")
            
            filtered_df = filtered_df[filtered_df['Load Case Description'].isin(selected_load_cases)]
            print(f"DEBUG: After load cases filter: {filtered_df.shape}")
        
        # Convert to list of dictionaries
        result_data = []
        for _, row in filtered_df.iterrows():
            row_data = {}
            for col in filtered_df.columns:
                if pd.notna(row[col]):
                    if pd.api.types.is_numeric_dtype(filtered_df[col]):
                        row_data[col] = float(row[col])
                    else:
                        row_data[col] = str(row[col])
                else:
                    row_data[col] = '' if pd.api.types.is_string_dtype(filtered_df[col]) else 0
            result_data.append(row_data)
        
        print(f"DEBUG: Final result data: {len(result_data)} records")
        return result_data
        
    except Exception as e:
        print(f"Error in apply_previous_selection_filter: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return []
    
    
def get_filtered_grouped_data(structure_id, filter_criteria, selected_load_cases, selection_source, selected_groups=None):  # NEW: Add selected_groups param
    """Get filtered data with grouping structure"""
    try:
        structure = ListOfStructure.objects.get(id=structure_id)
        
        print(f"DEBUG get_filtered_grouped_data: structure_id={structure_id}")
        print(f"DEBUG get_filtered_grouped_data: filter_criteria={filter_criteria}")
        print(f"DEBUG get_filtered_grouped_data: selected_load_cases={selected_load_cases}")
        print(f"DEBUG get_filtered_grouped_data: selection_source={selection_source}")
        print(f"DEBUG get_filtered_grouped_data: selected_groups={selected_groups}") 
        
        # Get the filtered data
        filtered_data = apply_previous_selection_filter(structure_id, filter_criteria, selected_load_cases)
        
        print(f"DEBUG get_filtered_grouped_data: filtered_data count = {len(filtered_data)}")
        
        if not filtered_data:
            return {'grouped_data': {}, 'all_columns': [], 'record_count': 0, 'is_grouped': True}
        
        # Convert back to DataFrame for grouping
        import pandas as pd
        df = pd.DataFrame(filtered_data)
        
        # Get all columns
        all_columns = list(df.columns) if not df.empty else []
        
        grouped_data = {}
        
        if selection_source == 'group':
            # Group by prefix for group load cases
            for record in filtered_data:
                if 'Load Case Description' in record:
                    case_name = record['Load Case Description']
                    if ' ' in case_name:
                        group_name = case_name.split(' ')[0]
                    else:
                        group_name = case_name
                    
                    if group_name not in grouped_data:
                        grouped_data[group_name] = []
                    grouped_data[group_name].append(record)
        
        elif selection_source == 'custom':
            # NEW: If no groups selected, return empty
            if not selected_groups:
                print("DEBUG: No custom groups selected, returning empty grouped data")
                return {'grouped_data': {}, 'all_columns': all_columns, 'record_count': 0, 'is_grouped': True}
            
            # Group by custom group names
            custom_groups = LoadCaseGroup.objects.filter(
                structure=structure, 
                is_custom=True
            ).prefetch_related('load_cases')
            
            for group in custom_groups:
                group_name = group.name
                # Only include if group is in selected_groups
                if group_name not in selected_groups:
                    continue
                
                group_cases = [case.name for case in group.load_cases.all()]
                grouped_data[group_name] = []
                
                # Find records that belong to this custom group
                for record in filtered_data:
                    if 'Load Case Description' in record and record['Load Case Description'] in group_cases:
                        grouped_data[group.name].append(record)
                
                # Remove empty groups
                if not grouped_data[group.name]:
                    del grouped_data[group.name]
        
        else:  # imported - use flat structure but still group by load case for consistency
            for record in filtered_data:
                if 'Load Case Description' in record:
                    case_name = record['Load Case Description']
                    if case_name not in grouped_data:
                        grouped_data[case_name] = []
                    grouped_data[case_name].append(record)
        
        # Calculate total record count
        total_records = sum(len(records) for records in grouped_data.values())
        
        print(f"DEBUG get_filtered_grouped_data: Final grouped data - {total_records} records in {len(grouped_data)} groups")
        
        return {
            'grouped_data': grouped_data,
            'all_columns': all_columns,
            'record_count': total_records,
            'is_grouped': True
        }
        
    except Exception as e:
        print(f"Error in get_filtered_grouped_data: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return {'grouped_data': {}, 'all_columns': [], 'record_count': 0, 'is_grouped': True}
    
def load_cases_page(request):
    """New dedicated page for Load Cases Selection and Load Values"""
    # Get selected values from session
    selected_values = request.session.get('selected_values', {})
    if isinstance(selected_values, list):
        print(f"⚠️ DEBUG load_cases_page: selected_values was a list, converting to dict")
        request.session['selected_values'] = {}
        selected_values = {}

    structure_id = selected_values.get('structure_id')
    selected_load_cases = selected_values.get('load_cases', [])
    
    # NEW: Get filter criteria from previous page
    filter_criteria = selected_values.get('filter_criteria', {})
    
    print(f"DEBUG load_cases_page: Session selected_values = {selected_values}")
    print(f"DEBUG: Filter criteria from session: {filter_criteria}")
    if 'set_phase_combinations' in filter_criteria:
        print(f"DEBUG: Number of combinations in filter_criteria: {len(filter_criteria['set_phase_combinations'])}")
        for i, combo in enumerate(filter_criteria['set_phase_combinations']):
            print(f"DEBUG: Combination {i}: Set={combo.get('set')}, Phase={combo.get('phase')}")
    
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
            print(f"DEBUG: Filtering by previous selection")
            print(f"DEBUG: Session selected_values: {request.session.get('selected_values', {})}")
            
            # Get filter criteria directly from session
            session_values = request.session.get('selected_values', {})
            # NEW: Add this type check/conversion here
            if isinstance(session_values, list):
                print(f"⚠️ DEBUG load_cases_page (filter_by_previous): session_values was a list, converting to dict")
                request.session['selected_values'] = {}
                session_values = {}
            
            filter_criteria = session_values.get('filter_criteria', {})
            selected_load_cases = session_values.get('load_cases', [])
            
            selected_groups = request.POST.getlist('selected_groups') or []
            
            print(f"DEBUG: Filter criteria from session: {filter_criteria}")
            print(f"DEBUG: Selected load cases from session: {selected_load_cases}")
            print(f"DEBUG: Selected groups: {selected_groups}")
            
            # NEW: Determine selection source from the request
            selection_source = request.POST.get('selection_source', 'imported')
            print(f"DEBUG: Selection source for filtering: {selection_source}")
            
            # Apply filter criteria with grouping
            filtered_result = get_filtered_grouped_data(
                structure_id, 
                filter_criteria, 
                selected_load_cases,
                selection_source,
                selected_groups
            )
            
            print(f"DEBUG: Filtered grouped data - {filtered_result['record_count']} records in {len(filtered_result['grouped_data'])} groups")
            
            return JsonResponse({
                'success': True, 
                'grouped_data': filtered_result['grouped_data'],
                'all_columns': filtered_result['all_columns'],
                'record_count': filtered_result['record_count'],
                'is_grouped': True,
                'current_selected_cases': selected_load_cases,
                'selection_source': selection_source,
                'filter_criteria': filter_criteria  # Return filter criteria for frontend display
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
    """Get filtered load data based on selected load cases with grouping support"""
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    structure_id = request.GET.get('structure_id')
    selected_load_cases = request.GET.getlist('selected_load_cases') or []
    selected_groups = request.GET.getlist('selected_groups') or []
    selection_source = request.GET.get('selection_source', 'imported')  # NEW: Get selection source
    
    if not structure_id:
        return JsonResponse({'error': 'Structure ID is required'}, status=400)
    
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

            # Filter by selected load cases if any are selected
            if selected_load_cases and 'Load Case Description' in df.columns:
                df = df[df['Load Case Description'].isin(selected_load_cases)]

            # NEW: Handle grouped response for group/custom selection sources
            if selection_source in ['group', 'custom'] and selected_load_cases:
                return get_grouped_response(df, selected_load_cases, selection_source, structure, selected_groups)
            
            # Existing flat list response for imported source
            load_data = []
            all_columns = []
            
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
                'record_count': len(load_data),
                'is_grouped': False  # NEW: Indicate this is flat data
            })
        else:
            return JsonResponse({'error': 'No file found for this structure'}, status=404)
            
    except ListOfStructure.DoesNotExist:
        return JsonResponse({'error': 'Structure not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# NEW: Function to create grouped response
def get_grouped_response(df, selected_load_cases, selection_source, structure, selected_groups=None):  # NEW: Add selected_groups param
    """Create grouped response for group/custom selection sources"""
    grouped_data = {}
    all_columns = list(df.columns)
    
    if selection_source == 'group':
        # Group by prefix for group load cases
        for case_name in selected_load_cases:
            if ' ' in case_name:
                group_name = case_name.split(' ')[0]
            else:
                group_name = case_name
                
            if group_name not in grouped_data:
                grouped_data[group_name] = []
            
            # Find matching rows for this load case
            case_rows = df[df['Load Case Description'] == case_name]
            for _, row in case_rows.iterrows():
                row_data = {}
                for col in df.columns:
                    if pd.notna(row[col]):
                        if pd.api.types.is_numeric_dtype(df[col]):
                            row_data[col] = float(row[col])
                        else:
                            row_data[col] = str(row[col])
                    else:
                        row_data[col] = '' if pd.api.types.is_string_dtype(df[col]) else 0
                grouped_data[group_name].append(row_data)
    
    elif selection_source == 'custom':
        # Group by custom group names
        custom_groups = LoadCaseGroup.objects.filter(
            structure=structure, 
            is_custom=True
        ).prefetch_related('load_cases')
        
        for group in custom_groups:
            group_name = group.name
            # NEW: Only include if group is in selected_groups
            if selected_groups and group_name not in selected_groups:
                continue
            
            group_cases = [case.name for case in group.load_cases.all()]
            # Check if any cases from this group are selected
            selected_group_cases = set(group_cases) & set(selected_load_cases)
            
            if selected_group_cases:
                grouped_data[group_name] = []
                for case_name in selected_group_cases:
                    # Find matching rows for this load case
                    case_rows = df[df['Load Case Description'] == case_name]
                    for _, row in case_rows.iterrows():
                        row_data = {}
                        for col in df.columns:
                            if pd.notna(row[col]):
                                if pd.api.types.is_numeric_dtype(df[col]):
                                    row_data[col] = float(row[col])
                                else:
                                    row_data[col] = str(row[col])
                            else:
                                row_data[col] = '' if pd.api.types.is_string_dtype(df[col]) else 0
                        grouped_data[group_name].append(row_data)
    
    # Calculate total record count
    total_records = sum(len(records) for records in grouped_data.values())
    
    return JsonResponse({
        'grouped_data': grouped_data,
        'all_columns': all_columns,
        'record_count': total_records,
        'is_grouped': True  # NEW: Indicate this is grouped data
    })
    
def get_all_load_cases(structure):
    """Get all available load cases from the database"""
    try:
        # Get all unique load case names from LoadCase model for this structure
        all_load_cases = LoadCase.objects.filter(
            structure=structure
        ).values_list('name', flat=True).distinct()
        
        return JsonResponse({'values': list(all_load_cases)})
        
    except Exception as e:
        return JsonResponse({'error': str(e)})

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
        
        elif request.method == 'POST' and 'edit_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            selected_cases = request.POST.getlist('selected_cases[]')
            
            if group_name and selected_cases is not None:
                try:
                    # Get the custom group
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=group_name,
                        is_custom=True
                    )
                    
                    # Clear existing load cases
                    group.load_cases.all().delete()
                    
                    # Add new load cases
                    for case_name in selected_cases:
                        LoadCase.objects.create(
                            name=case_name,
                            group=group,
                            structure=structure
                        )
                    
                    return JsonResponse({'success': True})
                    
                except LoadCaseGroup.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Group "{group_name}" not found'})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            
            return JsonResponse({'success': False, 'error': 'Group name and cases are required'})
        
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
                structure_id = request.GET.get('structure_id')
                print(f"DEBUG: Handling get_custom_groups_for_selection for structure_id: {structure_id}")  # NEW: Debug log
                if not structure_id:
                    return JsonResponse({'error': 'Structure ID is required'}, status=400)
                
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    return get_custom_groups(structure)
                except ListOfStructure.DoesNotExist:
                    print(f"DEBUG: Structure with ID {structure_id} not found")  # NEW: Debug log
                    return JsonResponse({'error': 'Structure not found'}, status=404)
            
            elif request.GET.get('get_all_load_cases'):
                return get_all_load_cases(structure)

    
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
    print(f"DEBUG: Getting custom groups for structure ID {structure.id} - Name: {structure.structure}")  # NEW: Debug log
    custom_groups = LoadCaseGroup.objects.filter(
        structure=structure, 
        is_custom=True
    ).prefetch_related('load_cases')
    
    print(f"DEBUG: Found {custom_groups.count()} custom groups for structure {structure.id}")  # NEW: Debug log
    groups_data = {}
    for group in custom_groups:
        groups_data[group.name] = [case.name for case in group.load_cases.all()]
        print(f"DEBUG: Group '{group.name}' has {len(groups_data[group.name])} load cases")  # NEW: Debug log
    
    print(f"DEBUG: Returning groups_data: {groups_data}")  # NEW: Debug log
    return JsonResponse({'custom_groups': groups_data})


import math
import json
from django.shortcuts import render


def calculation_view(request):
    # Initialize context with default values to avoid UnboundLocalError
    context = {'error': None}
    
    if request.method == 'POST':  # Handle POST requests
        # Get calculation data and selection source from POST parameters
        calculation_data_json = request.POST.get('calculation_data')
        selection_source = request.POST.get('selection_source', 'imported')
        custom_groups_json = request.POST.get('custom_groups_data', '{}')  # NEW: Get custom groups data
        
        print(f"DEBUG calculation_view: selection_source = {selection_source}")
        print(f"DEBUG calculation_view: custom_groups_json = {custom_groups_json}")
        
        if calculation_data_json:
            try:
                calculation_data = json.loads(calculation_data_json)
                custom_groups_data = json.loads(custom_groups_json)  # NEW: Parse custom groups
                
                print(f"DEBUG calculation_view: calculation_data count = {len(calculation_data)}")
                print(f"DEBUG calculation_view: custom_groups_data = {custom_groups_data}")
                
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
                    # Store Load Case Description for grouping
                    record['Load_Case_Description'] = record.get('Load Case Description', 'Unknown')
                
                # NEW: Group data based on selection source with custom groups support
                grouped_data = group_calculation_data(calculation_data, selection_source, custom_groups_data)
                print(f"DEBUG: Total groups after grouping: {len(grouped_data)}")
                for group_name, records in grouped_data.items():
                    print(f"DEBUG: Group '{group_name}': {len(records)} records")
                    
                    # Debug Set Nos. within this group
                    set_nos = set()
                    for record in records:
                        set_nos.add(record.get('Set_No', 'Unknown'))
                    print(f"DEBUG:   Set Nos. in '{group_name}': {set_nos}")

                # NEW: Create set-wise grouping within each group
                set_wise_data = {}
                set_max_resultants = {}
                
                
                for group_name, records in grouped_data.items():
                    
                    set_wise_data[group_name] = {}
                    set_max_resultants[group_name] = {}
                    
                    # Group records by Set No. within this group
                    for record in records:
                        set_no = record.get('Set_No', 'Unknown')
                        if set_no not in set_wise_data[group_name]:
                            set_wise_data[group_name][set_no] = []
                        set_wise_data[group_name][set_no].append(record)
                        
                    print(f"DEBUG: Group '{group_name}' has {len(set_wise_data[group_name])} unique Set Nos.")
                    
                    # Calculate max resultant for each set within this group
                    for set_no, set_records in set_wise_data[group_name].items():
                        resultant_values = [record['Resultant'] for record in set_records]
                        max_resultant = max(resultant_values)
                        max_index = resultant_values.index(max_resultant)
                        
                        set_max_resultants[group_name][set_no] = {
                            'vert': set_records[max_index]['Structure_Loads_Vert'],
                            'trans': set_records[max_index]['Structure_Loads_Trans'],
                            'long': set_records[max_index]['Structure_Loads_Long'],
                            'resultant': max_resultant,
                            'record_id': set_records[max_index]['record_id']
                        }
                        
                        # Add max resultant flag to set records
                        for i, record in enumerate(set_records):
                            if resultant_values[i] == max_resultant:
                                record['set_max_resultant_flag'] = 'yes'
                            else:
                                record['set_max_resultant_flag'] = 'no'
                    print(f"DEBUG: Group '{group_name}' set max resultants: {list(set_max_resultants[group_name].keys())}")
                
                # NEW: Calculate group-wise sums for set max resultants
                group_wise_set_max_sums = {}
                for group_name, set_data in set_max_resultants.items():
                    group_vert = sum([data['vert'] for data in set_data.values()])
                    group_trans = sum([data['trans'] for data in set_data.values()])
                    group_long = sum([data['long'] for data in set_data.values()])
                    group_resultant = math.sqrt(group_vert**2 + group_trans**2 + group_long**2)
                    
                    group_wise_set_max_sums[group_name] = {
                        'vert': group_vert,
                        'trans': group_trans,
                        'long': group_long,
                        'resultant': group_resultant,
                        'set_count': len(set_data)
                    }
                    
                request.session['group_wise_set_max_sums'] = group_wise_set_max_sums
                
                # Calculate max values for each group and flag max resultant rows
                group_max_values = {}
                max_resultant_values = {}  # Store the actual values that created the max resultant
                max_resultant_indexes = {}  # Store indexes for JavaScript approach
                
                for group_name, records in grouped_data.items():
                    vert_values = [float(record.get('Structure Loads Vert. (lbs)', 0) or 0) for record in records]
                    trans_values = [float(record.get('Structure Loads Trans. (lbs)', 0) or 0) for record in records]
                    long_values = [float(record.get('Structure Loads Long. (lbs)', 0) or 0) for record in records]
                    resultant_values = [record['Resultant'] for record in records]
                    
                    # Find the maximum resultant value
                    max_resultant = max(resultant_values)
                    max_index = resultant_values.index(max_resultant)
                    
                    # Store the actual values that created the max resultant
                    max_resultant_values[group_name] = {
                        'vert': vert_values[max_index],
                        'trans': trans_values[max_index],
                        'long': long_values[max_index],
                        'resultant': max_resultant,
                        'record_id': records[max_index]['record_id']  # Add record ID
                    }
                    
                    # Store index for JavaScript approach
                    max_resultant_indexes[group_name] = max_index
                    
                    # Add a simple flag to each record (as a string to avoid underscore issues)
                    for i, record in enumerate(records):
                        if resultant_values[i] == max_resultant:
                            record['max_resultant_flag'] = 'yes'
                        else:
                            record['max_resultant_flag'] = 'no'
                    
                    group_max_values[group_name] = {
                        'max_vert': max(vert_values),
                        'max_trans': max(trans_values),
                        'max_long': max(long_values),
                        'max_resultant': max_resultant,
                        'count': len(records)
                    }
                
                # Calculate combined values across all groups using the actual values that created max resultants
                combined_vert = sum([values['vert'] for values in max_resultant_values.values()])
                combined_trans = sum([values['trans'] for values in max_resultant_values.values()])
                combined_long = sum([values['long'] for values in max_resultant_values.values()])
                
                # Calculate the SQRT formula for combined values
                combined_sqrt = math.sqrt(combined_vert**2 + combined_trans**2 + combined_long**2)
                
                # Prepare context for template
                context = {
                    'grouped_data': grouped_data,
                    'group_max_values': group_max_values,
                    'max_resultant_values': max_resultant_values,
                    'set_wise_data': set_wise_data,  # NEW: Set-wise grouped data
                    'set_max_resultants': set_max_resultants,  # NEW: Set max resultants
                    'group_wise_set_max_sums': group_wise_set_max_sums,  # NEW: Group-wise sums
                    'combined_vert': combined_vert,
                    'combined_trans': combined_trans,
                    'combined_long': combined_long,
                    'combined_sqrt': combined_sqrt,
                    'calculation_data': calculation_data,
                    'max_resultant_indexes': max_resultant_indexes,
                    'calculation_data_json': json.dumps(calculation_data),
                    'selection_source': selection_source,
                    'custom_groups_data': custom_groups_data,  # NEW: Pass to template for reference
                    'error': None
                }
                
            except json.JSONDecodeError:
                context['error'] = 'Invalid calculation data format'
            except Exception as e:
                context['error'] = f'Error processing data: {str(e)}'
        else:
            context['error'] = 'No calculation data provided'
    
    # Handle GET requests
    elif request.method == 'GET':
        calculation_data_json = request.GET.get('calculation_data')
        selection_source = request.GET.get('selection_source', 'imported')
        custom_groups_json = request.GET.get('custom_groups_data', '{}')  # NEW: Get custom groups data
        
        if calculation_data_json:
            try:
                calculation_data = json.loads(calculation_data_json)
                custom_groups_data = json.loads(custom_groups_json)  # NEW: Parse custom groups
                
                # Add resultant calculation and unique ID to each record
                for index, record in enumerate(calculation_data):
                    vert = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
                    trans = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
                    long = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
                    
                    resultant = math.sqrt(vert**2 + trans**2 + long**2)
                    record['Resultant'] = round(resultant, 2)
                    record['record_id'] = f"record_{index}"
                    record['Structure_Loads_Vert'] = vert
                    record['Structure_Loads_Trans'] = trans
                    record['Structure_Loads_Long'] = long
                    record['Set_No'] = record.get('Set No.', 'Unknown')
                    record['Load_Case_Description'] = record.get('Load Case Description', 'Unknown')
                
                # NEW: Group data based on selection source with custom groups support
                grouped_data = group_calculation_data(calculation_data, selection_source, custom_groups_data)
                print(f"DEBUG: Total groups after grouping: {len(grouped_data)}")
                for group_name, records in grouped_data.items():
                    print(f"DEBUG: Group '{group_name}': {len(records)} records")
                    
                    # Debug Set Nos. within this group
                    set_nos = set()
                    for record in records:
                        set_nos.add(record.get('Set_No', 'Unknown'))
                    print(f"DEBUG:   Set Nos. in '{group_name}': {set_nos}")
                # NEW: Create set-wise grouping within each group for GET requests
                set_wise_data = {}
                set_max_resultants = {}
                
                for group_name, records in grouped_data.items():
                    set_wise_data[group_name] = {}
                    set_max_resultants[group_name] = {}
                    
                    # Group records by Set No. within this group
                    for record in records:
                        set_no = record.get('Set_No', 'Unknown')
                        if set_no not in set_wise_data[group_name]:
                            set_wise_data[group_name][set_no] = []
                        set_wise_data[group_name][set_no].append(record)
                    print(f"DEBUG: Group '{group_name}' has {len(set_wise_data[group_name])} unique Set Nos.")
                    
                    # Calculate max resultant for each set within this group
                    for set_no, set_records in set_wise_data[group_name].items():
                        resultant_values = [record['Resultant'] for record in set_records]
                        max_resultant = max(resultant_values)
                        max_index = resultant_values.index(max_resultant)
                        
                        set_max_resultants[group_name][set_no] = {
                            'vert': set_records[max_index]['Structure_Loads_Vert'],
                            'trans': set_records[max_index]['Structure_Loads_Trans'],
                            'long': set_records[max_index]['Structure_Loads_Long'],
                            'resultant': max_resultant,
                            'record_id': set_records[max_index]['record_id']
                        }
                        
                        # Add max resultant flag to set records
                        for i, record in enumerate(set_records):
                            if resultant_values[i] == max_resultant:
                                record['set_max_resultant_flag'] = 'yes'
                            else:
                                record['set_max_resultant_flag'] = 'no'
                    print(f"DEBUG: Group '{group_name}' set max resultants: {list(set_max_resultants[group_name].keys())}")
                
                # NEW: Calculate group-wise sums for set max resultants for GET requests
                group_wise_set_max_sums = {}
                for group_name, set_data in set_max_resultants.items():
                    group_vert = sum([data['vert'] for data in set_data.values()])
                    group_trans = sum([data['trans'] for data in set_data.values()])
                    group_long = sum([data['long'] for data in set_data.values()])
                    group_resultant = math.sqrt(group_vert**2 + group_trans**2 + group_long**2)
                    
                    group_wise_set_max_sums[group_name] = {
                        'vert': group_vert,
                        'trans': group_trans,
                        'long': group_long,
                        'resultant': group_resultant,
                        'set_count': len(set_data)
                    }
                
                # Calculate max values
                group_max_values = {}
                max_resultant_values = {}
                max_resultant_indexes = {}
                
                for group_name, records in grouped_data.items():
                    vert_values = [float(record.get('Structure Loads Vert. (lbs)', 0) or 0) for record in records]
                    trans_values = [float(record.get('Structure Loads Trans. (lbs)', 0) or 0) for record in records]
                    long_values = [float(record.get('Structure Loads Long. (lbs)', 0) or 0) for record in records]
                    resultant_values = [record['Resultant'] for record in records]
                    
                    max_resultant = max(resultant_values)
                    max_index = resultant_values.index(max_resultant)
                    
                    max_resultant_values[group_name] = {
                        'vert': vert_values[max_index],
                        'trans': trans_values[max_index],
                        'long': long_values[max_index],
                        'resultant': max_resultant,
                        'record_id': records[max_index]['record_id']
                    }
                    
                    max_resultant_indexes[group_name] = max_index
                    
                    for i, record in enumerate(records):
                        if resultant_values[i] == max_resultant:
                            record['max_resultant_flag'] = 'yes'
                        else:
                            record['max_resultant_flag'] = 'no'
                    
                    group_max_values[group_name] = {
                        'max_vert': max(vert_values),
                        'max_trans': max(trans_values),
                        'max_long': max(long_values),
                        'max_resultant': max_resultant,
                        'count': len(records)
                    }
                request.session['group_wise_set_max_sums'] = group_wise_set_max_sums
                    
                # Calculate combined values
                combined_vert = sum([values['vert'] for values in max_resultant_values.values()])
                combined_trans = sum([values['trans'] for values in max_resultant_values.values()])
                combined_long = sum([values['long'] for values in max_resultant_values.values()])
                combined_sqrt = math.sqrt(combined_vert**2 + combined_trans**2 + combined_long**2)
                
                context = {
                    'grouped_data': grouped_data,
                    'group_max_values': group_max_values,
                    'max_resultant_values': max_resultant_values,
                    'set_wise_data': set_wise_data,  # NEW: Set-wise grouped data
                    'set_max_resultants': set_max_resultants,  # NEW: Set max resultants
                    'group_wise_set_max_sums': group_wise_set_max_sums,  # NEW: Group-wise sums for GET
                    'combined_vert': combined_vert,
                    'combined_trans': combined_trans,
                    'combined_long': combined_long,
                    'combined_sqrt': combined_sqrt,
                    'calculation_data': calculation_data,
                    'max_resultant_indexes': max_resultant_indexes,
                    'calculation_data_json': json.dumps(calculation_data),
                    'selection_source': selection_source,
                    'custom_groups_data': custom_groups_data,  # NEW: Pass to template
                    'error': None
                }
                
            except json.JSONDecodeError:
                context['error'] = 'Invalid calculation data format'
            except Exception as e:
                context['error'] = f'Error processing data: {str(e)}'
        else:
            context['error'] = 'No calculation data provided'
    else:
        context['error'] = 'Invalid request method'
    
    return render(request, 'app1/calculation.html', context)

# In views.py, add this to your context or create a custom filter
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def items(dictionary):
    return dictionary.items()

def group_calculation_data(calculation_data, selection_source, custom_groups_data=None):
    """Group calculation data based on selection source with custom groups support"""
    grouped_data = {}
    
    if selection_source == 'imported':
        # Group by Load Case Description (individual load cases)
        for record in calculation_data:
            case_name = record.get('Load Case Description', 'Unknown')
            if case_name not in grouped_data:
                grouped_data[case_name] = []
            grouped_data[case_name].append(record)
    
    elif selection_source == 'group':
        # Group by prefix for group load cases (first word before space)
        for record in calculation_data:
            case_name = record.get('Load Case Description', 'Unknown')
            if ' ' in case_name:
                group_name = case_name.split(' ')[0]
            else:
                group_name = case_name
            
            if group_name not in grouped_data:
                grouped_data[group_name] = []
            grouped_data[group_name].append(record)
    
    elif selection_source == 'custom' and custom_groups_data:
        # FIX: Improved custom groups handling to preserve all groups
        print(f"DEBUG: Processing custom groups: {custom_groups_data}")
        
        # Initialize ALL custom groups first to ensure they appear
        for group_name, load_cases in custom_groups_data.items():
            grouped_data[group_name] = []  # Create group even if empty initially
        
        # Now populate with matching records
        for record in calculation_data:
            case_name = record.get('Load Case Description', '')
            for group_name, load_cases in custom_groups_data.items():
                if case_name in load_cases:
                    grouped_data[group_name].append(record)
        
        # DEBUG: Log group counts
        for group_name, records in grouped_data.items():
            print(f"DEBUG: Group '{group_name}': {len(records)} records")
    
    else:  # Default fallback - group by Set No.
        for record in calculation_data:
            set_no = record.get('Set No.', 'Unknown')
            if set_no not in grouped_data:
                grouped_data[set_no] = []
            grouped_data[set_no].append(record)
    
    return grouped_data

# NEW: Optional helper function to extract custom groups from data
def extract_custom_groups_from_data(calculation_data):
    """
    Try to extract custom group information from the calculation data.
    This is a simplified implementation - in practice, you might want to pass
    this information explicitly from the Load Cases page.
    """
    custom_groups = {}
    
    # Look for patterns that might indicate custom groups
    # This is a heuristic approach - adjust based on your data structure
    for record in calculation_data:
        case_name = record.get('Load Case Description', '')
        # If the case name contains specific patterns, you could group them
        # For now, return empty to fall back to Set No. grouping
        pass
    
    return custom_groups if custom_groups else None

# views.py
import math
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LoadCondition, AttachmentLoad

def load_condition_view(request):
    calculation_data = []
    processed_sums = {}
    group_wise_buffered_sums = {}
    
    # Initialize selected_conditions as empty dict
    selected_conditions = {}
    
    # Try to get calculation data from multiple sources
    if request.method == 'POST':
        calculation_data_json = request.POST.get('calculation_data')
        processed_sums_json = request.POST.get('processed_sums')
        group_wise_buffered_sums_json = request.POST.get('group_wise_buffered_sums')
        
        if calculation_data_json:
            try:
                calculation_data = json.loads(calculation_data_json)
                request.session['calculation_data'] = calculation_data
                
                if processed_sums_json:
                    processed_sums = json.loads(processed_sums_json)
                    request.session['processed_sums'] = processed_sums
                
                # Handle group-wise buffered sums
                if group_wise_buffered_sums_json:
                    group_wise_buffered_sums = json.loads(group_wise_buffered_sums_json)
                    request.session['group_wise_buffered_sums'] = group_wise_buffered_sums
                    
            except json.JSONDecodeError:
                calculation_data = request.session.get('calculation_data', [])
                processed_sums = request.session.get('processed_sums', {})
                group_wise_buffered_sums = request.session.get('group_wise_buffered_sums', {})
    else:
        calculation_data = request.session.get('calculation_data', [])
        processed_sums = request.session.get('processed_sums', {})
        group_wise_buffered_sums = request.session.get('group_wise_buffered_sums', {})
    
    # Get selected conditions from session with proper initialization
    selected_conditions = request.session.get('selected_conditions', {})
    if selected_conditions is None:
        selected_conditions = {}
    
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
    
    # Process calculation data only if it exists
    if calculation_data:
        # Add record_id and clean keys to calculation data for template access
        for index, record in enumerate(calculation_data):
            record['record_id'] = f"record_{index}"
            record['Structure_Loads_Vert'] = float(record.get('Structure Loads Vert. (lbs)', 0) or 0)
            record['Structure_Loads_Trans'] = float(record.get('Structure Loads Trans. (lbs)', 0) or 0)
            record['Structure_Loads_Long'] = float(record.get('Structure Loads Long. (lbs)', 0) or 0)
            record['Resultant'] = float(record.get('Resultant (lbs)', 0) or 0)
            record['Set_No'] = record.get('Set No.', 'Unknown')
        
        factored_loads_by_condition = {}
        group_wise_factored_loads = {}

        # PRIORITY 1: Use group-wise buffered sums if available (Select Set Max Resultant Within Groups)
        if group_wise_buffered_sums:
            # Process EACH group separately
            for group_name, group_data in group_wise_buffered_sums.items():
                group_factored_loads = {}
                
                # Get selected conditions for this group (if any)
                # Handle None case and empty dict
                group_selections = {}
                if selected_conditions and isinstance(selected_conditions, dict):
                    group_selections = selected_conditions.get(group_name, {})
                
                # If no specific selections for this group, use all conditions
                if not group_selections:
                    conditions_to_process = load_conditions
                else:
                    # Filter to only selected conditions
                    conditions_to_process = []
                    for condition in load_conditions:
                        # Try both string and integer keys
                        condition_id_str = str(condition.id)
                        is_selected = False
                        
                        # Check if condition is in selections
                        if condition_id_str in group_selections:
                            is_selected = bool(group_selections[condition_id_str])
                        elif condition.id in group_selections:
                            is_selected = bool(group_selections[condition.id])
                        
                        if is_selected:
                            conditions_to_process.append(condition)
                
                # If no conditions selected after filtering, skip this group
                if not conditions_to_process:
                    continue
                
                for condition in conditions_to_process:
                    from decimal import Decimal
                    
                    # Use group-wise buffered sums as base loads
                    base_vert = Decimal(str(group_data.get('vert', 0)))
                    base_trans = Decimal(str(group_data.get('trans', 0)))
                    base_long = Decimal(str(group_data.get('long', 0)))
                    
                    # Apply overload factors
                    factored_vert = base_vert * Decimal(str(condition.vertical_factor))
                    factored_trans = base_trans * Decimal(str(condition.transverse_factor))
                    factored_long = base_long * Decimal(str(condition.longitudinal_factor))
                    
                    factored_vert = float(factored_vert)
                    factored_trans = float(factored_trans)
                    factored_long = float(factored_long)
                    
                    factored_resultant = math.sqrt(factored_vert**2 + factored_trans**2 + factored_long**2)

                    group_factored_loads[condition.description] = {
                        'base_loads': {
                            'vert': float(base_vert),
                            'trans': float(base_trans),
                            'long': float(base_long),
                            'resultant': group_data.get('resultant', 0)
                        },
                        'factored_loads': {
                            'vert': factored_vert,
                            'trans': factored_trans,
                            'long': factored_long,
                            'resultant': factored_resultant
                        },
                        'factors': {
                            'vertical': condition.vertical_factor,
                            'transverse': condition.transverse_factor,
                            'longitudinal': condition.longitudinal_factor
                        },
                        'calculation_type': 'group_wise_buffered',
                        'group_name': group_name
                    }
                
                # Store factored loads for this group only if we have results
                if group_factored_loads:
                    group_wise_factored_loads[group_name] = group_factored_loads

        # PRIORITY 2: Use processed sums if available
        elif processed_sums and processed_sums.get('totalVert') is not None:  
            for condition in load_conditions:
                from decimal import Decimal
                
                base_vert = Decimal(str(processed_sums.get('totalVert', 0)))
                base_trans = Decimal(str(processed_sums.get('totalTrans', 0)))
                base_long = Decimal(str(processed_sums.get('totalLong', 0)))
                
                factored_vert = base_vert * Decimal(str(condition.vertical_factor))
                factored_trans = base_trans * Decimal(str(condition.transverse_factor))
                factored_long = base_long * Decimal(str(condition.longitudinal_factor))
                
                factored_vert = float(factored_vert)
                factored_trans = float(factored_trans)
                factored_long = float(factored_long)
                
                factored_resultant = math.sqrt(factored_vert**2 + factored_trans**2 + factored_long**2)

                factored_loads_by_condition[condition.description] = {
                    'base_loads': {
                        'vert': float(base_vert),
                        'trans': float(base_trans),
                        'long': float(base_long),
                        'resultant': processed_sums.get('finalResultant', 0)
                    },
                    'factored_loads': {
                        'vert': factored_vert,
                        'trans': factored_trans,
                        'long': factored_long,
                        'resultant': factored_resultant
                    },
                    'factors': {
                        'vertical': condition.vertical_factor,
                        'transverse': condition.transverse_factor,
                        'longitudinal': condition.longitudinal_factor
                    },
                    'calculation_type': 'processed_sums',
                }
        
        # PRIORITY 3: Fallback to individual records
        elif calculation_data:
            for condition in load_conditions:
                factored_loads_by_condition[condition.description] = {
                    'factors': {
                        'vertical': condition.vertical_factor,
                        'transverse': condition.transverse_factor,
                        'longitudinal': condition.longitudinal_factor
                    },
                    'calculation_type': 'individual_records'
                }
    
    # Prepare template data for checkboxes
    # Create a list of conditions with selection info for each group
    condition_selection_data = {}
    if group_wise_buffered_sums:
        for group_name in group_wise_buffered_sums.keys():
            group_selections = selected_conditions.get(group_name, {}) if selected_conditions else {}
            
            # Create a dictionary with condition_id as key for easy template access
            group_condition_data = {}
            for condition in load_conditions:
                condition_id_str = str(condition.id)
                is_selected = (
                    group_selections.get(condition_id_str, False) or 
                    group_selections.get(condition.id, False)
                )
                
                group_condition_data[condition.id] = {
                    'id': condition.id,
                    'description': condition.description,
                    'vertical_factor': condition.vertical_factor,
                    'transverse_factor': condition.transverse_factor,
                    'longitudinal_factor': condition.longitudinal_factor,
                    'is_selected': is_selected
                }
            
            condition_selection_data[group_name] = group_condition_data
    
    context = {
        'load_conditions': load_conditions,
        'attachment_loads': attachment_loads,
        'calculation_data': calculation_data,
        'calculation_data_json': json.dumps(calculation_data),
        'factored_loads_by_condition': factored_loads_by_condition,
        'group_wise_factored_loads': group_wise_factored_loads,
        'has_factored_loads': bool(factored_loads_by_condition) or bool(group_wise_factored_loads),
        'processed_sums': processed_sums,
        'using_processed_sums': bool(processed_sums),
        'group_wise_buffered_sums': group_wise_buffered_sums,
        'using_group_wise_sums': bool(group_wise_buffered_sums),
        'has_group_wise_factored_loads': bool(group_wise_factored_loads),
        'selected_conditions': selected_conditions,
        'condition_selection_data': condition_selection_data,  # New: Pre-processed selection data
    }
    
    return render(request, 'app1/load_condition.html', context)

from django.http import JsonResponse
import json

def get_current_selections(request):
    """Return current selections from session"""
    selected_conditions = request.session.get('selected_conditions', {})
    return JsonResponse(selected_conditions)

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def save_condition_selections(request):
    """Save user's condition selections"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group_name = data.get('group_name')
            selections = data.get('selections', {})
            
            logger.info(f"Received selections for group {group_name}: {selections}")
            
            # Get current selections from session
            selected_conditions = request.session.get('selected_conditions', {})
            if selected_conditions is None:
                selected_conditions = {}
            
            # Update selections for this group
            selected_conditions[group_name] = selections
            
            # Save to session
            request.session['selected_conditions'] = selected_conditions
            request.session.modified = True
            
            logger.info(f"Saved selections to session: {selected_conditions}")
            
            return JsonResponse({
                'success': True,
                'message': f'Selections saved for {group_name}',
                'selections_saved': selections
            })
        except Exception as e:
            logger.error(f"Error saving selections: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import LoadCondition
from .forms import LoadConditionForm

def create_load_condition(request):
    if request.method == 'POST':
        form = LoadConditionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Load condition created successfully!')
            # Preserve the calculation data in session
            if 'calculation_data' in request.session:
                # Keep the session data intact
                pass
            return redirect('load_condition')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = LoadConditionForm()
    
    return render(request, 'app1/load_condition_form.html', {'form': form})

def edit_load_condition(request, pk):
    load_condition = get_object_or_404(LoadCondition, pk=pk)
    
    if request.method == 'POST':
        form = LoadConditionForm(request.POST, instance=load_condition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Load condition updated successfully!')
            # Preserve the calculation data in session
            if 'calculation_data' in request.session:
                # Keep the session data intact
                pass
            return redirect('load_condition')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = LoadConditionForm(instance=load_condition)
    
    return render(request, 'app1/load_condition_form.html', {
        'form': form,
        'load_condition': load_condition,
        'editing': True
    })

def delete_load_condition(request, pk):
    load_condition = get_object_or_404(LoadCondition, pk=pk)
    
    if request.method == 'POST':
        load_condition.delete()
        messages.success(request, 'Load condition deleted successfully!')
        # Preserve the calculation data in session
        if 'calculation_data' in request.session:
            # Keep the session data intact
            pass
        return redirect('load_condition')
    
    # For GET requests, show confirmation
    return render(request, 'app1/confirm_delete.html', {
        'load_condition': load_condition
    })
    

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
    
    # Debug: Print current session data
    session_data = dict(request.session.items())
    print(f"DEBUG - Current session data: {session_data}")
    
    # Get session data to pass to template
    context = {
        'structures': structures,
        'groups': groups,
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_structure_id': request.session.get('selected_structure_id', ''),
        'session_popups': request.session.get('active_popups', []),
        'session_popup_selections': request.session.get('popup_selections', {}),
    }
    
    return render(request, 'app1/home.html', context)

def store_structure_selection(request):
    if request.method == 'POST':
        structure_type = request.POST.get('structure_type')
        structure_id = request.POST.get('structure_id')
        
        # Clear previous popup selections when starting a new structure type
        request.session['active_popups'] = []  # Reset the popup list
        request.session['popup_selections'] = {}  # Reset structured selections
        
        # Store in session
        request.session['selected_structure_type'] = structure_type
        request.session['selected_structure_id'] = structure_id
        
        # Debug print
        print(f"DEBUG - Stored in session: structure_type={structure_type}, structure_id={structure_id}")
        print(f"DEBUG - Session ID: {request.session.session_key}")
        print(f"DEBUG - Active popups cleared for new selection")
        print(f"DEBUG - Popup selections cleared for new selection")
        
        # Save session explicitly
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success', 
            'structure_type': structure_type,
            'structure_id': structure_id
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def store_popup_selection(request):
    if request.method == 'POST':
        popup_type = request.POST.get('popup_type')
        selection_value = request.POST.get('selection_value')
        structure_type = request.POST.get('structure_type')
        structure_id = request.POST.get('structure_id')
        
        # Debug: Print all received data
        print(f"DEBUG [store_popup_selection] - Received:")
        print(f"  popup_type: '{popup_type}'")
        print(f"  selection_value: '{selection_value}'")
        print(f"  structure_type: '{structure_type}'")
        print(f"  structure_id: '{structure_id}'")
        
        # Ensure active_popups exists in session
        if 'active_popups' not in request.session:
            request.session['active_popups'] = []
        
        # Store structure type if not already stored
        if structure_type and 'selected_structure_type' not in request.session:
            request.session['selected_structure_type'] = structure_type
        
        # Store structure ID if not already stored
        if structure_id and 'selected_structure_id' not in request.session:
            request.session['selected_structure_id'] = structure_id
        
        # Store the specific popup type and value
        if popup_type and selection_value:
            # Create a key for this specific selection
            selection_key = f"{popup_type}_{selection_value}"
            
            # Add to active popups if not already present
            if selection_key not in request.session['active_popups']:
                request.session['active_popups'].append(selection_key)
                print(f"DEBUG [store_popup_selection] - Added to active_popups: '{selection_key}'")
            else:
                print(f"DEBUG [store_popup_selection] - Already in active_popups: '{selection_key}'")
            
            # Also store in a structured way
            if 'popup_selections' not in request.session:
                request.session['popup_selections'] = {}
            
            # Check if we're overwriting an existing value
            if popup_type in request.session['popup_selections']:
                old_value = request.session['popup_selections'][popup_type]
                print(f"DEBUG [store_popup_selection] - Overwriting {popup_type}: '{old_value}' -> '{selection_value}'")
            
            request.session['popup_selections'][popup_type] = selection_value
            print(f"DEBUG [store_popup_selection] - Updated popup_selections[{popup_type}] = '{selection_value}'")
        else:
            print(f"DEBUG [store_popup_selection] - WARNING: Missing popup_type or selection_value!")
            print(f"  popup_type: {popup_type}")
            print(f"  selection_value: {selection_value}")
        
        # Debug print current state
        print(f"DEBUG [store_popup_selection] - Current state:")
        print(f"  active_popups: {request.session.get('active_popups', [])}")
        print(f"  popup_selections: {request.session.get('popup_selections', {})}")
        print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
        print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
        
        # Save session
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success', 
            'popup_type': popup_type,
            'selection_value': selection_value,
            'active_popups': request.session['active_popups'],
            'popup_selections': request.session.get('popup_selections', {})
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def clear_session_data(request):
    """Clear session data for debugging or starting fresh"""
    if 'active_popups' in request.session:
        del request.session['active_popups']
    if 'selected_structure_type' in request.session:
        del request.session['selected_structure_type']
    if 'selected_structure_id' in request.session:
        del request.session['selected_structure_id']
    
    request.session.modified = True
    return JsonResponse({'status': 'success', 'message': 'Session data cleared'})

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
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug logging
    print(f"DEBUG [tupload1] - Received structure_id: {structure_id}")
    print(f"DEBUG [tupload1] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload1] - circuit_id is invalid string: '{circuit_id}', setting to None")
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload1] - No circuit_id in URL, checking session")
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload1] - Got circuit_id from session circuit_definition: {circuit_id}")
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload1] - Got circuit_id from circuit_structure_id: {circuit_id}")
                
                # Check if there's any TowerDeadend data for this structure
                if not circuit_id:
                    circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                    if circuit_exists:
                        circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload1] - Found circuit data by structure lookup: {circuit_id}")
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload1] - Converted circuit_id to int: {circuit_id}")
                    else:
                        print(f"DEBUG [tupload1] - circuit_id is string but not digit: '{circuit_id}', setting to None")
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TowerDeadend.objects.get(id=circuit_id, structure=structure)
                        circuit_data_exists = True
                        print(f"DEBUG [tupload1] - Found circuit data by circuit_id: {circuit_id}")
                    except TowerDeadend.DoesNotExist:    # **********
                        print(f"DEBUG [tupload1] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")
                        # Fall back to structure lookup
                        circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                        if circuit_exists:
                            circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload1] - Found circuit data by structure: {circuit_id}")
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload1] - No circuit data found for structure")
                    except ValueError as e:
                        print(f"DEBUG [tupload1] - ValueError with circuit_id {circuit_id}: {e}")
                        # Try structure lookup as fallback
                        circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                        if circuit_exists:
                            circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload1] - Fallback: Found circuit data by structure: {circuit_id}")
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                if circuit_exists:
                    circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload1] - No circuit_id provided, found by structure: {circuit_id}")
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload1] - No circuit_id and no circuit data found for structure")
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload1] - No circuit data found, redirecting to tdeadend")
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend/?structure_id={structure_id}&structure_type={structure_type}'
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TowerDeadend',
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload1] - Updated session with circuit_id: {circuit_data.id}")
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile1.objects.filter(structure=structure).exists()
            
            if existing_file_check:
                return render(request, 'app1/tupload1.html', {
                    'form': tUploadedFileForm1(),
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files1__isnull=False).distinct(),
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = tUploadedFileForm1(request.POST, request.FILES)
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases1(instance)
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload1/?structure_id={structure_id}&structure_type={structure_type}'
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile1.objects.filter(structure=structure).exists()
        form = tUploadedFileForm1()      # **********
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files1__isnull=False).distinct()

    # Handle AJAX requests for data (GET requests only)
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload1.html', {
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug logging
    print(f"DEBUG [tupload2] - Received structure_id: {structure_id}")
    print(f"DEBUG [tupload2] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload2] - circuit_id is invalid string: '{circuit_id}', setting to None")
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload2] - No circuit_id in URL, checking session")
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload2] - Got circuit_id from session circuit_definition: {circuit_id}")
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload2] - Got circuit_id from circuit_structure_id: {circuit_id}")
                
                # Check if there's any TowerDeadend data for this structure
                if not circuit_id:
                    circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                    if circuit_exists:
                        circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload2] - Found circuit data by structure lookup: {circuit_id}")
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload2] - Converted circuit_id to int: {circuit_id}")
                    else:
                        print(f"DEBUG [tupload2] - circuit_id is string but not digit: '{circuit_id}', setting to None")
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TowerDeadend.objects.get(id=circuit_id, structure=structure)
                        circuit_data_exists = True
                        print(f"DEBUG [tupload2] - Found circuit data by circuit_id: {circuit_id}")
                    except TowerDeadend.DoesNotExist:    # **********
                        print(f"DEBUG [tupload2] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")
                        # Fall back to structure lookup
                        circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                        if circuit_exists:
                            circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload2] - Found circuit data by structure: {circuit_id}")
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload2] - No circuit data found for structure")
                    except ValueError as e:
                        print(f"DEBUG [tupload2] - ValueError with circuit_id {circuit_id}: {e}")
                        # Try structure lookup as fallback
                        circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                        if circuit_exists:
                            circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload2] - Fallback: Found circuit data by structure: {circuit_id}")
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TowerDeadend.objects.filter(structure=structure).exists()
                if circuit_exists:
                    circuit_data = TowerDeadend.objects.filter(structure=structure).latest('id')
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload2] - No circuit_id provided, found by structure: {circuit_id}")
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload2] - No circuit_id and no circuit data found for structure")
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload2] - No circuit data found, redirecting to tdeadend")
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend/?structure_id={structure_id}&structure_type={structure_type}'
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TowerDeadend',
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload2] - Updated session with circuit_id: {circuit_data.id}")
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile2.objects.filter(structure=structure).exists()
            
            if existing_file_check:
                return render(request, 'app1/tupload2.html', {
                    'form': tUploadedFileForm2(),
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files2__isnull=False).distinct(),
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = tUploadedFileForm2(request.POST, request.FILES)
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases3(instance)
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload2/?structure_id={structure_id}&structure_type={structure_type}'
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile2.objects.filter(structure=structure).exists()
        form = tUploadedFileForm2()     # *************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files2__isnull=False).distinct()

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload2.html', {
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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

def tdeadend3(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TowerDeadend3 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TowerDeadend3.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TowerDeadend3.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TowerDeadend3 data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TowerDeadend3.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TowerDeadend3 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload3/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend3.html', {   # *************
                'form': TowerDeadendForm3(instance=existing_circuit_data),   # **************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TowerDeadendForm3(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'HDeadend2',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TowerDeadend3] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload3/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TowerDeadend3 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TowerDeadendForm3(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TowerDeadend3',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TowerDeadendForm3()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TowerDeadend3 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend3.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tdeadend3_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TowerDeadend3, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend3FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload3/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend3FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend3_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })


def tdeadend4(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TowerDeadend4 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TowerDeadend4.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TowerDeadend4.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TowerDeadend4 data for structure ID: {structure_id}")   # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TowerDeadend4.DoesNotExist:       # **************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TowerDeadend4 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload4/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend4.html', {   # *************
                'form': TowerDeadendForm4(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TowerDeadendForm4(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TowerDeadend4',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TowerDeadend4] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload4/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TowerDeadend4 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TowerDeadendForm4(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TowerDeadend4',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TowerDeadendForm4()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TowerDeadend4 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend4.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tdeadend4_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TowerDeadend4, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend4FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload4/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend4FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend4_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tdeadend5(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TowerDeadend5 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TowerDeadend5.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TowerDeadend5.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TowerDeadend5 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TowerDeadend5.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TowerDeadend5 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload5/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend5.html', {   # *************
                'form': TowerDeadendForm5(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TowerDeadendForm5(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TowerDeadend5',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TowerDeadend5] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload5/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TowerDeadend5 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TowerDeadendForm5(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TowerDeadend5',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TowerDeadendForm5()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TowerDeadend5 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend5.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })



def tdeadend5_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TowerDeadend5, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend5FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload5/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend5FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend5_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tupload3(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload3] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload3] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload3] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload3] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload3] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload3] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TowerDeadend3 data for this structure
                if not circuit_id:
                    circuit_exists = TowerDeadend3.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TowerDeadend3.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload3] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload3] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload3] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TowerDeadend3.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload3] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TowerDeadend3.DoesNotExist:    # **********
                        print(f"DEBUG [tupload3] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TowerDeadend3.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend3.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload3] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload3] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload3] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TowerDeadend3.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend3.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload3] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TowerDeadend3.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TowerDeadend3.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload3] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload3] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload3] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend3/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TowerDeadend3',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload3] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile3.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload2.html', {
                    'form': tUploadedFileForm3(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files3__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = tUploadedFileForm3(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases33(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload3/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile3.objects.filter(structure=structure).exists()  # ***************
        form = tUploadedFileForm3()      # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files3__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload3.html', {
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


def tupload4(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload4] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload4] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload4] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload4] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload4] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload4] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TowerDeadend3 data for this structure
                if not circuit_id:
                    circuit_exists = TowerDeadend4.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TowerDeadend4.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload4] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload4] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload4] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TowerDeadend4.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload4] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TowerDeadend4.DoesNotExist:     # **********
                        print(f"DEBUG [tupload4] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TowerDeadend4.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend4.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload4] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload4] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload4] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TowerDeadend4.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend4.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload4] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TowerDeadend4.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TowerDeadend4.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload4] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload4] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload4] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend4/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TowerDeadend4',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload4] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile4.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload4.html', {
                    'form': tUploadedFileForm4(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files4__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = tUploadedFileForm4(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases4(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload4/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile4.objects.filter(structure=structure).exists()  # ***************
        form = tUploadedFileForm4()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files4__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile4.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload4.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


def tupload5(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload5] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload5] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload5] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload5] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload5] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload5] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TowerDeadend5 data for this structure
                if not circuit_id:
                    circuit_exists = TowerDeadend5.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TowerDeadend5.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload5] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload5] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload5] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TowerDeadend5.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload5] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TowerDeadend5.DoesNotExist:    # **********
                        print(f"DEBUG [tupload5] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TowerDeadend5.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend5.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload5] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload5] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload5] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TowerDeadend5.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TowerDeadend5.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload5] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TowerDeadend5.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TowerDeadend5.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload5] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload5] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload5] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend5/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TowerDeadend5',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload5] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile5.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload5.html', {
                    'form': tUploadedFileForm5(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files5__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = tUploadedFileForm5(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases5(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload5/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile5.objects.filter(structure=structure).exists()  # ***************
        form = tUploadedFileForm5()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files5__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile5.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload5.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


def tdeadend6(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend6 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend6.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend6.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend6 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend6.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend6 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload6/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend6.html', {   # *************
                'form': TDeadendForm6(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm6(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend6',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend6] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload6/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend6 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm6(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend6',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm6()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend6 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend6.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })



def tdeadend6_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend6, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend6FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload6/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend6FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend6_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tupload6(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload6] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload6] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload6] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload6] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload6] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload6] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend6 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend6.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend6.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload6] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload6] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload6] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend6.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload6] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend6.DoesNotExist:    # *************
                        print(f"DEBUG [tupload6] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend6.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend6.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload6] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload6] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload6] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend6.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend6.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload6] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend6.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend6.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload6] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload6] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload6] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend6/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend6',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload6] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile6.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload6.html', {
                    'form': TUDeadendForm6(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files6__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm6(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases6(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload6/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile6.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm6()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files6__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile6.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload6.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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

def tdeadend7_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend7, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend7FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload7/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend7FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend7_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tdeadend8_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend8, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend8FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload8/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend8FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend8_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tdeadend9_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend9, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend9FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload9/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend9FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend9_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tdeadend10_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend10, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend10FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload10/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend10FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend10_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })
    
    
def tdeadend11_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(TDeadend11, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = TDeadend11FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/tupload11/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = TDeadend11FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/tdeadend11_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def tdeadend7(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend7 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend7.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend7.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend7 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend7.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend7 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload7/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend7.html', {   # *************
                'form': TDeadendForm7(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm7(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend7',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend7] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload7/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend7 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm7(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend7',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm7()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend7 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend7.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tupload7(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload7] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload7] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload7] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload7] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload7] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload7] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend7 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend7.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend7.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload7] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload7] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload7] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend7.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload7] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend7.DoesNotExist:    # *************
                        print(f"DEBUG [tupload7] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend7.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend7.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload7] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload7] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload7] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend7.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend7.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload7] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend7.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend7.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload7] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload7] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload7] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend7/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend7',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload7] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile7.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload7.html', {
                    'form': TUDeadendForm7(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files7__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm7(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases7(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload7/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile7.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm7()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files7__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile7.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload7.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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



def tdeadend8(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend8 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend8.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend8.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend8 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend8.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend8 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload8/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend8.html', {   # *************
                'form': TDeadendForm8(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm8(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend8',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend8] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload8/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend8 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm8(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend8',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm8()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend8 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend8.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tupload8(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload8] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload8] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload8] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload8] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload8] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload8] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend8 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend8.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend8.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload8] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload8] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload8] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend8.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload8] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend8.DoesNotExist:    # *************
                        print(f"DEBUG [tupload8] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend8.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend8.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload8] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload8] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload8] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend8.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend8.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload8] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend8.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend8.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload8] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload8] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload8] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend8/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend8',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload8] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile8.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload8.html', {
                    'form': TUDeadendForm8(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files8__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm8(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases8(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload8/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile8.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm8()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files8__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile8.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload8.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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

def tdeadend9(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend9 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend9.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend9.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend9 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend9.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend9 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload9/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend9.html', {   # *************
                'form': TDeadendForm9(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm9(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend9',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend9] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload9/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend9 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm9(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend9',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm9()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend9 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend9.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tupload9(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload9] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload9] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload9] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload9] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload9] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload9] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend9 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend9.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend9.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [tupload9] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload9] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload9] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend9.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload9] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend9.DoesNotExist:    # *************
                        print(f"DEBUG [tupload9] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend9.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend9.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload9] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload9] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload9] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend9.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend9.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload9] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend9.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend9.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload9] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload9] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload9] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend9/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend9',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload9] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile9.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload8.html', {
                    'form': TUDeadendForm9(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files9__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm9(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases9(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload9/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile9.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm9()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files9__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile9.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload9.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


def tdeadend10(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend10 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend10.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend10.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend10 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend10.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend10 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload10/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend10.html', {   # *************
                'form': TDeadendForm10(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm10(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend10',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend10] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - TDeadend10] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload10/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend10 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm10(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend10',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm10()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend10 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend10.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tupload10(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload10] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload10] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload10] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload10] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload10] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload10] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend10 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend10.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend10.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [TDeadend10] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload10] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload10] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend10.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload10] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend9.DoesNotExist:    # *************
                        print(f"DEBUG [tupload10] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend10.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend10.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload10] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload10] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload10] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend10.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend10.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload10] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend10.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend10.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload10] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload10] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload10] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend10/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend10',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload10] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile10.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload10.html', {
                    'form': TUDeadendForm10(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files10__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm10(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases10(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload10/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile10.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm10()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files10__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile10.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload10.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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

def tdeadend11(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [TDeadend11 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = TDeadend11.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = TDeadend11.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing TDeadend11 data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except TDeadend11.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No TDeadend11 data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/tupload11/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/tdeadend11.html', {   # *************
                'form': TDeadendForm11(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = TDeadendForm11(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'TDeadend11',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [TDeadend11] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - TDeadend10] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/tupload11/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [TDeadend11 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = TDeadendForm11(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'TDeadend11',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = TDeadendForm11()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [TDeadend11 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/tdeadend11.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def tupload11(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [tupload11] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [tupload11] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [tupload11] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [tupload11] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [tupload11] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [tupload11] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any TDeadend11 data for this structure
                if not circuit_id:
                    circuit_exists = TDeadend11.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = TDeadend11.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [TDeadend11] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [tupload11] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [tupload11] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = TDeadend11.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [tupload11] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except TDeadend9.DoesNotExist:    # *************
                        print(f"DEBUG [tupload11] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = TDeadend11.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend11.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload11] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [tupload11] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [tupload11] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = TDeadend11.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = TDeadend11.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [tupload11] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = TDeadend11.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = TDeadend11.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [tupload11] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [tupload11] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [tupload11] - No circuit data found, redirecting to tdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/tdeadend11/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'TDeadend11',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [tupload11] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = tUploadedFile11.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/tupload11.html', {
                    'form': TUDeadendForm11(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(tuploaded_files11__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = TUDeadendForm11(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    textract_load_cases11(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/tupload11/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = tUploadedFile11.objects.filter(structure=structure).exists()  # ***************
        form = TUDeadendForm11()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(tuploaded_files11__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = tUploadedFile11.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/tupload11.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


import time 

import time

def hdeadend1(request):
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [Circuit Definition Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = HDeadend1.objects.filter(structure=structure).exists()
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = HDeadend1.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing HDeadend1 data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except HDeadend1.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No HDeadend1 data found for structure ID: {structure_id}")
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Pass session data to upload page
            return HttpResponseRedirect(
                f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}'
                f'&popup_actions={",".join(request.session.get("active_popups", []))}'
            )
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/hdeadend1.html', {
                'form': HDeadendForm1(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),  # Pass to template
                'session_structure_type': request.session.get('selected_structure_type', '')
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'HDeadend1',  # Identifier for this form type
                    'circuit_id': instance.id,     # Database ID of the saved record
                    'timestamp': time.time(),      # For debugging/tracking
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [Circuit Definition] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(
                    f'/hupload1/?structure_id={structure_id}&structure_type={structure_type}'
                    f'&popup_actions={",".join(request.session.get("active_popups", []))}'
                )
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = HDeadendForm1(instance=existing_circuit_data)
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'HDeadend1',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = HDeadendForm1()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/hdeadend1.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),  # Pass session data to template
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),  # NEW: Pass circuit definition
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
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [HDeadend2 Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = HDeadend2.objects.filter(structure=structure).exists()
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = HDeadend2.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing HDeadend2 data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except HDeadend2.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No HDeadend2 data found for structure ID: {structure_id}")
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/hupload2/?structure_id={structure_id}&structure_type={structure_type}')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/hdeadend2.html', {
                'form': HDeadendForm2(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = HDeadendForm2(request.POST)
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'HDeadend2',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [HDeadend2] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend2] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/hupload2/?structure_id={structure_id}&structure_type={structure_type}')
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [HDeadend2 Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = HDeadendForm2(instance=existing_circuit_data)
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'HDeadend2',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = HDeadendForm2()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [HDeadend2 GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/hdeadend2.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })


def hdeadend2_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(HDeadend2, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = HDeadendForm2UpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/hupload2/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm2UpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/hdeadend2_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })


def hupload2(request):           # ****************
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
            circuit_data_exists = HDeadend2.objects.filter(structure=structure).exists() # ****************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        return HttpResponseRedirect(f'/hdeadend2/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = hUploadedFile2.objects.filter(structure=structure).exists()  # ****************
            
            if existing_file_check:
                return render(request, 'app1/hupload2.html', {       # ****************
                    'form': HUDeadendForm2(),                        # ****************
                    'structures_with_files': ListOfStructure.objects.filter(huploaded_files2__isnull=False).distinct(),  # ****************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = HUDeadendForm2(request.POST, request.FILES)       # ****************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    extract_load_cases2(instance)    # *****************
                    
                    # Clear session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    request.session.pop('circuit_structure_id', None)
                    
                    # Redirect to show updated state
                    return HttpResponseRedirect(f'/hupload2/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
                    
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
        existing_file = hUploadedFile2.objects.filter(structure=structure).exists()  # ****************
        form = HUDeadendForm2()                  # ****************
        
    structures_with_files = ListOfStructure.objects.filter(huploaded_files2__isnull=False).distinct()  # ****************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile2.objects.filter(structure=structure).latest('uploaded_at')  # ****************
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

    return render(request, 'app1/hupload2.html', {          # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
    })

def hupload2_update(request):      # **************
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm2(request.POST, request.FILES)  # **************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile2.objects.get(structure=structure)  # **************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases2(uploaded_file)    # **************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload2_update')     # **************
                  
            except hUploadedFile2.DoesNotExist:         # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm2()             # **************

    return render(request, 'app1/hupload2_update.html', {         # **************
        'form': form
    })
    
def extract_load_cases2(uploaded_file):              # **************
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


def hdeadend3(request):
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [HDeadend3 Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = HDeadend3.objects.filter(structure=structure).exists()
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = HDeadend3.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing HDeadend3 data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except HDeadend3.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No HDeadend3 data found for structure ID: {structure_id}")
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/hupload3/?structure_id={structure_id}&structure_type={structure_type}')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/hdeadend3.html', {
                'form': HDeadendForm3(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = HDeadendForm3(request.POST)
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'HDeadend3',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [HDeadend3] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend3] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/hupload3/?structure_id={structure_id}&structure_type={structure_type}')
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [HDeadend3 Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = HDeadendForm3(instance=existing_circuit_data)
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'HDeadend3',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = HDeadendForm3()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [HDeadend3 GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/hdeadend3.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def hdeadend3_update(request, pk):
    hdeadend = get_object_or_404(HDeadend3, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = HDeadendForm3UpdateForm(request.POST, instance=hdeadend)        # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/hupload3/?structure_id={structure_id}&structure_type={structure_type}'     # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm3UpdateForm(instance=hdeadend)        # ***************

    return render(request, 'app1/hdeadend3_update.html', {          # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })


def hupload3(request):           # ****************
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
            circuit_data_exists = HDeadend3.objects.filter(structure=structure).exists() # ****************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        return HttpResponseRedirect(f'/hdeadend3/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = hUploadedFile3.objects.filter(structure=structure).exists()  # ****************
            
            if existing_file_check:
                return render(request, 'app1/hupload3.html', {       # ****************
                    'form': HUDeadendForm3(),                        # ****************
                    'structures_with_files': ListOfStructure.objects.filter(huploaded_files3__isnull=False).distinct(),  # ****************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = HUDeadendForm3(request.POST, request.FILES)       # ****************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    hextract_load_cases3(instance)    # *****************
                    
                    # Clear session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    request.session.pop('circuit_structure_id', None)
                    
                    # Redirect to show updated state
                    return HttpResponseRedirect(f'/hupload3/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
                    
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
        existing_file = hUploadedFile3.objects.filter(structure=structure).exists()  # ****************
        form = HUDeadendForm3()                  # ****************
        
    structures_with_files = ListOfStructure.objects.filter(huploaded_files3__isnull=False).distinct()  # ****************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')  # ****************
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

    return render(request, 'app1/hupload3.html', {          # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
    })

def hupload3_update(request):      # **************
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm3(request.POST, request.FILES)  # **************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile3.objects.get(structure=structure)  # **************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                hextract_load_cases3(uploaded_file)    # **************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload3_update')     # **************
                  
            except hUploadedFile3.DoesNotExist:         # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm3()             # **************

    return render(request, 'app1/hupload3_update.html', {         # **************
        'form': form
    })
    
def hextract_load_cases3(uploaded_file):              # **************
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
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [HDeadend4 Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = HDeadend4.objects.filter(structure=structure).exists()
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = HDeadend4.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing HDeadend4 data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except HDeadend4.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No HDeadend4 data found for structure ID: {structure_id}")
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/hupload4/?structure_id={structure_id}&structure_type={structure_type}')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/hdeadend4.html', {
                'form': HDeadendForm4(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = HDeadendForm4(request.POST)
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'HDeadend4',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [HDeadend4] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - HDeadend4] - All session data:")
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/hupload4/?structure_id={structure_id}&structure_type={structure_type}')
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [HDeadend4 Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = HDeadendForm4(instance=existing_circuit_data)
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'HDeadend4',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = HDeadendForm4()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [HDeadend4 GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/hdeadend4.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })
    
    
def hdeadend4_update(request, pk):
    hdeadend = get_object_or_404(HDeadend4, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = HDeadendForm4UpdateForm(request.POST, instance=hdeadend)        # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/hupload4/?structure_id={structure_id}&structure_type={structure_type}'     # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = HDeadendForm4UpdateForm(instance=hdeadend)        # ***************

    return render(request, 'app1/hdeadend4_update.html', {          # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def hupload4(request):           # ****************
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
            circuit_data_exists = HDeadend4.objects.filter(structure=structure).exists() # ****************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        return HttpResponseRedirect(f'/hdeadend4/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = hUploadedFile4.objects.filter(structure=structure).exists()  # ****************
            
            if existing_file_check:
                return render(request, 'app1/hupload4.html', {       # ****************
                    'form': HUDeadendForm4(),                        # ****************
                    'structures_with_files': ListOfStructure.objects.filter(huploaded_files4__isnull=False).distinct(),  # ****************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = HUDeadendForm4(request.POST, request.FILES)       # ****************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    hextract_load_cases4(instance)    # *****************
                    
                    # Clear session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    request.session.pop('circuit_structure_id', None)
                    
                    # Redirect to show updated state
                    return HttpResponseRedirect(f'/hupload4/?structure_id={structure_id}&structure_type={structure_type}')  # ****************
                    
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
        existing_file = hUploadedFile4.objects.filter(structure=structure).exists()  # ****************
        form = HUDeadendForm4()                  # ****************
        
    structures_with_files = ListOfStructure.objects.filter(huploaded_files4__isnull=False).distinct()  # ****************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = hUploadedFile3.objects.filter(structure=structure).latest('uploaded_at')  # ****************
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

    return render(request, 'app1/hupload4.html', {          # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
    })

def hupload4_update(request):      # **************
    """
    Single page update view with structure selection and file upload
    """
    if request.method == 'POST':
        form = HUDeadendUpdateForm4(request.POST, request.FILES)  # **************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = hUploadedFile4.objects.get(structure=structure)  # **************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                hextract_load_cases4(uploaded_file)    # **************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('hupload4_update')     # **************
                  
            except hUploadedFile4.DoesNotExist:         # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = HUDeadendUpdateForm4()             # **************

    return render(request, 'app1/hupload4_update.html', {         # **************
        'form': form
    })
    
def hextract_load_cases4(uploaded_file):              # **************
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
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [Monopole Circuit Definition Page] - Session data received:")
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = MonopoleDeadend.objects.filter(structure=structure).exists()
            
            # Get the latest record if data exists
            if existing_data:
                existing_circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')
                print(f"DEBUG [Existing Data Found] - Found existing MonopoleDeadend data for structure ID: {structure_id}")
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except MonopoleDeadend.DoesNotExist:
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No MonopoleDeadend data found for structure ID: {structure_id}")
    
    # Handle Next button click (for existing data)
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Pass session data to upload page with circuit_id
            circuit_id = existing_circuit_data.id if existing_circuit_data else None
            if circuit_id:
                return HttpResponseRedirect(
                    f'/mupload1/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={circuit_id}'
                    f'&popup_actions={",".join(request.session.get("active_popups", []))}'
                )
            else:
                return HttpResponseRedirect(
                    f'/mupload1/?structure_id={structure_id}&structure_type={structure_type}'
                    f'&popup_actions={",".join(request.session.get("active_popups", []))}'
                )
        else:
            return redirect('home')
    
    # 🔥 CRITICAL FIX: Check if this is a redirect from a successful POST
    # If we have circuit_id in GET params and data exists, show the existing data view
    if request.method == 'GET' and request.GET.get('circuit_id'):
        try:
            circuit_id = request.GET.get('circuit_id')
            existing_circuit_data = MonopoleDeadend.objects.get(id=circuit_id)
            existing_data = True
            
            # Force re-check existing data to ensure we show the right view
            if structure_id:
                existing_data = MonopoleDeadend.objects.filter(structure_id=structure_id).exists()
                if existing_data:
                    existing_circuit_data = MonopoleDeadend.objects.filter(structure_id=structure_id).latest('id')
            
            print(f"DEBUG [Redirect with circuit_id] - Showing existing data view for circuit_id: {circuit_id}")
        except (MonopoleDeadend.DoesNotExist, ValueError):
            pass
    
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # If data already exists, prevent saving new data
        if existing_data:
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Data already exists for this structure.'
                })
            return render(request, 'app1/mdeadend1.html', {
                'form': MDeadendForm(instance=existing_circuit_data),
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'existing_circuit_data': existing_circuit_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', '')
            })
        
        form = MDeadendForm(request.POST)
        if form.is_valid():
            try:
                # Force the structure from URL parameter
                instance = form.save(commit=False)
                if structure:
                    instance.structure = structure
                instance.save()
                
                # 🔥 IMPORTANT: Immediately update existing_data flag
                existing_data = True
                existing_circuit_data = instance
                
                # Store structure info in session for upload page
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type
                request.session['circuit_structure_id'] = instance.id
                
                # Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'MonopoleDeadend',
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [Monopole Circuit Definition] - Stored in session:")
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # For AJAX request, return success response with redirect URL
                if is_ajax:
                    # 🔥 Return a redirect URL instead of success message
                    return JsonResponse({
                        'status': 'success_redirect',
                        'redirect_url': f'/mdeadend1/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={instance.id}&refresh=true',
                        'message': 'Data saved successfully',
                        'structure_id': structure_id,
                        'structure_type': structure_type,
                        'circuit_id': instance.id
                    })
                
                # 🔥 For non-AJAX request, redirect back to same page with circuit_id
                # This ensures the page shows existing data view after refresh
                return HttpResponseRedirect(
                    f'/mdeadend1/?structure_id={structure_id}&structure_type={structure_type}&circuit_id={instance.id}&refresh=true'
                )
                
            except IntegrityError:
                error_msg = 'Data already added for this structure.'
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'errors': {'__all__': [error_msg]}
                    })
                form.add_error('structure', error_msg)
            except Exception as e:
                error_msg = f'Error saving data: {str(e)}'
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'errors': {'__all__': [error_msg]}
                    })
                form.add_error(None, error_msg)
        else:
            # Form is invalid
            print(f"DEBUG [Monopole Form Errors] - Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            
            # For AJAX request, return errors in JSON format
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                })
    
    else:
        # GET request - create form
        # Check if we should show popup immediately (after redirect from successful save)
        show_popup_immediately = request.GET.get('refresh') == 'true'
        
        if existing_data and existing_circuit_data:
            form = MDeadendForm(instance=existing_circuit_data)
            
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'MonopoleDeadend',
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Monopole Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
            
            # 🔥 If we're coming from a successful save, show popup immediately
            if show_popup_immediately:
                print(f"DEBUG [Show Popup Immediately] - Redirected from successful save")
        else:
            # Create empty form for new data
            form = MDeadendForm()
        
        # Debug: Print session state on GET request
        print(f"DEBUG [Monopole GET Request] - Current session state:")
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")
        print(f"  Show popup immediately: {show_popup_immediately}")

    return render(request, 'app1/mdeadend1.html', {
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'existing_circuit_data': existing_circuit_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
        'show_popup_immediately': show_popup_immediately,  # 🔥 Pass this to template
    })

def mdeadend1_update(request, pk):
    mdeadend = get_object_or_404(MonopoleDeadend, pk=pk)

    selected_structure = mdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = MDeadend1FormUpdateForm(request.POST, instance=mdeadend)
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/mupload1/?structure_id={structure_id}&structure_type={structure_type}'
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend1FormUpdateForm(instance=mdeadend)

    return render(request, 'app1/mdeadend1_update.html', {
        'form': form,
        'mdeadend': mdeadend,  # Changed from 'hdeadend' to 'mdeadend'
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })

def monopole_deadend_view(request):
    monopoles = MonopoleDeadend.objects.all()
    return render(request, 'app1/monopole_deadend_view.html', {'monopoles': monopoles})



def upload1(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [mupload1] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [mupload1] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [mupload1] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [mupload1] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [mupload1] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [mupload1] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any MonopoleDeadend data for this structure
                if not circuit_id:
                    circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [MonopoleDeadend] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [mupload1] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [mupload1] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = MonopoleDeadend.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [mupload1] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except MonopoleDeadend.DoesNotExist:    # *************
                        print(f"DEBUG [mupload1] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload1] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [mupload1] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [mupload1] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload1] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [mupload1] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [mupload1] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [mupload1] - No circuit data found, redirecting to mdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/mdeadend1/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'MonopoleDeadend',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [mupload1] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = UploadedFile1.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/upload1.html', {
                    'form': UploadedFileForm(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(muploaded_files1__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = UploadedFileForm(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    mextract_load_cases1(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/mupload1/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = UploadedFile1.objects.filter(structure=structure).exists()  # ***************
        form = UploadedFileForm()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(muploaded_files1__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = UploadedFile1.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/upload1.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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




def upload2(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [mupload2] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [mupload2] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [mupload2] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [mupload2] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [mupload2] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [mupload2] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any MonopoleDeadend data for this structure
                if not circuit_id:
                    circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [MonopoleDeadend] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [mupload2] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [mupload2] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = MonopoleDeadend.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [mupload2] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except MonopoleDeadend.DoesNotExist:    # *************
                        print(f"DEBUG [mupload2] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload2] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [mupload2] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [mupload2] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload2] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = MonopoleDeadend.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = MonopoleDeadend.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [mupload2] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [mupload2] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [mupload2] - No circuit data found, redirecting to mdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/mdeadend1/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'MonopoleDeadend',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [mupload2] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = UploadedFile22.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/upload2.html', {
                    'form': UploadedFileForm2(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(muploaded_files22__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = UploadedFileForm2(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    mextract_load_cases2(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/mupload2/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = UploadedFile22.objects.filter(structure=structure).exists()  # ***************
        form = UploadedFileForm2()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(muploaded_files22__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = UploadedFile22.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/upload2.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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
        
        
        
def mdeadend5(request):        # **************
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    # DEBUG: Print session data at the start of circuit definition
    print(f"DEBUG [MDeadend5 Page] - Session data received:")    # **************
    print(f"  selected_structure_type: {request.session.get('selected_structure_type')}")
    print(f"  selected_structure_id: {request.session.get('selected_structure_id')}")
    print(f"  active_popups: {request.session.get('active_popups', [])}")
    print(f"  popup_selections: {request.session.get('popup_selections', {})}")
    print(f"  Query params - structure_type: {structure_type}, structure_id: {structure_id}")
    
    # Use session data if query params are missing
    if not structure_type and 'selected_structure_type' in request.session:
        structure_type = request.session['selected_structure_type']
    
    if not structure_id and 'selected_structure_id' in request.session:
        structure_id = request.session['selected_structure_id']
    
    # Initialize variables
    structure = None
    existing_data = False
    existing_circuit_data = None
    
    # Get structure object safely
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            # Check if data already exists for this structure
            existing_data = MDeadend5.objects.filter(structure=structure).exists()   # **************
            
            # NEW: If data exists, get the latest record
            if existing_data:
                existing_circuit_data = MDeadend5.objects.filter(structure=structure).latest('id')  # **************
                print(f"DEBUG [Existing Data Found] - Found existing MonopoleDeadend data for structure ID: {structure_id}")  # **************
        except ListOfStructure.DoesNotExist:
            return redirect('home')
        except MDeadend5.DoesNotExist:         # *******************
            existing_circuit_data = None
            print(f"DEBUG [No Existing Data] - No MonopoleDeadend data found for structure ID: {structure_id}")  # **************
    
    # Handle Next button click
    if request.method == 'GET' and request.GET.get('next') == 'true':
        if structure_id and structure_type and existing_data:
            # Redirect to upload page
            return HttpResponseRedirect(f'/mupload5/?structure_id={structure_id}&structure_type={structure_type}')  # **************
        else:
            return redirect('home')
    
    if request.method == 'POST':
        # If data already exists, prevent saving new data
        if existing_data:
            return render(request, 'app1/mdeadend5.html', {   # *************
                'form': MDeadendForm5(instance=existing_circuit_data),    # *************
                'structure_type': structure_type,
                'selected_structure': structure,
                'structure_id': structure_id,
                'existing_data': existing_data,
                'session_popups': request.session.get('active_popups', []),
                'session_structure_type': request.session.get('selected_structure_type', ''),
                'session_circuit_definition': request.session.get('circuit_definition', {}),
            })
        
        form = MDeadendForm5(request.POST)     # ****************
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
                
                # NEW: Store circuit definition data in session
                circuit_definition_data = {
                    'num_3_phase_circuits': form.cleaned_data.get('num_3_phase_circuits'),
                    'num_shield_wires': form.cleaned_data.get('num_shield_wires'),
                    'num_1_phase_circuits': form.cleaned_data.get('num_1_phase_circuits'),
                    'num_communication_cables': form.cleaned_data.get('num_communication_cables'),
                    'circuit_model': 'MDeadend5',    # **************
                    'circuit_id': instance.id,
                    'timestamp': time.time(),
                }
                
                # Store in session
                request.session['circuit_definition'] = circuit_definition_data
                
                # Debug: Print stored circuit definition data
                print(f"DEBUG [MDeadend5] - Stored in session:")    # *************
                print(f"  Circuit Definition Data: {circuit_definition_data}")
                
                # Debug: Print complete session data
                print(f"DEBUG [Complete Session - MDeadend5] - All session data:")   # **********
                print(f"  Structure Type: {request.session.get('selected_structure_type')}")
                print(f"  Structure ID: {request.session.get('selected_structure_id')}")
                print(f"  Active Popups: {request.session.get('active_popups', [])}")
                print(f"  Popup Selections: {request.session.get('popup_selections', {})}")
                print(f"  Circuit Definition: {request.session.get('circuit_definition', {})}")
                
                # Redirect directly to upload page after successful save
                return HttpResponseRedirect(f'/mupload5/?structure_id={structure_id}&structure_type={structure_type}')   # ****************
            except IntegrityError:
                form.add_error('structure', 'Data already added for this structure.')
            except Exception as e:
                form.add_error(None, f'Error saving data: {str(e)}')
        else:
            # Form is invalid - debug print errors
            print(f"DEBUG [MDeadend5 Form Errors] - Form validation failed:")  # **************
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    else:
        # GET request - create form
        if existing_data and existing_circuit_data:
            # NEW: If data exists, populate form with database data
            form = MDeadendForm5(instance=existing_circuit_data)   # **************
            
            # NEW: Also update session with existing database data
            circuit_definition_data = {
                'num_3_phase_circuits': existing_circuit_data.num_3_phase_circuits,
                'num_shield_wires': existing_circuit_data.num_shield_wires,
                'num_1_phase_circuits': existing_circuit_data.num_1_phase_circuits,
                'num_communication_cables': existing_circuit_data.num_communication_cables,
                'circuit_model': 'MDeadend5',               # *******************
                'circuit_id': existing_circuit_data.id,
                'timestamp': time.time(),
            }
            
            # Update session with existing database data
            request.session['circuit_definition'] = circuit_definition_data
            
            print(f"DEBUG [Existing Data Loaded] - Loaded existing data from database:")
            print(f"  Circuit Definition Data: {circuit_definition_data}")
        else:
            # Create empty form for new data
            form = MDeadendForm5()                # ***************
        
        # Debug: Print session state on GET request
        print(f"DEBUG [MDeadendForm5 GET Request] - Current session state:")   # ***************
        print(f"  Circuit Definition in session: {request.session.get('circuit_definition', 'Not set')}")

    return render(request, 'app1/mdeadend5.html', {     # ***************
        'form': form,
        'structure_type': structure_type,
        'selected_structure': structure,
        'structure_id': structure_id,
        'existing_data': existing_data,
        'session_popups': request.session.get('active_popups', []),
        'session_structure_type': request.session.get('selected_structure_type', ''),
        'session_circuit_definition': request.session.get('circuit_definition', {}),
    })

def mupload5(request):    # ***************
    structure_id = (
        request.GET.get('structure_id') or
        request.POST.get('structure_id') or
        request.session.get('selected_structure_id')
    )
    
    # Validate and sanitize structure_id
    if structure_id:
        try:
            structure_id = int(structure_id)
        except (ValueError, TypeError):
            structure_id = None
    
    # Fallback to session if still None
    if not structure_id:
        session_structure_id = request.session.get('selected_structure_id')
        if session_structure_id:
            try:
                structure_id = int(session_structure_id)
            except (ValueError, TypeError):
                structure_id = None
    
    # If still invalid, redirect (structure_id is required)
    if not structure_id:
        return redirect('home')
    
    structure_type = (
        request.GET.get('structure_type') or
        request.POST.get('structure_type') or
        request.session.get('selected_structure_type')
    )
    circuit_id = request.GET.get('circuit_id')
    
    # Debug loggin
    print(f"DEBUG [mupload5] - Received structure_id: {structure_id}")   # **************
    print(f"DEBUG [mupload5] - Received circuit_id: '{circuit_id}' (type: {type(circuit_id)})")  # **************
    
    # Check if circuit_id is the string 'null' or 'undefined'
    if circuit_id in ['null', 'undefined', 'None', '']:
        print(f"DEBUG [mupload5] - circuit_id is invalid string: '{circuit_id}', setting to None")   # **************
        circuit_id = None
    
    structure = None
    existing_file = False
    circuit_data_exists = False
    circuit_data = None
    
    if structure_id:
        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            
            # If circuit_id is None, try to get it from session
            if not circuit_id:
                print(f"DEBUG [mupload5] - No circuit_id in URL, checking session")  # **************
                # Check session for circuit_definition
                circuit_definition = request.session.get('circuit_definition')
                if circuit_definition and 'circuit_id' in circuit_definition:
                    circuit_id = circuit_definition.get('circuit_id')
                    print(f"DEBUG [mupload5] - Got circuit_id from session circuit_definition: {circuit_id}")   # **************
                
                # Check if we have a circuit_structure_id in session
                if not circuit_id and 'circuit_structure_id' in request.session:
                    circuit_id = request.session.get('circuit_structure_id')
                    print(f"DEBUG [mupload5] - Got circuit_id from circuit_structure_id: {circuit_id}")  # **************
                
                # Check if there's any MDeadend5 data for this structure
                if not circuit_id:
                    circuit_exists = MDeadend5.objects.filter(structure=structure).exists()  # *************
                    if circuit_exists:
                        circuit_data = MDeadend5.objects.filter(structure=structure).latest('id')  # *************
                        circuit_id = circuit_data.id
                        print(f"DEBUG [MDeadend5] - Found circuit data by structure lookup: {circuit_id}")   # *************
            
            # Now process circuit_id if we have one
            if circuit_id:
                # Convert to integer if it's a string
                if isinstance(circuit_id, str):
                    if circuit_id.isdigit():
                        circuit_id = int(circuit_id)
                        print(f"DEBUG [mupload5] - Converted circuit_id to int: {circuit_id}")  # *************
                    else:
                        print(f"DEBUG [mupload5] - circuit_id is string but not digit: '{circuit_id}', setting to None")  # *************
                        circuit_id = None
                
                # Try to get circuit data by circuit_id
                if circuit_id:
                    try:
                        circuit_data = MDeadend5.objects.get(id=circuit_id, structure=structure)  # *************
                        circuit_data_exists = True
                        print(f"DEBUG [mupload5] - Found circuit data by circuit_id: {circuit_id}")  # *************
                    except MDeadend5.DoesNotExist:    # *************
                        print(f"DEBUG [mupload5] - Circuit not found by circuit_id {circuit_id}, trying structure lookup")  # *************
                        # Fall back to structure lookup
                        circuit_exists = MDeadend5.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MDeadend5.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload5] - Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
                            print(f"DEBUG [mupload5] - No circuit data found for structure")   # *************
                    except ValueError as e:
                        print(f"DEBUG [mupload5] - ValueError with circuit_id {circuit_id}: {e}")   # *************
                        # Try structure lookup as fallback
                        circuit_exists = MDeadend5.objects.filter(structure=structure).exists()  # *************
                        if circuit_exists:
                            circuit_data = MDeadend5.objects.filter(structure=structure).latest('id')  # *************
                            circuit_data_exists = True
                            circuit_id = circuit_data.id
                            print(f"DEBUG [mupload5] - Fallback: Found circuit data by structure: {circuit_id}")  # *************
                        else:
                            circuit_data_exists = False
            else:
                # No circuit_id at all, check if circuit data exists for structure
                circuit_exists = MDeadend5.objects.filter(structure=structure).exists()  # *************
                if circuit_exists:
                    circuit_data = MDeadend5.objects.filter(structure=structure).latest('id')  # *************
                    circuit_data_exists = True
                    circuit_id = circuit_data.id
                    print(f"DEBUG [mupload5] - No circuit_id provided, found by structure: {circuit_id}")  # *************
                else:
                    circuit_data_exists = False
                    print(f"DEBUG [mupload5] - No circuit_id and no circuit data found for structure")  # *************
                    
        except ListOfStructure.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    # Check if circuit data exists
    if not circuit_data_exists:
        print(f"DEBUG [mupload5] - No circuit data found, redirecting to mdeadend")  # *************
        # Redirect to circuit definition page
        redirect_url = f'/mdeadend5/?structure_id={structure_id}&structure_type={structure_type}'  # *************
        if circuit_id:
            redirect_url += f'&circuit_id={circuit_id}'
        return HttpResponseRedirect(redirect_url)
    
    # Ensure session has circuit data
    if circuit_data:
        circuit_definition_data = {
            'num_3_phase_circuits': circuit_data.num_3_phase_circuits,
            'num_shield_wires': circuit_data.num_shield_wires,
            'num_1_phase_circuits': circuit_data.num_1_phase_circuits,
            'num_communication_cables': circuit_data.num_communication_cables,
            'circuit_model': 'MDeadend5',  # *************
            'circuit_id': circuit_data.id,
            'timestamp': time.time(),
        }
        request.session['circuit_definition'] = circuit_definition_data
        request.session['circuit_structure_id'] = circuit_data.id
        print(f"DEBUG [mupload5] - Updated session with circuit_id: {circuit_data.id}")    # *************
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            # Check if file already exists for this structure
            existing_file_check = mUploadedFile5.objects.filter(structure=structure).exists()  # ***********
            
            if existing_file_check:
                return render(request, 'app1/mupload5.html', {
                    'form': MUDeadendForm5(),    # ***************
                    'structures_with_files': ListOfStructure.objects.filter(muploaded_files5__isnull=False).distinct(),  # ************
                    'selected_structure': structure,
                    'structure_type': structure_type,
                    'structure_id': structure_id,
                    'circuit_id': circuit_id,
                    'existing_file': existing_file_check,
                    'circuit_data_exists': circuit_data_exists
                })
            
            form = MUDeadendForm5(request.POST, request.FILES)  # ***************
            if form.is_valid():
                try:
                    # Force the structure from URL parameter
                    instance = form.save(commit=False)
                    instance.structure = structure
                    instance.save()
                    
                    mextract_load_cases5(instance)   # ***************
                    
                    # Don't clear circuit-related session data
                    request.session.pop('selected_structure_id', None)
                    request.session.pop('selected_structure_type', None)
                    
                    # Redirect to show updated state
                    redirect_url = f'/mupload5/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                    if circuit_id:
                        redirect_url += f'&circuit_id={circuit_id}'
                    return HttpResponseRedirect(redirect_url)
                    
                except IntegrityError as e:
                    form.add_error('structure', 'A file has already been uploaded for this structure.')
                except Exception as e:
                    form.add_error(None, f'Error uploading file: {str(e)}')
            else:
                # Form is invalid, show errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Set/Phase or Attachment Joint Label selection and redirect
        elif 'set_phase_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'set_phase',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
            
        elif 'joint_labels_button' in request.POST:
            # Store selection in session and redirect to canvas container
            selected_values = {
                'button_type': 'joint_labels',
                'structure_id': structure_id,
                'circuit_id': circuit_id
            }
            request.session['selected_values'] = selected_values
            return redirect('hdata1')
        
        # Handle custom group operations
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
                    
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'update_custom_group' in request.POST:
            old_group_name = request.POST.get('old_group_name')
            new_group_name = request.POST.get('new_group_name')
            
            if old_group_name and new_group_name and structure_id:
                try:
                    structure = ListOfStructure.objects.get(id=structure_id)
                    group = LoadCaseGroup.objects.get(
                        structure=structure,
                        name=old_group_name,
                        is_custom=True
                    )
                    group.name = new_group_name
                    group.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
        
        elif 'delete_custom_group' in request.POST:
            group_name = request.POST.get('group_name')
            
            if group_name and structure_id:
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
    
    else:  # GET request
        # GET request - check for existing file
        existing_file = mUploadedFile5.objects.filter(structure=structure).exists()  # ***************
        form = MUDeadendForm5()    # ************
        
    structures_with_files = ListOfStructure.objects.filter(muploaded_files5__isnull=False).distinct()  # ***************

    # Handle AJAX requests for data (GET requests only)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        structure_id = request.GET.get('structure_id')
        if not structure_id:
            return JsonResponse({'error': 'Structure ID is required'}, status=400)

        try:
            structure = ListOfStructure.objects.get(id=structure_id)
            latest_file = mUploadedFile5.objects.filter(structure=structure).latest('uploaded_at')  # ***************
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
            
            # Get custom groups for a structure
            elif request.GET.get('get_custom_groups_for_selection'):
                custom_groups = LoadCaseGroup.objects.filter(
                    structure=structure, 
                    is_custom=True
                ).prefetch_related('load_cases')
                
                groups_data = {}
                for group in custom_groups:
                    groups_data[group.name] = [case.name for case in group.load_cases.all()]
                
                return JsonResponse({'custom_groups': groups_data})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure circuit_id is always passed to template
    if not circuit_id and circuit_data:
        circuit_id = circuit_data.id
    
    return render(request, 'app1/mupload5.html', {     # ****************
        'form': form,
        'structures_with_files': structures_with_files,
        'selected_structure': structure,
        'structure_type': structure_type,
        'structure_id': structure_id,
        'circuit_id': circuit_id,
        'existing_file': existing_file,
        'circuit_data_exists': circuit_data_exists
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


def mdeadend5_update(request, pk):                    # ***************
    hdeadend = get_object_or_404(MDeadend5, pk=pk)       # ***************

    selected_structure = hdeadend.structure
    structure_id = selected_structure.id

    # ✅ Correct: Always fetch TYPE from URL (same as create flow)
    structure_type = request.GET.get('structure_type') or request.session.get('selected_structure_type')

    if request.method == 'POST':
        form = MDeadend5FormUpdateForm(request.POST, instance=hdeadend)   # ***************
        if form.is_valid():
            try:
                form.save()

                # ✅ Save structure type correctly into session
                request.session['selected_structure_id'] = structure_id
                request.session['selected_structure_type'] = structure_type

                return HttpResponseRedirect(
                    f'/mupload5/?structure_id={structure_id}&structure_type={structure_type}'  # ***************
                )

            except Exception as e:
                form.add_error(None, f'Error updating record: {str(e)}')
    else:
        form = MDeadend5FormUpdateForm(instance=hdeadend)    # ***************

    return render(request, 'app1/mdeadend5_update.html', {    # ***************
        'form': form,
        'hdeadend': hdeadend,
        'structure_id': structure_id,
        'structure_type': structure_type,  # ✅ Pass correct type
    })


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



    
def tupload1_update(request):
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = tUploadedUpdateForm1(request.POST, request.FILES)
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile1.objects.get(structure=structure)
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases1(uploaded_file)
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload1_update')
                
            except tUploadedFile1.DoesNotExist:
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = tUploadedUpdateForm1()

    return render(request, 'app1/tupload1_update.html', {
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    

def tupload2_update(request):
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = tUploadedUpdateForm2(request.POST, request.FILES)
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile2.objects.get(structure=structure)
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases3(uploaded_file)
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload2_update')
                
            except tUploadedFile2.DoesNotExist:
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = tUploadedUpdateForm2()

    return render(request, 'app1/tupload2_update.html', {
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
    
def tupload3_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm3(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile3.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases33(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload3_update')     # ****************
                  
            except tUploadedFile3.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm3()       # **************

    return render(request, 'app1/tupload3_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
    
def tupload4_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm4(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile4.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases4(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload4_update')     # ****************
                  
            except tUploadedFile4.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm4()       # **************

    return render(request, 'app1/tupload4_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
def tupload5_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm5(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile5.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                extract_load_cases5(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload5_update')     # ****************
                  
            except tUploadedFile5.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm5()       # **************

    return render(request, 'app1/tupload5_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })

    
    
def tupload6_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm6(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile6.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases6(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload6_update')     # ****************
                  
            except tUploadedFile6.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm6()       # **************

    return render(request, 'app1/tupload6_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
def tupload7_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm7(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile7.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases7(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload7_update')     # ****************
                  
            except tUploadedFile7.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm7()       # **************

    return render(request, 'app1/tupload7_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
def tupload8_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm8(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile8.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases8(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload8_update')     # ****************
                  
            except tUploadedFile8.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm8()       # **************

    return render(request, 'app1/tupload8_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
def tupload9_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm9(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile9.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases9(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload9_update')     # ****************
                  
            except tUploadedFile9.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm9()       # **************

    return render(request, 'app1/tupload9_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
def tupload10_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm10(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile10.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases10(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload10_update')     # ****************
                  
            except tUploadedFile10.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm10()       # **************

    return render(request, 'app1/tupload10_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
def tupload11_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = TUDeadendUpdateForm11(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = tUploadedFile11.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                textract_load_cases11(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('tupload11_update')     # ****************
                  
            except tUploadedFile11.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = TUDeadendUpdateForm11()       # **************

    return render(request, 'app1/tupload11_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
    
def mupload1_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = MUDeadendUpdateForm1(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = UploadedFile1.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases1(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload1_update')     # ****************
                  
            except UploadedFile1.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm1()       # **************

    return render(request, 'app1/mupload1_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
    
def mupload2_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = MUDeadendUpdateForm2(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = UploadedFile22.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases2(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload2_update')     # ****************
                  
            except UploadedFile22.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm2()       # **************

    return render(request, 'app1/mupload2_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
    })
    
    
def mupload5_update(request):    # *************
    """
    Single page update view with structure selection and file upload
    """
    structure_id = request.GET.get('structure_id')
    structure_type = request.GET.get('structure_type')
    
    if request.method == 'POST':
        form = MUDeadendUpdateForm5(request.POST, request.FILES)   # *************
        if form.is_valid():
            try:
                structure = form.cleaned_data['structure']
                new_file = form.cleaned_data['file']
                
                # Get the existing file for this structure
                uploaded_file = mUploadedFile5.objects.get(structure=structure)  # *************
                
                # Delete the old file from storage
                if uploaded_file.file:
                    uploaded_file.file.delete(save=False)
                
                # Update the file field and save
                uploaded_file.file = new_file
                uploaded_file.save()
                
                # Re-extract load cases from the updated file
                mextract_load_cases5(uploaded_file)     # ****************
                
                messages.success(request, f'File for {structure.structure} updated successfully!')
                return redirect('mupload5_update')     # ****************
                  
            except mUploadedFile5.DoesNotExist:     # **************
                messages.error(request, 'No uploaded file found for this structure.')
            except IntegrityError as e:
                messages.error(request, 'File with this structure already exists.')
            except Exception as e:
                messages.error(request, f'Error updating file: {str(e)}')
    else:
        form = MUDeadendUpdateForm5()       # **************

    return render(request, 'app1/mupload5_update.html', {       # **************
        'form': form,
        'structure_id': structure_id,
        'structure_type': structure_type
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
    
    
