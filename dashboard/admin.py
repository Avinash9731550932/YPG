from django.contrib import admin
from .models import CompanyProfile, AppLog
from import_export.admin import ImportExportModelAdmin

class AppLogAdmin(ImportExportModelAdmin):
    list_display= ('log_type','description', 'log_url', 'log_model', 'created_at')

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display= ('company_name','company_address')


admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(AppLog, AppLogAdmin)
