from django.contrib import admin
from .models import EmployeeProfile, EmployeeLoginLog, ETLog

from import_export.admin import ImportExportModelAdmin
from .resources import ETLogResource
    
class ETlogAdmin(ImportExportModelAdmin):
    resource_class = ETLogResource
    list_display= ('id','created_at', 'lat', 'lng', 'employee_id')

class EmployeeLoginLogAdmin(ImportExportModelAdmin):
    list_display= ('employee','login_time', 'logout_time')

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display= ('employee','address', 'phone_number','security_license','status')
    list_editable = ('status',)


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(EmployeeLoginLog, EmployeeLoginLogAdmin)
admin.site.register(ETLog, ETlogAdmin)
