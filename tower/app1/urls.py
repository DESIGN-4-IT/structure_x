from django.urls import path
from app1 import views 

urlpatterns = [

   path('help/',views.help,name='help'),
   path('deadend/',views.deadend,name='deadend'), 
   path('monopole_deadend_view/', views.monopole_deadend_view, name='monopole_deadend_view'),
   path('mdeadend/',views.mdeadend,name='mdeadend'), 
   path('hdeadend/',views.hdeadend,name='hdeadend'), 
   path('tdeadend/',views.tdeadend,name='tdeadend'), 
   path('tdeadend1/',views.tdeadend1,name='tdeadend1'),
   path('upload1/',views.upload1,name='upload1'), 
   path('hupload/',views.hupload,name='hupload'),
   path('drop1/',views.drop1,name='drop1'),
   path('hdrop/',views.hdrop,name='hdrop'),
   path('chart/',views.chart,name='chart'),
   path('data/',views.data,name='data'),
   path('', views.list_structures, name='home'),
   path('add_structures/', views.add_structure, name='add_structure'),
   path('str_delete/<int:structure_id>/', views.delete_structure, name='delete_structure'),

   
]