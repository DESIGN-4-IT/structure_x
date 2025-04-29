from django.shortcuts import render,get_object_or_404
from .forms import *
from .models import *
import pandas as pd


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

def mdeadend(request):
    return render(request,'app1/mdeadend.html')

def hdeadend(request):
    return render(request,'app1/hdeadend.html')

def tdeadend(request):
    return render(request,'app1/tdeadend.html')

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


def hupload(request):
    return render(request,'app1/hupload.html')

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




def hdrop(request):
    return render(request,'app1/hdrop.html')

def chart(request):
    return render(request,'app1/chart.html')

def data(request):
    return render(request,'app1/data.html')



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