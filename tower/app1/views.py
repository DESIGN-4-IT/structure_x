from django.shortcuts import render,get_object_or_404

# Create your views here.
def home(request):
    return render(request,'app1/home.html')


def help(request):
    return render(request,'app1/help.html')

def deadend(request):
    return render(request,'app1/deadend.html')

def hdeadend(request):
    return render(request,'app1/hdeadend.html')

def tdeadend(request):
    return render(request,'app1/tdeadend.html')

def upload1(request):
    return render(request,'app1/upload1.html')

def hupload(request):
    return render(request,'app1/hupload.html')

def drop1(request):
    return render(request,'app1/drop1.html')

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
            return redirect('list_structures')
    else:
        form = StructureForm()
    return render(request, 'app1/add_structure.html', {'form': form})


def delete_structure(request, structure_id):
    structure = get_object_or_404(ListOfStructure, id=structure_id)
    structure.delete()
    return redirect('list_structures')