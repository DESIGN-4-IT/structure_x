from django.urls import path
from app1 import views 

urlpatterns = [
   path('',views.home,name='home'),
   path('help/',views.help,name='help'),
   path('deadend/',views.deadend,name='deadend'), 
   path('upload1/',views.upload1,name='upload1'), 
   path('drop1/',views.drop1,name='drop1'),
   path('chart/',views.chart,name='chart'),
   path('data/',views.data,name='data'),
   
]