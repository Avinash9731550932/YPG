from django.contrib import admin
from .models import Job, JobAssign, JobRequest, JobReport, JobReportImage
from import_export.admin import ImportExportModelAdmin

class JobAdmin(ImportExportModelAdmin):
    list_display = ('job_no','client_name','lng','status','created_at')
    list_editable = ('status',)

class JobRequestAdmin(ImportExportModelAdmin):
    list_display= ('job','employee', 'created_at')

class JobReportAdmin(admin.ModelAdmin):
    list_display= ('job','employee','attendance_note','time_on','time_off','created_at')

class JobAssignAdmin(ImportExportModelAdmin):
    list_display= ('job','employee','assigned_type','created_at')


admin.site.register(Job, JobAdmin)
admin.site.register(JobAssign, JobAssignAdmin)
admin.site.register(JobRequest, JobRequestAdmin)
admin.site.register(JobReport, JobReportAdmin)
admin.site.register(JobReportImage)
