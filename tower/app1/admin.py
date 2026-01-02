from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ListOfStructure)
admin.site.register(StructureGroup)
admin.site.register(MonopoleDeadend)
admin.site.register(UploadedFile1)
admin.site.register(MonopoleDeadend1)
admin.site.register(MonopoleDeadend4)
admin.site.register(UploadedFile2)
admin.site.register(UploadedFile22)
admin.site.register(UploadedFile4)
admin.site.register(TowerDeadend)
admin.site.register(tUploadedFile1)  
admin.site.register(TowerDeadend3)
admin.site.register(TowerDeadend4)
admin.site.register(TowerDeadend5)
admin.site.register(tUploadedFile3)  
admin.site.register(tUploadedFile4)  
admin.site.register(tUploadedFile5)   
admin.site.register(tUploadedFile6) 
admin.site.register(tUploadedFile7)
admin.site.register(tUploadedFile8)
admin.site.register(tUploadedFile9)
admin.site.register(tUploadedFile10)
admin.site.register(tUploadedFile11)
admin.site.register(HDeadend1)  
admin.site.register(hUploadedFile1)  
admin.site.register(LoadCaseGroup)
admin.site.register(LoadCase)
admin.site.register(LoadCondition)
admin.site.register(AttachmentLoad)
admin.site.register(tUploadedFile2)
admin.site.register(HDeadend3)
admin.site.register(hUploadedFile3)
admin.site.register(hUploadedFile2) 
admin.site.register(hUploadedFile4)  
admin.site.register(mUploadedFile5)
admin.site.register(mUploadedFile6)
admin.site.register(mUploadedFile7)
admin.site.register(mUploadedFile8)
admin.site.register(mUploadedFile9)
admin.site.register(mUploadedFile10)
admin.site.register(mUploadedFile11)
admin.site.register(mUploadedFile12)
admin.site.register(mUploadedFile13)


@admin.register(TowerModel)
class TowerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'structure_type', 'attachment_points', 'configuration', 'circuit_type')
    list_filter = ('structure_type', 'attachment_points', 'configuration', 'circuit_type')
    search_fields = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model_file')
        }),
        ('Categorization', {
            'fields': ('structure_type', 'attachment_points', 'configuration', 'circuit_type')
        }),
    )