from django.urls import path
from . import views

urlpatterns = [
    # Acounts
    path('accounts/login/', views.EmployeeLogin.as_view(), name="api_login"),
    path('accounts/logout/', views.EmployeeLogout.as_view(), name="api_logout"),
    path('accounts/employee-profile/<int:pk>/', views.EmployeeProfile.as_view(), name="api_employee_profile"),
    path('accounts/change-password-employee/', views.ChangePasswordEmployee.as_view(), name="api_change_password_employee"),
    path('accounts/change-employee-profile/', views.ChangeEmployeeProfile.as_view(), name="api_change_employee_profile"),
    path('accounts/employee-login-logs/<int:pk>/', views.EmployeeLoginLogs.as_view(), name="api_employee_login_logs"),
    path('accounts/employee-login-log-detail/<int:pk>/', views.EmployeeLoginLogDetail.as_view(), name="api_employee_login_log_detail"),
    path('accounts/create-employee/', views.EmployeeCreate.as_view(), name="api_employee_cfreate"),

    #Assets   
    path('assets/asset-list/', views.AssetList.as_view(), name="api_asset_list"),  
    path('assets/asset-assign/', views.AssetAssign.as_view(), name="api_asset_assign"),  

    # JOBS
    path('jobs/job-detail/<int:pk>/', views.JobDetail.as_view(), name="api_job_detail"),  
    path('jobs/create-alarm-report/', views.AlarmResponseReport.as_view(), name="api_create_alarm_report"),
    path('jobs/job-assign-api/', views.JobAssignAPI.as_view(), name="api_job_assign"),   
    path('jobs/request-denied/', views.JobRequestDenied.as_view(), name="api_job_request_denied"),
    path('jobs/cancel-job/', views.JobCancelled.as_view(), name="api_job_cancel_job"),

    #Logs
    path('logs/etlog/', views.ETLog.as_view(), name="api_etlog"),
]