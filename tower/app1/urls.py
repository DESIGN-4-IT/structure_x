from django.urls import path
from app1 import views 

urlpatterns = [
   
   path('base/',views.base,name='base'),

   path('help/',views.help,name='help'),
   path('mdeadend1/',views.mdeadend1,name='mdeadend1'), 
   path('monopole_deadend_view/', views.monopole_deadend_view, name='monopole_deadend_view'),
   path('monopole_deadend_view1/', views.monopole_deadend_view1, name='monopole_deadend_view1'),
   path('monopole_deadend_view4/', views.monopole_deadend_view4, name='monopole_deadend_view4'),

   path('mdeadend/',views.mdeadend,name='mdeadend'), 
   path('hdeadend/',views.hdeadend,name='hdeadend'), 
   path('mdeadend4/',views.mdeadend4,name='mdeadend4'), 

   path('tdeadend/',views.tdeadend,name='tdeadend'), 
   path('tupload1/',views.tupload1,name='tupload1'),
   path('tower_deadend_view1/', views.tower_deadend_view1, name='tower_deadend_view1'),
   path('tower_deadend_view3/', views.tower_deadend_view3, name='tower_deadend_view3'),
   path('tower_deadend_view4/', views.tower_deadend_view4, name='tower_deadend_view4'),
   path('tower_deadend_view5/', views.tower_deadend_view5, name='tower_deadend_view5'),


   path('tdrop1/',views.tdrop1,name='tdrop1'),
   path('tupload2/',views.tupload2,name='tupload2'),
   path('tdrop2/',views.tdrop2,name='tdrop2'),



   path('tdeadend1/',views.tdeadend1,name='tdeadend1'),
   path('mupload1/',views.upload1,name='mupload1'),
   path('mupload2/',views.upload2,name='mupload2'),
   path('mupload4/',views.mupload4,name='mupload4'),
   path('tdeadend3/',views.tdeadend3,name='tdeadend3'),
   path('tdeadend4/',views.tdeadend4,name='tdeadend4'),
   path('tdeadend5/',views.tdeadend5,name='tdeadend5'),
   path('tupload3/',views.tupload3,name='tupload3'),
   path('tupload4/',views.tupload4,name='tupload4'),
   path('tupload5/',views.tupload5,name='tupload5'),
   
   path('tdeadend6/',views.tdeadend6,name='tdeadend6'),
   path('tupload6/',views.tupload6,name='tupload6'),
   path('t_deadend_view6/', views.t_deadend_view6, name='t_deadend_view6'),
   
   path('tdeadend7/',views.tdeadend7,name='tdeadend7'),
   path('tupload7/',views.tupload7,name='tupload7'),
   path('t_deadend_view7/', views.t_deadend_view7, name='t_deadend_view7'),
   
   path('tdeadend8/',views.tdeadend8,name='tdeadend8'),
   path('tupload8/',views.tupload8,name='tupload8'),
   path('t_deadend_view8/', views.t_deadend_view8, name='t_deadend_view8'),
   
   path('tdeadend9/',views.tdeadend9,name='tdeadend9'),
   path('tupload9/',views.tupload9,name='tupload9'),
   path('t_deadend_view9/', views.t_deadend_view9, name='t_deadend_view9'),
   
   path('tdeadend10/',views.tdeadend10,name='tdeadend10'),
   path('tupload10/',views.tupload10,name='tupload10'),
   path('t_deadend_view10/', views.t_deadend_view10, name='t_deadend_view10'),
   
   path('tdeadend11/',views.tdeadend11,name='tdeadend11'),
   path('tupload11/',views.tupload11,name='tupload11'),
   path('t_deadend_view11/', views.t_deadend_view11, name='t_deadend_view11'),
   
   path('tdrop3/',views.tdrop3,name='tdrop3'),
   path('tdrop4/',views.tdrop4,name='tdrop4'),
   path('tdrop5/',views.tdrop5,name='tdrop5'),


   path('hdeadend1/',views.hdeadend1,name='hdeadend1'),
   path('hdeadend1/update/<int:pk>/', views.hdeadend1_update, name='h_deadend1_update'),

   path('hupload1/',views.hupload1,name='hupload1'),
   path('hupload1/update/', views.hupload1_update, name='hupload1_update'),

   path('hdrop1/',views.hdrop1,name='hdrop1'),
   path('hdeadend2/',views.hdeadend2,name='hdeadend2'),
   path('hdeadend2/update/<int:pk>/', views.hdeadend2_update, name='h_deadend2_update'),

   path('hupload2/',views.hupload2,name='hupload2'),
   path('hupload2/update/', views.hupload2_update, name='hupload2_update'),

   path('hdrop2/',views.hdrop2,name='hdrop2'),
   path('h_deadend_view1/', views.h_deadend_view1, name='h_deadend_view1'),
   path('h_deadend_view2/', views.h_deadend_view2, name='h_deadend_view2'),
   path('hdeadend3/',views.hdeadend3,name='hdeadend3'),
   path('hdeadend3/update/<int:pk>/', views.hdeadend3_update, name='h_deadend3_update'),

   path('hupload3/',views.hupload3,name='hupload3'),
   path('hupload3/update/', views.hupload3_update, name='hupload3_update'),

   path('h_deadend_view3/', views.h_deadend_view3, name='h_deadend_view3'),
   path('hdeadend4/',views.hdeadend4,name='hdeadend4'),
   path('hdeadend4/update/<int:pk>/', views.hdeadend4_update, name='h_deadend4_update'),

   path('hupload4/',views.hupload4,name='hupload4'),
   path('hupload4/update/', views.hupload4_update, name='hupload4_update'),
   path('h_deadend_view4/', views.h_deadend_view4, name='h_deadend_view4'),

   path('hdata1/',views.hdata1,name='hdata1'),
   path('calculation/', views.calculation_view, name='calculation'),
   path('load-condition/', views.load_condition_view, name='load_condition'),
   path('calculate-final-loads/', views.calculate_final_loads, name='calculate_final_loads'),



   path('hupload/',views.hupload,name='hupload'),
   path('drop1/',views.drop1,name='drop1'),
   path('drop2/',views.drop2,name='drop2'),
   path('drop4/',views.drop4,name='drop4'),
   
   path('hdrop/',views.hdrop,name='hdrop'),
   path('chart/',views.chart,name='chart'),
   path('data/',views.data,name='data'),
   path('', views.list_structures, name='home'),
   path('add_structures/', views.add_structure, name='add_structure'),
   path('str_delete/<int:structure_id>/', views.delete_structure, name='delete_structure'),
   
   
   path('mdeadend5/',views.mdeadend5,name='mdeadend5'),
   path('mupload5/',views.mupload5,name='mupload5'),
   path('m_deadend_view5/', views.m_deadend_view5, name='m_deadend_view5'),
   
   path('mdeadend6/',views.mdeadend6,name='mdeadend6'),
   path('mupload6/',views.mupload6,name='mupload6'),
   path('m_deadend_view6/', views.m_deadend_view6, name='m_deadend_view6'),
   
   path('mdeadend7/',views.mdeadend7,name='mdeadend7'),
   path('mupload7/',views.mupload7,name='mupload7'),
   path('m_deadend_view7/', views.m_deadend_view7, name='m_deadend_view7'),
   
   path('mdeadend8/',views.mdeadend8,name='mdeadend8'),
   path('mupload8/',views.mupload8,name='mupload8'),
   path('m_deadend_view8/', views.m_deadend_view8, name='m_deadend_view8'),
   
   path('mdeadend9/',views.mdeadend9,name='mdeadend9'),
   path('mupload9/',views.mupload9,name='mupload9'),
   path('m_deadend_view9/', views.m_deadend_view9, name='m_deadend_view9'),

   path('mdeadend10/',views.mdeadend10,name='mdeadend10'),
   path('mupload10/',views.mupload10,name='mupload10'),
   path('m_deadend_view10/', views.m_deadend_view10, name='m_deadend_view10'),
   
   path('mdeadend11/',views.mdeadend11,name='mdeadend11'),
   path('mupload11/',views.mupload11,name='mupload11'),
   path('m_deadend_view11/', views.m_deadend_view11, name='m_deadend_view11'),
   
   path('mdeadend12/',views.mdeadend12,name='mdeadend12'),
   path('mupload12/',views.mupload12,name='mupload12'),
   path('m_deadend_view12/', views.m_deadend_view12, name='m_deadend_view12'),
   
   path('mdeadend13/',views.mdeadend13,name='mdeadend13'),
   path('mupload13/',views.mupload13,name='mupload13'),
   path('m_deadend_view13/', views.m_deadend_view13, name='m_deadend_view13'),
   
]