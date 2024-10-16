from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'app1/home.html')


def help(request):
    return render(request,'app1/help.html')

def deadend(request):
    return render(request,'app1/deadend.html')

def hdeadend(request):
    return render(request,'app1/hdeadend.html')

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