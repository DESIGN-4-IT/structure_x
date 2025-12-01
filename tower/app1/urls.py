from django.urls import path
from app1 import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
   path('base/',views.base,name='base'),

   path('help/',views.help,name='help'),
   path('mdeadend1/',views.mdeadend1,name='mdeadend1'), 
   path('mdeadend1/update/<int:pk>/', views.mdeadend1_update, name='m_deadend1_update'),

   path('monopole_deadend_view/', views.monopole_deadend_view, name='monopole_deadend_view'),
   path('monopole_deadend_view1/', views.monopole_deadend_view1, name='monopole_deadend_view1'),
   path('monopole_deadend_view4/', views.monopole_deadend_view4, name='monopole_deadend_view4'),

   path('mdeadend/',views.mdeadend,name='mdeadend'), 
   path('hdeadend/',views.hdeadend,name='hdeadend'), 
   path('mdeadend4/',views.mdeadend4,name='mdeadend4'), 

   path('tdeadend/',views.tdeadend,name='tdeadend'), 
   path('tdeadend/update/<int:pk>/', views.tdeadend_update, name='t_deadend_update'),

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
   path('tdeadend3/update/<int:pk>/', views.tdeadend3_update, name='t_deadend3_update'),

   path('tdeadend4/',views.tdeadend4,name='tdeadend4'),
   path('tdeadend4/update/<int:pk>/', views.tdeadend4_update, name='t_deadend4_update'),

   path('tdeadend5/',views.tdeadend5,name='tdeadend5'),
   path('tdeadend5/update/<int:pk>/', views.tdeadend5_update, name='t_deadend5_update'),

   path('tupload3/',views.tupload3,name='tupload3'),
   path('tupload4/',views.tupload4,name='tupload4'),
   path('tupload5/',views.tupload5,name='tupload5'),
   
   path('tdeadend6/',views.tdeadend6,name='tdeadend6'),
   path('tdeadend6/update/<int:pk>/', views.tdeadend6_update, name='t_deadend6_update'),
   path('tupload6/',views.tupload6,name='tupload6'),
   path('t_deadend_view6/', views.t_deadend_view6, name='t_deadend_view6'),
   
   path('tdeadend7/update/<int:pk>/', views.tdeadend7_update, name='t_deadend7_update'),
   path('tdeadend8/update/<int:pk>/', views.tdeadend8_update, name='t_deadend8_update'),
   path('tdeadend9/update/<int:pk>/', views.tdeadend9_update, name='t_deadend9_update'),
   path('tdeadend10/update/<int:pk>/', views.tdeadend10_update, name='t_deadend10_update'),
   path('tdeadend11/update/<int:pk>/', views.tdeadend11_update, name='t_deadend11_update'),
   
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
   path('store-combinations/', views.store_set_phase_combinations, name='store_set_phase_combinations'),
   path('hdata1/',views.hdata1,name='hdata1'),
   path('load-cases/', views.load_cases_page, name='load_cases'),
   path('update-selection-session/', views.update_selection_session, name='update_selection_session'),  # NEW

   path('calculation/', views.calculation_view, name='calculation'),
   path('load-condition/', views.load_condition_view, name='load_condition'),
   path('get-current-selections/', views.get_current_selections, name='get_current_selections'),
   path('save-condition-selections/', views.save_condition_selections, name='save_condition_selections'),
   path('calculate-final-loads/', views.calculate_final_loads, name='calculate_final_loads'),
   path('load-condition/create/', views.create_load_condition, name='create_load_condition'),
   path('load-condition/<int:pk>/edit/', views.edit_load_condition, name='edit_load_condition'),
   path('load-condition/<int:pk>/delete/', views.delete_load_condition, name='delete_load_condition'),



   path('hupload/',views.hupload,name='hupload'),
   path('drop1/',views.drop1,name='drop1'),
   path('drop2/',views.drop2,name='drop2'),
   path('drop4/',views.drop4,name='drop4'),
   
   path('hdrop/',views.hdrop,name='hdrop'),
   path('chart/',views.chart,name='chart'),
   path('data/',views.data,name='data'),
   path('', views.list_structures, name='home'),
   path('rename-structure-group/<int:group_id>/', views.rename_structure_group, name='rename_structure_group'),
   path('add_structures/', views.add_structure, name='add_structure'),
   path('add_group/', views.add_group, name='add_group'),
   path('str_delete/<int:structure_id>/', views.delete_structure, name='delete_structure'),
   path('delete_structure_group/<int:group_id>/', views.delete_structure_group, name='delete_structure_group'),

   
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
   
   path('mdeadend5/update/<int:pk>/', views.mdeadend5_update, name='m_deadend5_update'),
   path('mdeadend6/update/<int:pk>/', views.mdeadend6_update, name='m_deadend6_update'),
   path('mdeadend7/update/<int:pk>/', views.mdeadend7_update, name='m_deadend7_update'),
   path('mdeadend8/update/<int:pk>/', views.mdeadend8_update, name='m_deadend8_update'),
   path('mdeadend9/update/<int:pk>/', views.mdeadend9_update, name='m_deadend9_update'),
   path('mdeadend10/update/<int:pk>/', views.mdeadend10_update, name='m_deadend10_update'),
   path('mdeadend11/update/<int:pk>/', views.mdeadend11_update, name='m_deadend11_update'),
   path('mdeadend12/update/<int:pk>/', views.mdeadend12_update, name='m_deadend12_update'),
   path('mdeadend13/update/<int:pk>/', views.mdeadend13_update, name='m_deadend13_update'),

   path('tupload1/update/', views.tupload1_update, name='tupload1_update'),
   path('tupload2/update/', views.tupload2_update, name='tupload2_update'),
   path('tupload3/update/', views.tupload3_update, name='tupload3_update'),
   path('tupload4/update/', views.tupload4_update, name='tupload4_update'),
   path('tupload5/update/', views.tupload5_update, name='tupload5_update'),
   path('tupload6/update/', views.tupload6_update, name='tupload6_update'),
   path('tupload7/update/', views.tupload7_update, name='tupload7_update'),
   path('tupload8/update/', views.tupload8_update, name='tupload8_update'),
   path('tupload9/update/', views.tupload9_update, name='tupload9_update'),
   path('tupload10/update/', views.tupload10_update, name='tupload10_update'),
   path('tupload11/update/', views.tupload11_update, name='tupload11_update'),
   
   path('mupload1/update/', views.mupload1_update, name='mupload1_update'),
   path('mupload2/update/', views.mupload2_update, name='mupload2_update'),
   path('mupload5/update/', views.mupload5_update, name='mupload5_update'),
   path('mupload6/update/', views.mupload6_update, name='mupload6_update'),
   path('mupload7/update/', views.mupload7_update, name='mupload7_update'),
   path('mupload8/update/', views.mupload8_update, name='mupload8_update'),
   path('mupload9/update/', views.mupload9_update, name='mupload9_update'),
   path('mupload10/update/', views.mupload10_update, name='mupload10_update'),
   path('mupload11/update/', views.mupload11_update, name='mupload11_update'),
   path('mupload12/update/', views.mupload12_update, name='mupload12_update'),
   path('mupload13/update/', views.mupload13_update, name='mupload13_update'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)