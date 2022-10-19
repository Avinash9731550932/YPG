from django.contrib import admin
from .models import Asset, AssetAssign
from import_export.admin import ImportExportModelAdmin

class AssetAdmin(admin.ModelAdmin):
    list_display= ('car_name','car_model', 'plate_number','created_on', 'is_available')
    list_editable = ('is_available',)

class AssetAssignAdmin(ImportExportModelAdmin):
    list_display= ('employee','asset','created_on')

admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetAssign, AssetAssignAdmin)
