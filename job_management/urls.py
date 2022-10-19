from django.urls import path
from . import views

urlpatterns = [                                                    
    path('assign-job/', views.assign_job, name="assign_job"),                                                               
    path('view-jobs/', views.view_jobs, name="view_jobs"),
    path('job-detail/<int:pk>/', views.job_detail, name="job_detail"),
    path('view-alarm-response/', views.view_alarm_response, name="view_alarm_response"),
    path('save-job/', views.save_job, name="save_job"),
    path('update-job/', views.update_job, name="update_job"),
    path('job-manual-assign/', views.job_manual_assign, name="job_manual_assign"),
    path('view-job-request-logs/', views.view_job_request_logs, name="view_job_request_logs"),
    path('view-job-assigned-logs/', views.view_job_assigned_logs, name="view_job_assigned_logs"),

    # path('report-lab/', views.report_lab, name="report_lab"),
    path('job-pusher-trigger/', views.job_pusher_trigger, name="job_pusher_trigger"),  

    ##### APIS ####
    path('auth-pusher', views.auth_pusher, name="auth_pusher"),  
    path('fetch-emp-live-direction/', views.FetchEmpLive.as_view(), name="fetch_emp_live_direction"),
    path('change-job-request-process', views.change_job_request_process, name="change_job_request_process"),      
] 