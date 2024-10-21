from django.urls import path
from . import views  # Ensure you're importing views properly

urlpatterns = [
    path('', views.home, name='home'),  # Ensure you have a valid view  
    path('blank_page/', views.blank_page, name='blank_page'),
]